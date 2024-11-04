FROM python:3.12.7-slim-bullseye

WORKDIR /container

RUN apt-get update && apt-get install -y \
    sqlite3 \
    libsqlite3-dev

COPY requirements.txt /container/requirements.txt

RUN pip install -r requirements.txt

COPY /app /container/app
COPY /tests /container/tests

EXPOSE 8000

CMD [ "python", "app/main.py" ]
