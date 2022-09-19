import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from configs import ALLOWED_ORIGINS,APIREST_PORT,APIREST_HOST
from analytic_endpoints import AnalyticEndPoints


def app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(
                        CORSMiddleware,
                        allow_origins=ALLOWED_ORIGINS, 
                        allow_credentials=True, 
                        allow_methods=["*"],
                        allow_headers=["*"]
                    )
    AnalyticEndPoints.setup()
    app.include_router(AnalyticEndPoints.get_router())
    return app

if __name__ == "__main__":  
    uvicorn.run("main_v1:app", port=APIREST_PORT,host=APIREST_HOST, reload=True) 

