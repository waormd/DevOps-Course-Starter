import requests as r

class TrelloApi:

    def __init__(self, url, boardId, apiKey, serverToken):
        self.url = url
        self.boardId = boardId
        self.apiKey = apiKey
        self.serverToken = serverToken

    def loadLists(self):
        url = f'{self.url}/1/boards/{self.boardId}/lists?key={self.apiKey}&token={self.serverToken}'
        print(f'GET to {self.boardId}: {url}')
        return r.get(url).json()

    def loadCards(self, listId):
        url = f'{self.url}/1/lists/{listId}/cards?key={self.apiKey}&token={self.serverToken}'
        print(f'GET to {self.boardId}: {url}')
        return r.get(url).json()

    def addCard(self, listId, name):
        url = f'{self.url}/1/cards?key={self.apiKey}&token={self.serverToken}&idList={listId}&name={name}'
        print(f'POST to {self.boardId}: {url}')
        return r.post(url)

    def moveCard(self, cardId, targetListId):
        url = f'{self.url}/1/cards/{cardId}?key={self.apiKey}&token={self.serverToken}&idList={targetListId}'
        print(f'PUT to {self.boardId}: {url}')
        return r.put(url)
