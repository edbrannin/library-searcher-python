import csv
import fileinput
import pprint

import requests

from model import *

DEBUG = False

if DEBUG:
    # http://stackoverflow.com/a/16630836/25625
    import logging

    # These two lines enable debugging at httplib level (requests->urllib3->http.client)
    # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
    # The only thing missing will be the response.body which is not logged.
    try:
        import http.client as http_client
    except ImportError:
        # Python 2
        import httplib as http_client
    http_client.HTTPConnection.debuglevel = 1

    # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

session = None


SEARCH_URL = "http://catalogplus.libraryweb.org/search"
AVAILABILITY_URL = "http://catalogplus.libraryweb.org/availability"
# Library Javascritpt adds timestamps to avoid caches like this:
# ?_=1455916577153

HEADERS = {
        "Referer":"http://catalogplus.libraryweb.org/",
        "Accept":"application/json, text/javascript, */*; q=0.01",
        "Content-Type":"application/json",
        }

def post(url, body):
    r = requests.post(url, json=body, headers=HEADERS)
    try:
        return r.json()
    except:
        print r.text
        raise

def search(text):
    r = post(SEARCH_URL, search_payload(text))
    for i, item in enumerate(r['resources']):
        save_item(text, i, item)

def save_item(query, position, item):
    result = SearchResult(
            search_query=query,
            id=item['id'],
            position=position,
            format=item['format'],
            author=item['shortAuthor'],
            title=item['shortTitle']
            )
    session.add(result)
    for holding in item['holdingsInformations']:
        rh = ResourceHolding(
                item_id=result.id,
                barcode=holding['barcode'],
                branch_name=holding['branchName'],
                collection_name=holding['collectionName'],
                call_class=holding['callClass']
                )
        session.add(rh)
    session.commit()

class Resource(object):
    def __init__(self, resource):
        self.format = resource['format']
        self.holdings = resource['holdingsInformations']
        self.author = resource['shortAuthor']
        self.title = resource['shortTitle']


def availability_payload(*items):
    pass
    # itemIdentifier=resources[x].barCode,
    # resourceId=resources[x].holdingsInformations[y].id

def search_payload(text, branch_ids=()):
    return {
            "searchTerm"     : text,
            "startIndex"     : 0,
            "hitsPerPage"    : 12,
            "facetFilters"   : [],
            "branchFilters"  : branch_ids,
            "sortCriteria"   : "Relevancy",
            "targetAudience" : "",
            "addToHistory"   : True,
            "dbCodes"        : []
            }
# {"searchTerm":"Asch\tBear Shadow","startIndex":0,"hitsPerPage":12,"facetFilters":[],"branchFilters":["1"],"sortCriteria":"Relevancy","targetAudience":"","addToHistory":true,"dbCodes":[]}

    pass



def main():
    global session
    session = setup_sqlalchemy('sqlite:///books.sqlite3')()
    s = Searcher()
    results = dict()
    for line in fileinput.input():
        line = line.strip()
        if len(line) == 0:
            continue
        print line
        results[line] = search(line)
        break

    with open('results.csv', 'wb') as writer:
        w = csv.writer(writer)

        #pprint.pprint(results)
        for line, result in results.items():
            print line
            for resource in result['resources']:
                r = Resource(resource)
                # pprint.pprint(vars(r))
                for holding in r.holdings:
                    w.writerow([(s or '').encode('utf-8') for s in [
                        line,
                        r.title,
                        r.author,
                        r.format,
                        holding['branchName'],
                        holding['collectionName'],
                        holding['callClass'],
                        ]])


if __name__ == '__main__':
    main()

