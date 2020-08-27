import pytest
import app
import dotenv
from unittest.mock import MagicMock
import requests.models as models
from todo.trello_api import TrelloApi
import json

@pytest.fixture
def client():
    file_path = dotenv.find_dotenv('.env.test')
    trello_api = MagicMock()
    dotenv.load_dotenv(file_path, override=True)

    trello_api.loadLists.return_value = json.loads('[{"id":"5efb3c3b14042c23bf8a2cad","name":"Todo","closed":false,"pos":65535,"softLimit":null,"idBoard":"5efb3c14dca74d15041cd57e","subscribed":false}]')
    trello_api.loadCards.return_value = json.loads('[{"id":"5efb3c57227fb087384f4476","checkItemStates":null,"closed":false,"dateLastActivity":"2020-08-03T16:05:42.564Z","desc":"","descData":null,"dueReminder":null,"idBoard":"5efb3c14dca74d15041cd57e","idList":"5efb3c3b14042c23bf8a2cad","idMembersVoted":[],"idShort":1,"idAttachmentCover":null,"idLabels":[],"manualCoverAttachment":false,"name":"Card 1","pos":65535,"shortLink":"DrXnHrWo","isTemplate":false,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":false,"votes":0,"viewingMemberVoted":false,"subscribed":false,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":null,"comments":0,"attachments":0,"description":false,"due":null,"dueComplete":false},"dueComplete":false,"due":null,"idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/DrXnHrWo","subscribed":false,"url":"https://trello.com/c/DrXnHrWo/1-card-1","cover":{"idAttachment":null,"color":null,"idUploadedBackground":null,"size":"normal","brightness":"light"}}]')
    
    test_app = app.create_app(trello_api)
    with test_app.test_client() as client:
        yield client

def test_index_page(client):
    response = client.get('/')
    assert "Card 1" in str(response.data)