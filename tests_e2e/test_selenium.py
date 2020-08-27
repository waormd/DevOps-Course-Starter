import app
import requests as r
import pytest
import os
import time
import yaml
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By

def createBoard(key, token, board_name):
    post = f"https://api.trello.com/1/boards/?key={key}&token={token}&name={board_name}&defaultLists=false"
    print("POST to " + post)
    resp = r.post(post).json()
    print("BOARD_ID: " + resp['id'])
    return resp['id']

def createListsOnBoard(key, token, board_id):
    postTodo = f"https://api.trello.com/1/lists/?key={key}&token={token}&idBoard={board_id}&name=Todo"
    postInProgress = f"https://api.trello.com/1/lists/?key={key}&token={token}&idBoard={board_id}&name=In%20progress"
    postDone = f"https://api.trello.com/1/lists/?key={key}&token={token}&idBoard={board_id}&name=Done"
    print("POST to " + postTodo)
    print("POST to " + postInProgress)
    print("POST to " + postDone)
    resp = r.post(postTodo)
    resp = r.post(postInProgress)
    resp = r.post(postDone)


def deleteBoard(key, token, boardId):
    delete = f"https://api.trello.com/1/boards/{boardId}?key={key}&token={token}"
    print("DELETE to " + delete)
    r.delete(delete)

@pytest.fixture(scope='module')
def test_app():
    api_key = os.getenv('TRELLO_API_KEY')
    server_token = os.getenv('TRELLO_SERVER_TOKEN')
    board_id = createBoard(api_key, server_token, 'testBoard')
    createListsOnBoard(api_key, server_token, board_id)

    os.environ['TRELLO_BOARD_ID'] = board_id

    from todo.trello_api import TrelloApi

    trello_api = TrelloApi('https://api.trello.com', board_id, api_key, server_token)
    application = app.create_app(trello_api)

    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application

    thread.join(1)
    deleteBoard(api_key, server_token, board_id)

@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver

def test_task_journey(driver, test_app):
    expectedCard = 'test-card'
    driver.get('http://localhost:5000/')
    addTextBox = driver.find_element(By.XPATH, '//*[@id="item"]')
    addTextBox.send_keys(expectedCard)
    print("HERE")

    submit = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/form/input[2]')
    submit.click()

    time.sleep(2)
    driver.refresh()
    actualCard = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/table[1]/tbody/tr[1]/td[1]').text
    
    assert actualCard == expectedCard
    assert driver.title == 'To-Do App'

