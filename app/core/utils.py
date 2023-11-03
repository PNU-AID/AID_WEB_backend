import logging
import random
import string


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
