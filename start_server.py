import uvicorn
from app.main import app


if __name__ == "__main__":
    uvicorn.run("start_server:app", host="0.0.0.0", port=9487, reload=True)
