import json
import asyncio
from fastapi import WebSocket, WebSocketDisconnect

from kubernetes.client import CoreV1Api
from kubernetes.stream import stream

RESIZE_CHANNEL = 4

class ConnectionManager:
    def __init__(self, core_v1_api: CoreV1Api, name: str, namespace: str):
        self.stream = None
        self.websocket = None
        self.core_v1_api = core_v1_api
        self.name = name
        self.namespace = namespace
        self.exec_command = [
            "/bin/sh",
            "-c",
            'export LINES=20; export COLUMNS=100; '
            'TERM=xterm-256color; export TERM; [ -x /bin/bash ] '
            '&& ([ -x /usr/bin/script ] '
            '&& /usr/bin/script -q -c "/bin/bash" /dev/null || exec /bin/bash) '
            '|| exec /bin/sh'
        ]
    
    def _pod_exec(self):
        self.stream = stream(self.core_v1_api.connect_get_namespaced_pod_exec,
                            name=self.name,
                            namespace=self.namespace,
                            command=self.exec_command,
                            stderr=True, stdin=True,
                            stdout=True, tty=True,
                            _preload_content=False)
    
    def _set_size(self, rows, cols):
        self.stream.write_channel(RESIZE_CHANNEL, json.dumps({"Height": int(rows), "Width": int(cols)}))
    
    async def on_connect(self, websocket: WebSocket, rows=20, cols=80):
        await websocket.accept()
        self.websocket = websocket

        self._pod_exec()
        self._set_size(rows, cols)

        await asyncio.gather(self._receive(), self._send())

    async def _receive(self):
        while True:
            try:
                command = await self.websocket.receive_text()
                try:
                    resize = json.loads(command)
                    assert type(resize)  == list
                    rows = resize[0]
                    cols = resize[1]
                    self._set_size(rows, cols)
                except:
                    self.stream.write_stdin(command)
            except WebSocketDisconnect:
                await self._disconnect()
                break
                
    
    async def _send(self):
        while self.stream.is_open():
            await asyncio.sleep(0)
            
            try:
                if self.stream.peek_stdout():
                    stdout = self.stream.read_stdout()
                    await self.websocket.send_text(stdout)

                if self.stream.peek_stderr():
                    stderr = self.stream.read_stderr()
                    await self.websocket.send_text(stderr)
            except:
                pass
        else:
            await self._disconnect()
    
    async def _disconnect(self):
        try:
            if self.stream and self.stream.is_open():
                self.stream.write_stdin('\u0003')
                self.stream.write_stdin('\u0004')
                self.stream.write_stdin('exit\r')
            await self.websocket.close()
        except:
            pass
        
        