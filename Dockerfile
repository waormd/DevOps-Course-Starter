FROM python:3.8.5-buster as base

ENV POETRY_HOME=/poetry
ENV PATH=${POETRY_HOME}/bin:$PATH

EXPOSE 5000 5000

RUN apt-get update && \
    apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python-openssl git && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python


FROM base as dev
ENTRYPOINT cd /todo-app && poetry install && poetry run flask run --host 0.0.0.0

FROM base as production
COPY . /todo-app
ENTRYPOINT cd /todo-app && poetry install && poetry run gunicorn -w 4 -b 0.0.0.0:5000 app:app

FROM base as test
COPY . /todo-app
ENTRYPOINT cd /todo-app && poetry install && poetry run pytest

