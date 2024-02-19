from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from Api.Schemas.schemas import VersionProject


def version_project():
    """[main method]: Retorna la version segmentada del software. Se estructura como major, minor, patch."""
    version= VersionProject(ver="0.0.9", major=0, minor=0, patch=9)
    return version
version= version_project()


#>> Metodo para enviar respuesta ~
def response_model_error(status_code: str, error: bool, message: str, res, headers=None):
    """[main method]: Devuelve un JSONResponse en cada solicitud a la API, para mostrar la respuesta al usuario."""
    response_headers = {"Content-Type": "application/json"}
    if headers:
        response_headers.update(headers)

    return JSONResponse(
        status_code=status_code,
        headers=response_headers,
        content=jsonable_encoder({
            "error": error,
            "message": message,
            "res": res,
            "version": f"v{version.ver}"
        })
    )