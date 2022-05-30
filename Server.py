import uvicorn

if __name__ == "__main__":
    uvicorn.run('Main:app', host="0.0.0.0", port=$PORT, reload=True)
