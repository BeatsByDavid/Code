from sql_declaratives import *
from config import DB_STRING

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

class DownloadingQueries:

    def __init__(self):
        self.engine = create_engine(DB_STRING)

        Base.metadata.bind = self.engine
        self.db_session = sessionmaker()
        self.db_session.bind = self.engine

        pass

    def generate_session(self):
        # type: () -> Session
        return self.db_session()

    def start_adv_query(self, data_type, **kwargs):
        session = self.generate_session()
        keys = data_type.__table__.columns.keys()

        q = session.query(data_type)

        for key, value in kwargs.items():
            if key in keys:
                q = q.filter(data_type.__getattribute__(data_type, key) == kwargs[key])

        if 'order_by' in kwargs:
            col = data_type.__getattribute__(data_type, kwargs['order_by'])
            if 'direction' in kwargs:
                if kwargs['direction'] == 'ASC':
                    col = col.asc()
                elif kwargs['direction'] == 'DESC':
                    col = col.desc()
            q = q.order_by(col)
        if 'limit' in kwargs:
            q = q.limit(kwargs['limit'])

        return q

    def sql_array_to_json_array(self, results):
        j = []
        for result in results:
            j.append(result.to_json())
        return j

    def query_locations(self, **kwargs):
        q = self.start_adv_query(Location, **kwargs)
        return self.sql_array_to_json_array(q.all())

    def query_data(self, **kwargs):
        q = self.start_adv_query(Data, **kwargs)
        return self.sql_array_to_json_array(q.all())

    def query_devices(self, **kwargs):
        q = self.start_adv_query(Device, **kwargs)
        return self.sql_array_to_json_array(q.all())
