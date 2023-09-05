## Setting
- install pyenv
- install poetry
- use Python 3.10.9

## 가상환경 설정 방법
```sh
pyenv install 3.10.9
pyenv local 3.10.9
# poetry config virtualenvs.in-project true
# poetry config virtualenvs.path "./.venv"
poetry install

pre-commit install
```
