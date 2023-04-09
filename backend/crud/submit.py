from backend.database import db
#submit에 관한 crud 구현

def create_submit(data: dict):
    db["submit"].insert_one(data)


def read_all_submit(data): #submit을 모두 읽음
    all_submits = db.submit.find()
    return all_submits


def read_submit(data): #submit을 하나 읽어옴
    submits = db.submit.find_one({"id":id})
    return submits