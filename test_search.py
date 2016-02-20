import json

from model import *
from search import *

def read(name):
    with open('test_data/{name}.json'.format(name=name)) as i:
        return json.load(i)

def test_save_item():
    response = read('search-response')
    save_item("scraping", response['resources'][0])

    # TODO Assert
    assert session.query(SearchResult).count() == 1
