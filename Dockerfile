FROM python:3.10-slim

WORKDIR /app

COPY ./app .

COPY ./Pipfile .
COPY ./Pipfile.lock .

RUN pip install --upgrade pip && pip install pipenv

RUN pipenv install --system --deploy

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "80"]
