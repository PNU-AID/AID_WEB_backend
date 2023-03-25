from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv(dotenv_path="./env/.server.env", verbose=True)


class Settings(BaseSettings):
    PROJECT_NAME: str = "AID_WEB"
    PROJECT_VERSION: str = "0.1.0"

    mongo_user: str
    mongo_password: str
    mongo_host: str
    mongo_port: str

    # TODO
    # prod, dev env 분리 할 것

    class Confing:
        env_file = "./env/.server.env"
        env_file_encoding = "utf-8"


settings = Settings()
