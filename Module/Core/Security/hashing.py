import uuid, datetime
from settings import PROJECT_NAME, HASHING_UUID


def hashing_string_uuid(to_hash: str):
    """[method]: Hashea 'to_hash' con UUID de la app."""
    date= datetime.datetime.now()
    return uuid.uuid5(uuid.UUID(HASHING_UUID), f"{to_hash}{date}")
