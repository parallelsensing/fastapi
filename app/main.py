from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from app.api import sensing
from app.core.database import Base, engine
from app.models import Item as ItemModel
from app.models import User as UserModel


app = FastAPI()
# Base.metadata.create_all(bind=engine)



router = APIRouter()
router.include_router(sensing.item, prefix="/item", tags=["sensing", "item"])
router.include_router(sensing.user, prefix="/user", tags=["sensing", "user"])


app.include_router(router, prefix="/api/sensing", tags=["sensing"])