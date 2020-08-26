import app
import requests as r
import pytest
import os
import yaml
from threading import Thread
from selenium import webdriver

def createBoard(key, token, boardName):
    resp = r.post(f"https://api.trello.com/1/boards/?key={key}&token={token}&name={boardName}").json()
    return resp['id']

def deleteBoard(key, token, boardId):
    r.delete(f"https://api.trello.com/1/boards/{boardId}?key={key}&token={token}")

@pytest.fixture(scope='module')
def test_app():
    apiKey = os.getenv('TRELLO_API_KEY')
    serverToken = os.getenv('TRELLO_SERVER_TOKEN')
    board_id = createBoard(apiKey, serverToken, 'testBoard')

    os.environ['TRELLO_BOARD_ID'] = board_id

    from todo.trello_api import TrelloApi

    trello_api = TrelloApi('https://api.trello.com', board_id, apiKey, serverToken)
    application = app.create_app(trello_api)

    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield app

    thread.join(1)
    deleteBoard(apiKey, serverToken, board_id)

@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver

def test_task_journey(driver, test_app):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'

