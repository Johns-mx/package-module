from fastapi import FastAPI
import uvicorn


app = FastAPI(
    title="Package Module Api",
    version="0.0.1"
)


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)