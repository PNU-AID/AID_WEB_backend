import logging
import random
import string

from bson import ObjectId

# FastAPI에서 사용할 유틸리티 함수들을 정의하는 모듈인 utils.py


# PyObjectId 클래스:
# MongoDB의 ObjectId를 Python에서 사용하기 쉽도록 Wrapping하여 FastAPI에서 쉽게 사용할 수 있도록 한다.
# 이 클래스는 bson.ObjectId 클래스를 상속하며,
# __get_validators__와 __modify_schema__ 메소드를 오버라이드하여 FastAPI에서 해당 클래스를 사용할 때 유효성 검사를 수행하도록 한다.

# 위에 내용을 더 쉬운표현으로 설명하자면,
# Python에서 MongoDB에서 사용되는 ObjectId는 일반적인 문자열과는 다른 형식을 갖고 있으며,
# 이를 FastAPI에서 바로 사용하면 유효성 검사를 통과하지 못할 수 있다.
# 따라서 PyObjectId 클래스는 해당 ObjectId를 Python에서 사용하기 쉬운 형태로 Wrapping하고,
# FastAPI에서 해당 클래스를 사용할 때 유효성 검사를 수행하도록 함으로써 이를 방지해준다.


class PyObjectId(ObjectId):
    # https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


# ObjectIdStr 클래스와 StrObjectId 클래스: ObjectId와 str 타입을 서로 변환하기 위한 유틸리티 클래스다.
# 이 클래스들도 __get_validators__와 validate 메소드를 오버라이드하여 FastAPI에서 해당 클래스를 사용할 때 유효성 검사를 수행하도록 한다.
# 결국 둘다 유효성 검사 기능을 한다.


class ObjectIdStr(str):
    # https://github.com/tiangolo/fastapi/issues/452
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise ValueError("Not a valid ObjectId")
        return str(v)


class StrObjectId(str):
    # https://github.com/tiangolo/fastapi/issues/452
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise ValueError("Not a str")
        return ObjectId(v)


# ----- Logger -----
class Logger:
    def __init__(self):
        self.formatter = logging.Formatter("[%(asctime)s] %(levelname)s %(message)s")
        self.logger_lst = {}

    def add_logger(self, logger_name, file_name, logging_level=logging.INFO):
        if self.logger_lst.get(logger_name, 0) != 0:
            # you can not make same name logger
            return
        handler = logging.FileHandler(file_name)
        handler.setFormatter(self.formatter)
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging_level)
        logger.addHandler(handler)

        self.logger_lst[logger_name] = logger

    def get_logger(self, logger_name):
        return self.logger_lst.get(logger_name, None)

    def info(self, logger_name, messege):
        try:
            self.logger_lst[logger_name].info(messege)
        except KeyError:
            raise KeyError()


# ----- serializer -----
def serializer(item) -> dict:
    return {
        **{"id": str(item[i]) for i in item if i == "_id"},
        **{i: item[i] for i in item if i != "_id"},
    }


# ----- random string -----
def get_random_name(length: int = 12) -> str:
    letter_set = string.ascii_letters + string.digits
    random_name = [random.choice(letter_set) for _ in range(length)]
    return "user-" + "".join(random_name)


# ----- message -----
def make_message(message: str) -> dict:
    return {"message": message}
