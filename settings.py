import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME=os.getenv("NAME_PROJECT")
HASHING_UUID=os.getenv("UUID_HASHING")
BPA_NAME=os.getenv("NAME_BPA")
BPA_VERSION=os.getenv("VERSION_BPA")
