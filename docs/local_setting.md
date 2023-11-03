# How to start

github repo fork
```sh
git clone [fork한 본인 repo의 url]
git remote add upstream https://github.com/PNU-AID/AID_WEB_backend
git remote -v
git checkout -t origin/dev
# upstream(협업 repo내용)과 동기화 하려면 아래 명령어 실행
git pull upstream dev
# 이후 기능 브랜치 파서 작업
git checkout -b feat/<기능 내용>
```

## Setting
- [install pyenv](https://github.com/pyenv/pyenv)
  - 윈도우는 이 링크로 설치 : [pyenv-win](https://github.com/pyenv-win/pyenv-win)
- [install poetry](https://python-poetry.org/docs/)
- use Python 3.10.9

## 가상환경 설정 방법
```sh
pyenv install 3.10.9
pyenv local 3.10.9
# 터미널 재시작 혹은 아래 명령어 실행
pyenv shell 3.10.9
poetry config virtualenvs.in-project true
poetry config virtualenvs.path "./.venv"
poetry config --list # poetry config 확인
poetry install
poetry shell
pre-commit install
```
---

## 백엔드 서버 여는 방법

```sh
mkdir env
touch .server.env
touch .db.env
```
환경변수는 AID_WEB 노션에 있으니 참고 바람
```sh
# .server.env sample
mongo_user=admin_user
mongo_password=password
mongo_host=db
mongo_port=27017
# openssl rand -hex 32
SECRET_KEY=***
REFRESH_SECRET_KEY=***
ADMIN_NAME=***
ADMIN_PWD=***
email_id=***
email_pw=***(앱 비밀번호)

# .db.env sample
MONGO_INITDB_ROOT_USERNAME=admin_user
MONGO_INITDB_ROOT_PASSWORD=password
```

_도커 설치 필수로 되어있어야 함_

환경 설정을 모두 마치면 도커를 실행
```
docker compose up -d
```

127.0.0.1/api/docs로 접근하여 페이지 열리는지 확인
