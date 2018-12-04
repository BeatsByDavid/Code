from sql_declaratives import *
from config import DB_STRING

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


class UploadingQueries:

    # Start some SQL Alchemy stuff
    def __init__(self):
        self.engine = create_engine(DB_STRING)
        Base.metadata.bind = self.engine
        self.db_session = sessionmaker()
        self.db_session.bind = self.engine

    # Create a connection to the DB
    def generate_session(self):
        # type: () -> Session
        return self.db_session()


    def add_data(self, **kwargs):
        # type: (dict) -> str
        session = self.generate_session()

        new_item = Data(**kwargs)
        session.add(new_item)
        session.commit()

        ret = new_item.to_json()

        session.close()

        return ret
