from flask import Flask, render_template, request, redirect, url_for
from todo.item import Item
from todo.view import ViewModel
from todo.trello_api import TrelloApi
import os

import requests as r
import yaml

TRELLO_BASE_URL = 'https://api.trello.com'
TRELLO_BOARD_ID = os.getenv('TRELLO_BOARD_ID')

def loadSecrets():
    with open('config/secrets.yml') as file:
        secrets = yaml.load(file, Loader=yaml.FullLoader)
        return secrets['trello']
    return {}

app = Flask(__name__)
trelloApi = TrelloApi(TRELLO_BASE_URL, loadSecrets())

def create_app():
    app = Flask(__name__)
    return app, trelloApi

@app.route('/', methods=['POST'])
def indexPost():
    title = request.form['item']
    lists = trelloApi.loadLists(TRELLO_BOARD_ID)
    for item in lists:
        if item['name'] == "Todo":
            trelloApi.addCard(item['id'], title)
    return redirect(url_for('indexGet'))

@app.route('/', methods=['GET'])
def indexGet():
    lists = trelloApi.loadLists(TRELLO_BOARD_ID)
    item_view_model = ViewModel(loadItems(lists))
    return render_template('index.html', view_model = item_view_model)

@app.route('/complete_item', methods=['POST'])
def indexPut():
    cardId = request.form['cardId']
    target = request.form['target']
    lists = trelloApi.loadLists(TRELLO_BOARD_ID)
    for item in lists:
        if item['name'] == target:
            trelloApi.moveCard(cardId, item['id'])
    return redirect(url_for('indexGet'))


def loadItems(lists):
    flattened = []
    for item in lists:
        cards = trelloApi.loadCards(item['id'])
        for card in cards:
            flattened.append(Item(card['id'], item['name'], card['name'], card['dateLastActivity']))
    return flattened

if __name__ == '__main__':
    app, trelloApi = create_app()
    app.run()
