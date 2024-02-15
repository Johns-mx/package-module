import uvicorn
from fastapi import FastAPI
from Api.Config.methods import version
from Api.Routers import package, user


app = FastAPI(
    title="Package Module Api",
    version=version.ver
)


app.include_router(package.package_router)
app.include_router(user.user_router)


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)