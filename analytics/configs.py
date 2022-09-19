from dotenv import load_dotenv
from os import environ, getcwd
from os.path import join, dirname

load_dotenv(join(dirname(getcwd()),".env"))

APIREST_HOST = environ.get("ANALYTICS_HOST_NAME")
APIREST_PORT = int(environ.get("ANALYTICS_HOST_PORT"))


ALLOWED_ORIGINS= {
    f"http://{APIREST_HOST}",
    "http://backend:8080"
    f"http://{APIREST_HOST}:5000",
}


hexaGeojson_file_path = "./json_data/hexaGeojson.json"
hexagons_centers_csv_file_path = "./csv_data/hexagons_centers.csv"