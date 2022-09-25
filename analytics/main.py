import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from configs import APIREST_PORT,APIREST_HOST, apirest_configurations
from modules.apirest_manager import ApiRestManager


def app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(CORSMiddleware,**apirest_configurations)
    ApiRestManager.setup()
    app.include_router(ApiRestManager.get_router())
    return app

if __name__ == "__main__":  
    uvicorn.run("main:app", port=APIREST_PORT,host=APIREST_HOST, reload=True) 

