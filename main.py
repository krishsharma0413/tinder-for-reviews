from uvicorn import run
from user_config import host, port

if __name__ == "__main__":
    run("app:app", host=host, port=port, reload=True)