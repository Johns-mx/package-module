from Api.Schemas.schemas import VersionProject


def version_project():
    version= VersionProject(ver="0.0.3", major=0, minor=0, patch=3)
    return version
version= version_project()