from dotenv import load_dotenv
from os import environ, getcwd, getenv
from os.path import join, dirname

load_dotenv(join(dirname(getcwd()), ".env"))

# ::::::...... APIREST configurations ......::::::
APIREST_HOST = getenv("ANALYTICS_HOST_NAME")
APIREST_PORT = int(getenv("ANALYTICS_HOST_PORT"))
BACKEND_PORT = int(getenv("BACKEND_HOST_PORT"))
ALLOWED_ORIGINS = {
    f"http://{APIREST_HOST}",
    f"http://{BACKEND_PORT}:8080"
    f"http://{APIREST_HOST}:5000",
}

APIREST_CONFIGURATIONS = {
    "allow_origins": ALLOWED_ORIGINS,
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"]
}


# ::::::....... Configurations to obtain data (Temporary Methods)  ......::::::
hexagons_geometry_data_file_path = "./data/json_data\hexagonsGeometryData.json"
hexagons_centers_csv_file_path = "./data/csv_data/hexagons_centers.csv"

DB_CONFIGS = {
    "mysql_db_local": {"engine":"mysql", "credentials_name": "MYSQL_DB_LOCAL"}
}