from sqlalchemy import create_engine
from sqlalchemy.engine import URL,Engine
from pandas import DataFrame, read_sql_query


class DBManager:

    _engine = None

    @classmethod
    def select_as_df(cls,query,**kwargs) -> DataFrame:
        pass