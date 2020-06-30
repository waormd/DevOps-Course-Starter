from flask import Flask, render_template, request, redirect, url_for
import session_items as session
import requests as r
import yaml

TRELLO_BASE_URL = 'https://api.trello.com'

app = Flask(__name__)
app.config.from_object('flask_config.Config')

@app.route('/', methods=['POST'])
def indexPost():
    item = request.form['item']
    session.add_item(item)
    return index(loadItems())

@app.route('/', methods=['GET'])
def indexGet():
    return index(loadItems())

def index(sessionItems):
    return render_template('index.html', items = sessionItems)

def loadSecrets():
    with open('secrets.yml') as file:
        secrets = yaml.load(file, Loader=yaml.FullLoader)
        return secrets['trello']
    return {}

def loadItems():
    secrets = loadSecrets()
    lists = loadLists(secrets, 'CX81X1uD')
    flattened = []
    for item in lists:
        cards = loadCards(secrets, item['id'])
        for card in cards:
            flattened.append({'id': card['id'], 'status': item['name'], 'title': card['name']})
    return flattened


def loadLists(secrets, boardId):
    return r.get(f'{TRELLO_BASE_URL}/1/boards/{boardId}/lists?key={secrets["api-key"]}&token={secrets["server-token"]}').json()

def loadCards(secrets, listId):
    return r.get(f'{TRELLO_BASE_URL}/1/lists/{listId}/cards?key={secrets["api-key"]}&token={secrets["server-token"]}').json()


if __name__ == '__main__':
    app.run()
