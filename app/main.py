from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from app.api import sensing


app = FastAPI()




router = APIRouter()
router.include_router(sensing.item, prefix="/item", tags=["sensing", "item"])
router.include_router(sensing.user, prefix="/user", tags=["sensing", "user"])


app.include_router(router, prefix="/api/sensing", tags=["sensing"])

