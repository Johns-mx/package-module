from Api.Schemas.schemas import VersionProject


def version_project():
    version= VersionProject(ver="0.0.4", major=0, minor=0, patch=4)
    return version
version= version_project()