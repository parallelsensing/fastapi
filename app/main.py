from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from app.api import sensing
from app.core.database import Base, engine
from app.models import Item as ItemModel
from app.models import User as UserModel
from app.core.config import settings
from fastapi.staticfiles import StaticFiles

app = FastAPI()
Base.metadata.create_all(bind=engine)



router = APIRouter()
router.include_router(sensing.item, prefix="/item", tags=["sensing", "item"])
router.include_router(sensing.user, prefix="/user", tags=["sensing", "user"])
router.include_router(sensing.image, prefix="/image", tags=["sensing", "image"])


app.mount("/images", StaticFiles(directory=settings.IMAGE_DIR), name="images")
app.include_router(router, prefix="/api/sensing", tags=["sensing"])