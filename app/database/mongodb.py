from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.core import settings
from app.models import __all_model__

# DB username, password에 특수문자 사용하는 방법
# https://stackoverflow.com/questions/39237813/how-to-escape-in-a-password-in-pymongo-connection


async def initiate_database():
    uri = (
        f"mongodb://{settings.mongo_user}:"
        f"{settings.mongo_password}@"
        f"{settings.mongo_host}:"
        f"{settings.mongo_port}/?authMechanism=DEFAULT"
    )
    client = AsyncIOMotorClient(uri)
    await init_beanie(
        database=client[settings.mongo_db_name],
        document_models=__all_model__,
    )


# 이 코드에서는 연결할 MongoDB 서버의 인증 정보와 호스트 및 포트 정보를 settings 모듈에서 가져오고 있다.
# 이후에는 연결된 MongoDB 서버에서 "AID_test" 라는 이름의 데이터베이스를 선택하고 있다.
