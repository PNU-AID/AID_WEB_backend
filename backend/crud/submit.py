# submit에 관한 crud 구현
from backend.database import db


def create_submit(data):  # submit을 생성(submit form을 생성?), api\endpoint\submit api에서 사용함
    db["submit"].insert_one(data)
    print(type(data))
    print(data)


def read_all_submit(data):  # submit을 모두 읽음
    pass


def read_submit(data):  # submit을 하나 읽어옴
    pass
