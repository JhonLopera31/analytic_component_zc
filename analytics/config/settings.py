from dotenv import load_dotenv
from os import getcwd, getenv
from os.path import join, dirname
from utils.settings_yaml import load_settings


# Loading .env enviroment variables
load_dotenv(join(dirname(getcwd()), ".env"))


# Logger configuration
LOGGING_SETTINGS = load_settings("config")


# ::::::...... APIREST configurations ......::::::
APIREST_HOST = getenv("ANALYTICS_HOST_NAME")
APIREST_PORT = getenv("ANALYTICS_HOST_PORT")
BACKEND_PORT = getenv("BACKEND_HOST_PORT")
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

# ::::::....... Database connections configs......::::::
DB_CONFIGS = {
    "mysql_db_local": {"engine":"mysql", "credentials_name": "MYSQL_DB_LOCAL"},
    "mongo_db": {"engine": "mongo",  "credentials_name": "MONGO_DB"}
}


# ::::::....... Firebase storage service connection configs ......::::::
FIREBASE_FORECASTING_FOLDER = "forecasting_models"
FIREBASE_CONFIGS = {
    "interperia-test": {"credentials_name": "FIREBASE_INTERPERIA"}
}


# ::::::....... Firebase storage service connection configs ......::::::
ANALYTIC_PROCESSOR = {"run_forecasting"}
