import json

from model import *
import search

def setup_function(function):
    global session
    session = setup_sqlalchemy('sqlite://')()
    search.session = session

def read(name):
    with open('test_data/{name}.json'.format(name=name)) as i:
        return json.load(i)

def test_save_item():
    response = read('search-response')
    search.save_item("scraping", 1, response['resources'][0])

    assert session.query(SearchResult).count() == 1
    result = session.query(SearchResult).one()

    assert result.search_query == "scraping"
    assert result.id == 10964391
    assert result.position == 1
    assert result.format == "Book"
    assert result.holdings == None
    assert result.author ==  "Ross, Cindy"
    assert result.title == "Scraping heaven : a family's journey along the Continental Divide"

    assert session.query(ResourceHolding).count() == 2

    holdings = session.query(ResourceHolding).order_by(ResourceHolding.barcode).all()

    assert holdings[0].item_id == 10964391
    assert holdings[0].barcode ==  "39077051679580"
    assert holdings[0].branch_name ==  "Irondequoit Public Library"
    assert holdings[0].collection_name ==  "."
    assert holdings[0].call_class ==  "917.8 ROS"

    assert holdings[1].item_id == 10964391
    assert holdings[1].barcode ==  "39077051679747"
    assert holdings[1].branch_name ==  "Irondequoit Public Library"
    assert holdings[1].collection_name ==  "."
    assert holdings[1].call_class ==  "917.8 ROS"
