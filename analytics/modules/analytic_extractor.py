from pandas import DataFrame
from modules.db_manager import DBManager
import queries


class AnalyticExtractor:
    _db_manager = DBManager("mysql_db_local")

    @classmethod
    def extract_location_data(cls, cluster_location: dict, radius: int | float) -> DataFrame:
        """This method is used to extract the coordinates and dates around the cluster 
        location and within a defined radius.

        :param cluster_location: longitud and latitud of a cluster in the following format
                                -> cluster_location = {
                                    "lng":float(longitude),
                                    "lat":float(latitude)
                                    }
        :type cluster_location: dict
        :param radius: Radius delimiting the region of analysis [meters]
        :type radius: int | float
        """
        params = {
            "radius": radius,
            "lng": cluster_location.get("lng", 0),
            "lat": cluster_location.get("lat", 0)
        }
        query = queries.get_locations_by_cluster.format(**params)
        df = cls._db_manager.select_as_df(query)
        return df
