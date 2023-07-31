from fastapi import FastAPI
from core.config import settings
from core.celery_config import create_celery_app
#from apis.general_pages.route_homepage import general_pages_router

from db.sessions import engine
from db.base import Base
from apis.base import api_router

# for routers

def include_router(app):   
	app.include_router(api_router) 
# for database
def create_tables():
    Base.metadata.create_all(bind=engine)

def start_application():
    app = FastAPI(title= settings.PROJECT_NAME, version= settings.PROJECT_VERSION)
    include_router(app)
    create_tables()
    return app

app =start_application()

# create an instance of celery app
celery_app = create_celery_app()