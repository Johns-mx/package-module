import uvicorn
from fastapi import FastAPI
from Api.Config.methods import version
from Api.Routers.package import package_router


app = FastAPI(
    title="Package Module Api",
    version=version.ver
)


app.include_router(package_router)


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)