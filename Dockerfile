FROM python:3.10-slim

WORKDIR /app

# .pyc(바이트코드) 생성 x
ENV PYTHONDONTWRITEBYTECODE 1
# 버퍼 사용 x
ENV PYTHONUNBUFFERED 1

COPY ./app .

COPY ./Pipfile .
COPY ./Pipfile.lock .

RUN pip install --upgrade pip && pip install pipenv

RUN pipenv install --system --deploy

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "80"]
