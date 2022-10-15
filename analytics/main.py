import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules.logs.loggers import GeneralLogger
from config.settings import APIREST_PORT,APIREST_HOST, APIREST_CONFIGURATIONS
from modules.apirest.apirest_manager import ApiRestManager

GeneralLogger.setup_logger("Automatic_Medispan_ETL")

def app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(CORSMiddleware,**APIREST_CONFIGURATIONS)
    ApiRestManager.setup()
    app.include_router(ApiRestManager.get_router())
    return app

if __name__ == "__main__":  
    uvicorn.run("main:app", port=APIREST_PORT,host=APIREST_HOST, reload=True, factory=True) 

