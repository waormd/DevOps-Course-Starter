FROM python:3.8.5-buster as base

ENV POETRY_HOME=/poetry
ENV PATH=${POETRY_HOME}/bin:$PATH

RUN apt-get update && \
    apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python-openssl git && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python


FROM base as dev
ENTRYPOINT cd /todo-app && poetry install && poetry run flask run --host 0.0.0.0

FROM base as copied
COPY . /todo-app
WORKDIR /todo-app

FROM copied as prod
RUN poetry install --no-dev
ENTRYPOINT ["poetry", "run", "gunicorn", "-w", "4", "-b", "0.0.0.0:$PORT", "app:app"]

FROM copied as test
# Install Chrome
RUN poetry install
RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb &&\    
    apt-get install ./chrome.deb -y &&\    
    rm ./chrome.deb
    
# Install Chromium WebDriver
RUN LATEST=`curl -sSL https://chromedriver.storage.googleapis.com/LATEST_RELEASE` &&\    
    echo "Installing chromium webdriver version ${LATEST}" &&\    
    curl -sSL https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip -o chromedriver_linux64.zip &&\    
    apt-get install unzip -y &&\    
    unzip ./chromedriver_linux64.zip
ENTRYPOINT ["poetry", "run", "pytest"]

