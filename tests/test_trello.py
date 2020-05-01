import json
import os

import pytest
import responses
import re

from trello.trello import Trello


@pytest.fixture()
def trello_obj():
    return Trello(trello_key="fookey", trello_token="footoken")


@pytest.fixture()
def trello_url():
    return "https://api.trello.com/*"


@pytest.fixture()
def json_directory(setup_tests_directory):
    return os.path.join(setup_tests_directory, "fixtures")


@responses.activate
def test_get_lists(trello_obj, trello_url):
    expected = [{'id': '5af97c9dbbe346788853b3ba',
                 'name': 'test',
                 'closed': False,
                 'idBoard': '5af97addbaeeb13712b04ed1',
                 'pos': 81919,
                 'subscribed': False}]
    responses.add(responses.GET, re.compile(trello_url), json=expected, status=200)
    response = trello_obj.get_lists(board_id='fooid')
    assert response == expected


@responses.activate
def test_get_cards(trello_obj, trello_url, json_directory):
    with open(os.path.join(json_directory, 'cards.json')) as f:
        expected = json.load(f)
    responses.add(responses.GET, url=re.compile(trello_url), json=expected, status=200)
    response = trello_obj.get_cards(list_id='fooid')
    assert response == expected


@responses.activate
def test_create_checklist(trello_obj, trello_url):
    expected = {'id': '5af98622a7cfee3ce5bd3c9b',
                'name': 'test_checklist',
                'idBoard': '5af97addbaeeb13712b04ed1',
                'idCard': '5af981b43a87d3d98c9b7cfa',
                'pos': 32768,
                'checkItems': []}
    responses.add(responses.POST, url=re.compile(trello_url), json=expected, status=200)
    response = trello_obj.create_checklist(card_id='fooid', name='test_checklist')
    assert response == expected['id']


@responses.activate
def test_create_card(trello_obj, trello_url, json_directory):
    with open(os.path.join(json_directory, 'create_card.json')) as f:
        expected = json.load(f)
    responses.add(responses.POST, url=re.compile(trello_url), json=expected, status=200)
    response = trello_obj.create_card(list_id='5af97c9dbbe346788853b3ba', desc='foobar', name='test_card')
    assert response == expected['id']


@responses.activate
def test_add_attachment_to_card(trello_obj, trello_url):
    expected = {'id': '5af98ed1c7b83322d90cf081',
                'bytes': None,
                'date': '2018-05-14T13:27:45.702Z',
                'edgeColor': None,
                'idMember': '574cc3d3dec5144369efb6ee',
                'isUpload': False,
                'mimeType': '',
                'name': 'foobarzee',
                'previews': [],
                'url': 'http://www.google.com',
                'pos': 16384,
                'limits': {}}
    responses.add(responses.POST, url=re.compile(trello_url), json=expected, status=200)
    response = trello_obj.add_attachment_to_card(card_id='fooid', attachment_url='foourl', name='bar')
    assert response == expected['id']
