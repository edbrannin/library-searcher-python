import json

from model import *
import search

def setup_module():
    global session
    session = setup_sqlalchemy('sqlite://')()
    search.session = session

def read(name):
    with open('test_data/{name}.json'.format(name=name)) as i:
        return json.load(i)

def test_save_item():
    response = read('search-response')
    search.save_item("scraping", response['resources'][0])

    assert session.query(SearchResult).count() == 1
    result = session.query(SearchResult).one()

