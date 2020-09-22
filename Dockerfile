FROM python:3.8.5-buster as base

RUN apt-get update && \
    apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

COPY . /todo-app
RUN useradd -m user

USER user

ENV PATH=/home/user/.poetry/bin:/home/user/.local/bin:/home/user/.pyenv/bin:$PATH \
    PYENV_ROOT=/home/user/.pyenv 

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python && \
    pip install gunicorn flask && \
    cd /todo-app && \
    poetry install && \
    pip install requests


EXPOSE 5000 5000

FROM base as dev
RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv && \
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile && \
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile && \
    echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.profile && \
    pyenv install 3.8.5 && \
    pyenv global 3.8.5

ENTRYPOINT cd /todo-app && poetry run flask run --host 0.0.0.0

FROM base as production
ENTRYPOINT cd /todo-app && gunicorn -w 4 -b 0.0.0.0:5000 app:app

