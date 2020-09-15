FROM python:3.8.5-buster

COPY . /todo-app
RUN useradd -m user

USER user

ENV PATH=/home/user/.poetry/bin:/home/user/.local/bin:$PATH 

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python && \
    pip install gunicorn flask && \
    cd /todo-app && \
    poetry install && \
    pip install requests

EXPOSE 5000 5000


ENTRYPOINT cd /todo-app && gunicorn -w 4 -b 0.0.0.0:5000 app:app

