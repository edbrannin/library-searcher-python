from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class ReprMixin(object):
    def __repr__(self):
        return pprint.pformat(vars(self))

"""
class Branch(Base, ReprMixin):
    __tablename__ = 'branches'
"""

class SearchResult(Base, ReprMixin):
    __tablename__ = 'search_results'

    search_query = Column(String)
    id = Column(Integer, primary_key=True)
    format = Column(String)
    holdings = None
    author = Column(String)
    title = Column(String)

class resource_holdings(Base, ReprMixin):
    __tablename__ = 'search_holdings'
    item_id = Column(Integer)
    barcode = Column(String, primary_key=True)
    branch_name = Column(String)
    collection_name = Column(String)
    call_class = Column(String)

class Status(Base, ReprMixin):
    __tablename__ = 'search_status'

    available = Column(Boolean)
    due_date = Column(Integer)
    due_date_string = Column(String)
    non_circulating = Column(Boolean)
    on_order = Column(Boolean)

    resource_id = Column(Integer)
    item_identifier = Column(String, primary_key=True) # Barcode
    status = Column(String)
    status_code = Column(String)

    """
    {
      "available": true,
      "dueDate": null,
      "dueDateString": null,
      "itemIdentifier": "39077051679580",
      "modStatus": null,
      "nonCirculating": false,
      "onOrder": false,
      "resourceId": 10964391,
      "status": "Not Checked Out",
      "statusCode": "available"
    }
    """


def setup_sqlalchemy(url):
    global session
    engine = create_engine(url)
    Session = sessionmaker(bind=engine)
    # Create all tables as needed
    Base.metadata.create_all(engine)
    return Session
