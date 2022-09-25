from dotenv import load_dotenv
from os import environ, getcwd
from os.path import join, dirname

load_dotenv(join(dirname(getcwd()), ".env"))

APIREST_HOST = int(environ.get("ANALYTICS_HOST_NAME"))
APIREST_PORT = int(environ.get("ANALYTICS_HOST_PORT"))


ALLOWED_ORIGINS = {
    f"http://{APIREST_HOST}",
    "http://backend:8080"
    f"http://{APIREST_HOST}:5000",
}


apirest_configurations = {
    "allow_origins": ALLOWED_ORIGINS,
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"]
}


hexagons_geometry_data_file_path = "./data/json_data\hexagonsGeometryData.json"
hexagons_centers_csv_file_path = "./data/csv_data/hexagons_centers.csv"
