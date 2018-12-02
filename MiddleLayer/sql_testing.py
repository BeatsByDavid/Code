from sql_declaratives import *
from config import DB_STRING

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DB_STRING)

Base.metadata.bind = engine
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()

print type(session)

ret = session.query(Location).first()
print ret


# from DownloadingQueries import DownloadingQueries
# d = DownloadingQueries()
# d.query_data()
