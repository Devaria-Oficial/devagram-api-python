import uvicorn

from decouple import config

if __name__ == "__main__":
    PORT = config("PORT")

    if not PORT:
        PORT = 5000

    PORT = int(PORT)    

    uvicorn.run('Main:app', host="0.0.0.0", port=PORT, reload=True)
