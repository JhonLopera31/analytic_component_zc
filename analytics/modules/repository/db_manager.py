from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from pandas import DataFrame, read_sql_query
from config.settings import DB_CONFIGS


class DBManager:
    _engine = None

    def __init__(self, db_name: str) -> None:
        engine_name = DB_CONFIGS.get(db_name).get("engine")
        credentials = self._get_credentials(db_name)

        if engine_name == "mysql":
            url = URL.create(drivername="mysql+pymysql", **credentials)

        elif engine_name == "posgresql":
            url = URL.create(drivername="posgresql+pymysql", **credentials)

        self._engine = create_engine(url)


    def _get_credentials(self, db_name: str) -> dict:
        """
        Get database credentials from the environment variables
        :param db_name: Name of the database as set DB_CONFIG in config.py file
        :return: Dictionary with the database credentials
        """
        credentials_name = DB_CONFIGS.get(db_name).get("credentials_name")
        credentials = getenv(credentials_name).split(",")
        credentials = {
            "host": credentials[0],
            "username": credentials[1],
            "password": credentials[2],
            "database": credentials[3],
            "port": credentials[4],
        }
        return credentials

    def select_as_df(self, query, **kwargs) -> DataFrame:
        """
        Run a sql query statement and return the result as dataframe.
        :param query: The given sql statement.
        :param kwargs: kwargs according to pandas docs.
        https://pandas.pydata.org/docs/reference/api/pandas.read_sql_query.html
        :return: The query result as pandas dataframe
        """
        with self._engine.begin() as conn:
            df = read_sql_query(query, conn, *kwargs)
        return df

    def dispose_engine(self):
        self._engine.dispose()
