import fileinput
import pprint

import requests

import render_results
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
        save_search_result(text, i, item)

def save_search_result(query, position, item):
    result = Resource(
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

def update_availability():
    payload = availability_payload(session.query(Resource))
    r = post(AVAILABILITY_URL, payload)
    save_availability(*r["itemAvailabilities"])


def save_availability(*results):
    for result in results:
        status = Status(
                available=result['available'],
                due_date=result['dueDate'],
                due_date_string=result['dueDateString'],
                non_circulating=result['nonCirculating'],
                on_order=result['onOrder'],
                resource_id=result['resourceId'],
                item_identifier=result['itemIdentifier'],
                status=result['status'],
                status_code=result['statusCode'],
                )
        session.add(status)
    session.commit()

def availability_payload(search_results):
    answer = []
    for result in search_results:
        for holding in result.holdings:
            answer.append(dict(
                itemIdentifier=holding.barcode,
                resourceId=holding.item_id,
                ))
    return answer

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
    session = setup_sqlalchemy()()
    for line in fileinput.input():
        line = line.strip()
        if len(line) == 0:
            continue
        print line
        search(line)

    update_availability()
    with open('done.html', 'w') as out:
        out.write(render_results.render_results())


if __name__ == '__main__':
    main()

