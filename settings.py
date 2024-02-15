import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME=os.getenv("NAME_PROJECT")
HASHING_UUID=os.getenv("UUID_HASHING")
BPA_NAME=os.getenv("NAME_BPA")
BPA_VERSION=os.getenv("VERSION_BPA")
BPA_PATH=os.getenv("PATH_BPA")

YPW_URL=os.getenv("YPW_URL_API")
YPW_APP_CONNECT=os.getenv("YPW_APP_CONNECT")
YPW_KEY_USER=os.getenv("YPW_KEY_USER")
YPW_PUBLIC_KEY=os.getenv("YPW_PUBLIC_KEY")
YPW_PRIVATE_KEY=os.getenv("YPW_PRIVATE_KEY")