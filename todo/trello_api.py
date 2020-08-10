import requests as r

class TrelloApi:


    def __init__(self, url, secrets):
        self.url = url
        self.secrets = secrets

    def loadLists(self, boardId):
        url = f'{self.url}/1/boards/{boardId}/lists?key={self.secrets["api-key"]}&token={self.secrets["server-token"]}'
        print(f'GET to {url}')
        return r.get(url).json()

    def loadCards(self, listId):
        url = f'{self.url}/1/lists/{listId}/cards?key={self.secrets["api-key"]}&token={self.secrets["server-token"]}'
        print(f'GET to {url}')
        return r.get(url).json()

    def addCard(self, listId, name):
        url = f'{self.url}/1/cards?key={self.secrets["api-key"]}&token={self.secrets["server-token"]}&idList={listId}&name={name}'
        print(f'POST to {url}')
        return r.post(url)

    def moveCard(self, cardId, targetListId):
        url = f'{self.url}/1/cards/{cardId}?key={self.secrets["api-key"]}&token={self.secrets["server-token"]}&idList={targetListId}'
        print(f'PUT to {url}')
        return r.put(url)
