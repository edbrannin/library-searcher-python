from datetime import datetime
import pprint

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()

class ModelMixin(object):
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return pprint.pformat(vars(self))

"""
class Branch(Base, ModelMixin):
    __tablename__ = 'branches'
"""

# FIXME Adjust PKs to be auto-generated IDs

class Resource(Base, ModelMixin):
    __tablename__ = 'resources'

    search_query = Column(String)
    id = Column(Integer, primary_key=True)
    position = Column(Integer)
    format = Column(String)
    holdings = None
    author = Column(String)
    title = Column(String)
    holdings = relationship("ResourceHolding")

class ResourceHolding(Base, ModelMixin):
    __tablename__ = 'resource_holdings'
    item_id = Column(Integer, ForeignKey("resources.id"))
    barcode = Column(String, primary_key=True)
    branch_name = Column(String)
    collection_name = Column(String)
    call_class = Column(String)
    resource = relationship("Resource", back_populates="holdings", uselist=False)
    status = relationship("Status", foreign_keys="Status.item_identifier")

class Status(Base, ModelMixin):
    __tablename__ = 'resource_status'

    available = Column(Boolean)
    due_date = Column(Integer)
    due_date_string = Column(String)
    non_circulating = Column(Boolean)
    on_order = Column(Boolean)

    resource_id = Column(Integer, ForeignKey("resource_holdings.item_id"))
    item_identifier = Column(String, ForeignKey("resource_holdings.barcode"), primary_key=True)
    status = Column(String)
    status_code = Column(String)

    holding = relationship("ResourceHolding", back_populates="status", uselist=False, foreign_keys=item_identifier)

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


def setup_sqlalchemy(url="sqlite:///books.sqlite3"):
    global session
    engine = create_engine(url)
    Session = sessionmaker(bind=engine)
    # Create all tables as needed
    Base.metadata.create_all(engine)
    return Session
