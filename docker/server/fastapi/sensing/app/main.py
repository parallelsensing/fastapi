from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import sensing
import asyncio
from app.jobs import jobs_run



app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
  CORSMiddleware,
  allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


router = APIRouter()
router.include_router(sensing.article, prefix="/article", tags=["cpsi", "article"])
router.include_router(sensing.user, prefix="/user", tags=["cpsi", "user"])

app.include_router(router, prefix=settings.API_PATH, tags=["cpsi"])




@app.on_event("startup")
async def startup_event():
  asyncio.create_task(jobs_run())
