# How to start

github repo fork
```sh
git clone [fork한 본인 repo의 url]
git remote add upstream [https://github.com/sihyeong671/AID_WEB]
git remote -v
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
poetry config virtualenvs.in-project true
poetry config virtualenvs.path "./.venv"
poetry config --list
poetry install
poetry shell
pre-commit install
```
