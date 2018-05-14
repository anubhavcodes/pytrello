import json
import os

import pytest
import responses
import re

from create_trello_cards.trello import Trello


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
