import uvicorn

from decouple import config

if __name__ == "__main__":
    PORT = config("MONGODB_URL")

    uvicorn.run('Main:app', host="0.0.0.0", port=PORT, reload=True)
