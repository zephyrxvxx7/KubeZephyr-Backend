docker run -d \
  --name kubezephyr_backend_container \
  -v $(pwd)/app:/app \
  -p 8080:80 \
  kubezephyr_backend_image \
  /start-reload.sh