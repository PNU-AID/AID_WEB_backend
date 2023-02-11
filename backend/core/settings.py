from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv(dotenv_path=".env", verbose=True)


class Settings(BaseSettings):
    mongo_user: str
    mongo_password: str
    mongo_host: str
    mongo_port: str

    # TODO
    # prod, dev env 분리 할 것

    class Confing:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
