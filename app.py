from flask import Flask, render_template, request, redirect, url_for
import session_items as session
import requests as r
import yaml

TRELLO_BASE_URL = 'https://api.trello.com'
TRELLO_BOARD_ID = 'CX81X1uD'

app = Flask(__name__)
app.config.from_object('flask_config.Config')

@app.route('/', methods=['POST'])
def indexPost():
    title = request.form['item']
    secrets = loadSecrets()
    lists = loadLists(secrets, TRELLO_BOARD_ID)
    for item in lists:
        if item['name'] == "Todo":
            addCard(secrets, item['id'], title)

    return index(loadItems(secrets, lists))

@app.route('/', methods=['GET'])
def indexGet():
    secrets = loadSecrets()
    lists = loadLists(secrets, TRELLO_BOARD_ID)
    return index(loadItems(secrets, lists))

@app.route('/move', methods=['POST'])
def indexPut():
    cardId = request.form['cardId']
    target = request.form['target']
    secrets = loadSecrets()
    lists = loadLists(secrets, TRELLO_BOARD_ID)
    for item in lists:
        if item['name'] == target:
            moveCard(secrets, cardId, item['id'])
    return index(loadItems(secrets, lists))

def index(sessionItems):
    return render_template('index.html', items = sessionItems)


def loadSecrets():
    with open('secrets.yml') as file:
        secrets = yaml.load(file, Loader=yaml.FullLoader)
        return secrets['trello']
    return {}

def loadItems(secrets, lists):
    flattened = []
    for item in lists:
        cards = loadCards(secrets, item['id'])
        for card in cards:
            flattened.append({'id': card['id'], 'status': item['name'], 'title': card['name']})
    return flattened


def loadLists(secrets, boardId):
    url = f'{TRELLO_BASE_URL}/1/boards/{boardId}/lists?key={secrets["api-key"]}&token={secrets["server-token"]}'
    print(f'GET to {url}')
    return r.get(url).json()

def loadCards(secrets, listId):
    url = f'{TRELLO_BASE_URL}/1/lists/{listId}/cards?key={secrets["api-key"]}&token={secrets["server-token"]}'
    print(f'GET to {url}')
    return r.get(url).json()

def addCard(secrets, listId, name):
    url = f'{TRELLO_BASE_URL}/1/cards?key={secrets["api-key"]}&token={secrets["server-token"]}&idList={listId}&name={name}'
    print(f'POST to {url}')
    return r.post(url)

def moveCard(secrets, cardId, targetListId):
    url = f'{TRELLO_BASE_URL}/1/cards/{cardId}?key={secrets["api-key"]}&token={secrets["server-token"]}&idList={targetListId}'
    print(f'PUT to {url}')
    return r.put(url)


if __name__ == '__main__':
    app.run()
