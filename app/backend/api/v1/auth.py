from backend.scheme import UserCreate, UserLogIn
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()  # auth 라우터를 위한 api router 선언부


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/signup")
def signup(user: UserCreate):
    # TODO
    # valid user email
    valid = True
    if valid:
        print(user)
        # print(get_password_hash(user.password))
        # create_user(user)
    else:
        return {"message": "signup fail"}
    return {"message": "signup success"}


@router.post("/login")
def login(user: UserLogIn):
    """login 하는 api

    Args:
        user (UserCreate): _description_

    Returns:
        _type_: _description_
    """

    return user


@router.post("/logout")
def logout(user: UserCreate):
    # 유저 password hashing
    return user


@router.delete("/signout")
def signout(user: UserCreate):
    # 유저 password hashing
    return user


@router.put("/modify")
def modify(user: UserCreate):
    # 유저 password hashing
    return user


@router.get("/get_user")
def get_user_info(user: UserCreate):
    # 유저 password hashing
    return user
