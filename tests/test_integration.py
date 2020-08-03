import pytest
import todo.app as app
import dotenv
import unittest.mock
import requests.models as models

@pytest.fixture
def client():
    file_path = dotenv.find_dotenv('.env.test')
    dotenv.load_dotenv(file_path, override=True)
    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client

def test_index_page(client):
    # unittest.mock.patch(models, 'json', return_value='[{"id":"5efb3c3b14042c23bf8a2cad","name":"Todo","closed":false,"pos":65535,"softLimit":null,"idBoard":"5efb3c14dca74d15041cd57e","subscribed":false},{"id":"5efb3c46f8d20e47ad68885f","name":"In progress","closed":false,"pos":131071,"softLimit":null,"idBoard":"5efb3c14dca74d15041cd57e","subscribed":false},{"id":"5efb3c499cd3104241539e35","name":"Done","closed":false,"pos":196607,"softLimit":null,"idBoard":"5efb3c14dca74d15041cd57e","subscribed":false}]')
    response = client.get('/')