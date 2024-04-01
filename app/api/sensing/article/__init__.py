from typing import Any, Annotated
from os import path, makedirs, remove
from mimetypes import guess_extension
from urllib.parse import unquote
from fastapi import Depends, APIRouter, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.schemas import IResponse, IPopularType, ISearchType, IAdvancedSearch
from app.models import User
from app.api import deps
from app import crud
from app.core.config import settings

from .author import router as author_router

router = APIRouter()

router.include_router(author_router, prefix='/author')

@router.get("/list", response_model=IResponse)
def articles(
  db:Session = Depends(deps.get_db)
) -> Any:
  res = IResponse()
  res.data = crud.article.get_list(db)
  return res


@router.get("/search", response_model=IResponse)
def search(
  keyword:str,
  type:ISearchType = ISearchType.All,
  db:Session = Depends(deps.get_db)
) -> Any:
  res = IResponse()
  res.data = crud.article.search(db, keyword, type)
  return res


@router.post("/search", response_model=IResponse)
def advanced_search(
  arr: list[IAdvancedSearch],
  db:Session = Depends(deps.get_db)
) -> Any:
  res = IResponse()
  res.data = crud.article.advanced_search(db, arr)
  return res

@router.get("/early-access", response_model=IResponse)
def early_access(
  db:Session = Depends(deps.get_db)
) -> Any:
  res = IResponse()
  res.data = crud.article.early_access(db)
  return res





@router.get("/download/{article_id}")
def download(
  article_id:int,
  db:Session = Depends(deps.get_db),
) -> Any:
  article = crud.article.get(db, article_id)
  filename = path.basename(article.pdfLink)
  filepath = f"{settings.FILES_DIR}/{article.pdfLink}"
  crud.article.download(db, article_id)
  return FileResponse(
    path=filepath,
    media_type="application/pdf",
    filename=filename
  )

@router.get("/browse/{article_id}")
def download(
  article_id:int,
  db:Session = Depends(deps.get_db),
) -> Any:
  article = crud.article.get(db, article_id)
  if article.pdfEdition:
    filepath = f"{settings.FILES_DIR}/{article.pdfEdition}"
  else:
    filepath = f"{settings.FILES_DIR}/{article.pdfLink}"

  with open(filepath, "rb") as file:
    pdf_data = file.read()
  crud.article.read(db, article_id)
  response = Response(content=pdf_data)
  response.headers["Content-Type"] = "application/pdf"

  return response

@router.get("/edition/{article_id}")
def download(
  article_id:int,
  db:Session = Depends(deps.get_db),
) -> Any:
  article = crud.article.get(db, article_id)
  if article.pdfEdition:
    filepath = f"{settings.FILES_DIR}/{article.pdfEdition}"
  else:
    filepath = f"{settings.FILES_DIR}/{article.pdfLink}"

  with open(filepath, "rb") as file:
    pdf_data = file.read()
  response = Response(content=pdf_data)
  response.headers["Content-Type"] = "application/pdf"

  return response


