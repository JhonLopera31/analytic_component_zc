from fastapi import APIRouter
from modules.apirest_endpoints import AnalyticEndPoints
from utils.utility_functions import create_folder_if_not_exist, read_json_file_from
from pandas import DataFrame, read_csv
from pathlib import Path
import configs


class ApiRestManager:
    _router = None
    _hexagons_center_coordinates = None

    @classmethod
    def setup(cls) -> None:
        print(":::..::: Starting Setup for APIREST of Analytic component :::..:::")
        cls._setup_router()
        cls._setup_hexagons_file()

    @classmethod
    def _setup_router(cls) -> None:
        print("* Adding all endpoints to 'router' attribute")
        cls._router = APIRouter()
        cls._router.add_api_route(**AnalyticEndPoints.get_index_endpoint())
        cls._router.add_api_route(**AnalyticEndPoints.get_forecasting_endpoint())
        cls._router.add_api_route(**AnalyticEndPoints.get_test_endpoint())
        print("Done..")

    @classmethod
    def _setup_hexagons_file(cls):
        print("* Getting central coordinates of the hexagons")

        if not Path.exists(Path(configs.hexagons_centers_csv_file_path)):
            print("-- Generating data from json file (Temporal method)")
            json_file_path = configs.hexagons_geometry_data_file_path
            json_data = read_json_file_from(json_file_path)

            data = {
                "lat": [x.get("properties").get("center")[0] for x in json_data],
                "lng": [x.get("properties").get("center")[1] for x in json_data]
            }

            cls._hexagons_center_coordinates = DataFrame(data=data)

            save_path = configs.hexagons_centers_csv_file_path
            create_folder_if_not_exist(Path(save_path).parent)
            print(f"-- Saving data in {save_path}")
            cls._hexagons_center_coordinates.to_csv(save_path, sep=",", index=False)

        else:
            print(f"-- Loading data from {configs.hexagons_centers_csv_file_path}")
            cls._hexagons_center_coordinates = read_csv(configs.hexagons_centers_csv_file_path, sep=",")
        print("Done..")

    @classmethod
    def hexagons_center_coordinates(cls):
        return cls._hexagons_center_coordinates

    @classmethod
    def get_router(cls):
        return cls._router
