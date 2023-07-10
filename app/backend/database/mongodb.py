# Python에서 MongoDB 데이터베이스에 연결하기 위해 PyMongo 모듈을 사용하는 예제
from backend.core import logger, settings
from pymongo import MongoClient
from pymongo.database import Database

# PyMongo 모듈의 MongoClient 클래스를 사용하여 MongoDB 서버에 연결
# MongoClient: MongoDB 서버에 연결하기 위한 인증 정보와 호스트 및 포트 정보를 인자로 받는다.


class MongoManager:
    def __init__(self):
        self.clinet: MongoClient = None
        self.db: Database = None
        self.db_logger = None

    def connect_logger(self):
        # logger 선언 순서 때문에 함수를 통해 연결
        self.db_logger = logger.get_logger("db_log")

    def connect_to_db(self):
        self.db_logger.info("Connecting to MongoDB...")
        self.clinet = MongoClient(
            f"mongodb://{settings.mongo_user}:"
            f"{settings.mongo_password}@"
            f"{settings.mongo_host}:"
            f"{settings.mongo_port}/?authMechanism=DEFAULT"
        )
        self.db = self.clinet["AID"]
        self.db_logger.info("Connected to MongoDB.")

    def close_db_connection(self):
        self.db_logger.info("Closing connection with MongoDB.")
        self.client.close()
        self.db_logger.info("Closed connection with MongoDB.")


# 이 코드에서는 연결할 MongoDB 서버의 인증 정보와 호스트 및 포트 정보를 settings 모듈에서 가져오고 있다.
# 이후에는 연결된 MongoDB 서버에서 "AID_test" 라는 이름의 데이터베이스를 선택하고 있다.
