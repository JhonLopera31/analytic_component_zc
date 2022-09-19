from fastapi import APIRouter, Request
from models import Location
from json import load
from pandas import DataFrame, read_csv
from pathlib import Path
import configs


class AnalyticEndPoints:

    _hexagons_center_coordinates = None

    @classmethod
    def setup (cls):
        print (":::..::: Starting Setup for APIREST of Analytic component :::..:::")
        print("* Adding all endpoint to the route attribute")
        cls._router = APIRouter()
        cls._router.add_api_route("/", cls._index_endpoint, methods=["GET"])
        cls._router.add_api_route("/test", cls._test_endpoint, methods=["GET"])
        cls._router.add_api_route("/perform_forecasting", cls._perform_forecasting, methods=["POST"])

        print ("* Generating central coordinates of the hexagons from json file (Temporal method)")
        cls.get_hexagon_centers()
        
  
    @classmethod
    def get_hexagon_centers(cls):
        print("- Check if the csv with the coordinates of the hexagon centers is already created")
        if not Path.exists(Path(configs.hexagons_centers_csv_file_path)):
            print("-- Generating dataframe with coordinates of the hexagon center from json file")
            json_file_path = configs.hexaGeojson_file_path
            json_file = open(json_file_path)
            json_data = load(json_file)
            json_file.close()

            hexagon_centers_lat = [x.get("properties").get("center")[0] for x in json_data]
            hexagon_centers_lng = [x.get("properties").get("center")[1] for x in json_data]

            cls._hexagons_center_coordinates = DataFrame (data={"lat":hexagon_centers_lat, "lng": hexagon_centers_lng})

            cls.create_folder_if_not_exist(Path(configs.hexagons_centers_csv_file_path).parent)
            print(f"-- Saving data in {configs.hexagons_centers_csv_file_path}")
            cls._hexagons_center_coordinates.to_csv(configs.hexagons_centers_csv_file_path, sep=",", index=False)
            
        else:
            print(f"-- Loading data from {configs.hexagons_centers_csv_file_path}")
            cls._hexagons_center_coordinates = read_csv(configs.hexagons_centers_csv_file_path, sep=",")


    @classmethod
    def hexagons_center_coordinates(cls):
        return cls._hexagons_center_coordinates

    @classmethod
    def get_router(cls):
        return cls._router

    @classmethod
    async def _index_endpoint(cls):
        return AnalyticEndPoints.json_message("APIREST is working...")

    @classmethod
    async def _test_endpoint(cls, request: Request):
        message = {"message": "Testing apirest", "host":request.client.host, "method": request.method}
        return message

    @classmethod
    async def _perform_forecasting(cls, location: Location):
        return AnalyticEndPoints.json_message("This is not ready yet.")
    

    @staticmethod
    def json_message(msn:str):
        return {"Message": f"{msn}"}
    
    @staticmethod
    def create_folder_if_not_exist(path):
        print("-- Checking if parent folder already exist.")            
        try:
            path.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            print("--- Folder is already there")
        else:
            print("--- Folder was created")