from Api.Schemas.schemas import VersionProject


def version_project():
    version= VersionProject(ver="0.0.5", major=0, minor=0, patch=5)
    return version
version= version_project()