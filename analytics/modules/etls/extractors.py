from pandas import DataFrame
from modules.repository.db_manager import DBManager
from utils.utility_functions import read_json_file_from
from utils.utility_functions import read_json_file_from
from utils.utility_functions import create_folder_if_not_exist
from pandas import DataFrame, read_csv
from pathlib import Path
from config.settings import CLUSTER_DATA_JSON_PATH
from config.settings import CLUSTER_DATA_CSV_PATH
from modules.etls import queries
from modules.logs.loggers import GeneralLogger

class AnalyticExtractor:
    _db_manager = DBManager("mysql_db_local")
    _cluster_coordinates = None

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
        params = {
            "radius": radius,
            "lng": cluster_location.get("lng", 0),
            "lat": cluster_location.get("lat", 0),
        }
        query = queries.get_locations_by_cluster.format(**params)
        df = cls._db_manager.select_as_df(query)
        return df

    @classmethod
    def extract_cluster_coordinates(cls, extraction_method: str = "apirest"):
        GeneralLogger.put_log("* Getting cluster's coordinates")
        if not Path.exists(Path(CLUSTER_DATA_CSV_PATH)):
            if extraction_method == "local":
                cls._extract_coordinates_from_json_file()
            elif extraction_method == "apirest":
                cls._extract_coordinates_from_apirest()
            else:
                raise Exception("You must provide a correct extraction method")

        else:
            print(f"-- Loading data from {CLUSTER_DATA_CSV_PATH}")
            cls._cluster_coordinates = read_csv(CLUSTER_DATA_CSV_PATH, sep=",")
            print("Extraction finished succesfully...")

    @classmethod
    def _extract_coordinates_from_json_file(cls):
        print("-- Generating data from json file (Temporal method)")
        json_data = read_json_file_from(CLUSTER_DATA_JSON_PATH)

        data = {
            "lat": [x.get("properties").get("center")[0] for x in json_data],
            "lng": [x.get("properties").get("center")[1] for x in json_data],
        }

        save_path = CLUSTER_DATA_CSV_PATH
        create_folder_if_not_exist(Path(save_path).parent)
        print(f"-- Saving data in {save_path}")
        cls._cluster_coordinates = DataFrame(data)
        cls._cluster_coordinates.to_csv(save_path, sep=",", index=False)

    @classmethod
    def _extract_coordinates_from_apirest(cls):
        # Introduce some logic
        pass

    @classmethod
    def get_cluster_coordinates(cls):
        return cls._cluster_coordinates
