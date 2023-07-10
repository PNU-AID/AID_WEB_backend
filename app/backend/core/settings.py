from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv(dotenv_path="./env/.server.env", verbose=True)


class Settings(BaseSettings):  # mongodb 의 세팅을 저장하는 클래스(.\database\mongodb.py에서 client 생성하는데 쓰임)
    PROJECT_NAME: str = "AID_WEB"
    PROJECT_VERSION: str = "0.1.0"

    mongo_user: str
    mongo_password: str
    mongo_host: str
    mongo_port: str

    email_id: str
    email_pw: str

    # TODO
    # prod, dev env 분리 할 것

    class Confing:
        env_file = "./env/.server.env"
        env_file_encoding = "utf-8"
