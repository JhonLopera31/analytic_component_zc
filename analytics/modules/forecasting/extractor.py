from modules.forecasting import queries
from pandas import DataFrame
from modules.logs.loggers import GeneralLogger
from modules.repository.db_manager import DBManager


class ForecastingExtractor:
    
    _training_data: DataFrame = None
    
    @classmethod
    def extract_training_data(cls, json_content:dict) -> DataFrame:
        df = DataFrame(json_content.get("data"))
        df = df.join(DataFrame(df['counts'].tolist()).add_prefix('interval_'))
        cls._training_data = df.drop("counts", axis=1)
        return cls._training_data 
        
    
    @classmethod
    def extract_location_data(cls, cluster_location: dict, radius: int | float) -> DataFrame:
        """This method is used to extract the coordinates and dates around the cluster
        location and within a defined radius.

        :param cluster_location: longitud and latitud of a cluster in the following format:
                                 cluster_location = {
                                 "lng":float(longitude),
                                 "lat":float(latitude)
                                }
        :type cluster_location: dict
        :param radius: Radius delimiting the region of analysis [meters]
        :type radius: int | float
        """
        # TODO: Consider to use a singleton patter no get a db_manager connection
        # TODO: Define where the dispose_engine method will be used
        
        db_manager = DBManager("mysql_db_local")
        params = {
            "radius": radius,
            "lng": cluster_location.get("lng", 0),
            "lat": cluster_location.get("lat", 0),
        }
        query = queries.get_locations_by_cluster.format(**params)
        df = db_manager.select_as_df(query)
        return df