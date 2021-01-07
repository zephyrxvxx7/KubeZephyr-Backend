import uvicorn
from app.main import app


if __name__ == "__main__":
    uvicorn.run("start_server:app", host="0.0.0.0", port=8000, reload=True)
