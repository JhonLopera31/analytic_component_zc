from uvicorn import run
from fastapi import FastAPI
from modules.logs.loggers import GeneralLogger
from config.settings import APIREST_PORT, APIREST_HOST
from modules.apirest.apirest_manager import ApiRestManager
from dotenv import load_dotenv
from os import getenv

load_dotenv(".env")


def app() -> FastAPI:
    GeneralLogger.setup_logger(f"Analityc component {getenv('EXECUTION_ENV')}")
    return ApiRestManager.setup()

if __name__ == "__main__":  
    run("main:app", port=int(APIREST_PORT),host=APIREST_HOST, reload=True, factory=True)
 