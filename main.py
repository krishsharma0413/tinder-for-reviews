from uvicorn import run

if __name__ == "__main__":
    run("app:app", host="localhost", port=8000, reload=True)