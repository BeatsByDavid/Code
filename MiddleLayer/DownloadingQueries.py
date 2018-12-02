from sql_declaratives import *
from config import DB_STRING

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


class DownloadingQueries:

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

    # Creates a query based on named arguments
    #   data_type   -> The SQL Table to query
    #   **kwargs    -> Filter arguments
    #       Valid keys: [*(table_columns),  -> Any column name in the table
    #                       order_by,       -> A column name to order by
    #                       direction,      -> ASC or DESC
    #                       limit]          -> The maximum number or rows to return
    # Names that match columns in the table will be filtered with an EQUALS operator
    #   ie. "KEY": "VALUE" -> WHERE KEY=VALUE
    # This does NOT execute the query. To get all rows, call .all() on the returned object
    def start_adv_query(self, data_type, **kwargs):
        # Create a connection to the database
        session = self.generate_session()

        # Get a list of column names
        keys = data_type.__table__.columns.keys()

        # Start a query
        q = session.query(data_type)

        # Apply filters based on the column names
        # Loop through all the named arguments
        for key, value in kwargs.items():
            # if the name matches a column
            if key in keys:
                # Apply the filter
                q = q.filter(data_type.__getattribute__(data_type, key) == kwargs[key])

        # Apply logistical filters/conditions (AFTER THE WHERE CLAUSE)
        # Order by a specific column
        if 'order_by' in kwargs:
            # Find the column to order row by
            col = data_type.__getattribute__(data_type, kwargs['order_by'])
            # Check if there is a desired direction
            if 'direction' in kwargs:
                if kwargs['direction'] == 'ASC':
                    col = col.asc()
                elif kwargs['direction'] == 'DESC':
                    col = col.desc()
            # Apply the order
            q = q.order_by(col)
        # Limit the number or rows returned
        if 'limit' in kwargs:
            q = q.limit(kwargs['limit'])

        return q

    # Helper function that converts an array or row returned from
    # a query to a json array
    # REQUIREMENT: The item that you want to serialize MUST have
    # a to_json() function that returns a str object
    #   ie. in sql_declaratives add a to_json to each table
    # FUTURE: Add a 'level' argument that converts foreign keys
    # to the actual objects for a certain depth
    def sql_array_to_json_array(self, results):
        j = []
        for result in results:
            j.append(result.to_json())
        return j

    # Method used to query the LOCATION table
    # See start_adv_query for more information
    def query_locations(self, **kwargs):
        q = self.start_adv_query(Location, **kwargs)
        return self.sql_array_to_json_array(q.all())

    # Method used to query the DATA table
    # See start_adv_query for more information
    def query_data(self, **kwargs):
        q = self.start_adv_query(Data, **kwargs)
        return self.sql_array_to_json_array(q.all())

    # Method used to query the DEVICE table
    # See start_adv_query for more information
    def query_devices(self, **kwargs):
        q = self.start_adv_query(Device, **kwargs)
        return self.sql_array_to_json_array(q.all())
