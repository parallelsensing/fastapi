from typing import Any, Union
from urllib.parse import unquote
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.schemas import IResponse,  IUser, IAuthor
from app.models import User
from app.api import deps
from app import crud


router = APIRouter()


@router.get("/search", response_model=IResponse)
def authors(
  keyword: str = None,
  db:Session = Depends(deps.get_db)
) -> Any:
  res = IResponse()
  res.data = crud.author.search(db, keyword=keyword)
  return res

@router.get("/valid_email", response_model=IResponse)
def authors(
  email: str = None,
  db:Session = Depends(deps.get_db)
) -> Any:
  res = IResponse()
  author = crud.author.get_by_email(db, email=email)
  if author:
    res.data = author.id or None
  return res

@router.get("/zones", response_model=IResponse)
def zones(
  keyword: str = None,
  db:Session = Depends(deps.get_db)
) -> Any:
  res = IResponse()
  res.data = crud.author.zones(db, keyword=keyword)
  return res

@router.get("/institutions", response_model=IResponse)
def institutions(
  keyword: str = None,
  db:Session = Depends(deps.get_db)
) -> Any:
  res = IResponse()
  res.data = crud.institution.search(db, keyword=keyword)
  return res

@router.get("/{id}", response_model=IResponse)
def author(
  id: int,
  db:Session = Depends(deps.get_db)
) -> Any:
  res = IResponse()
  res.data = crud.author.get_single_full(db, id=id)
  return res

@router.post("/", response_model=IResponse)
def author_create(
  req: IAuthor,
  db:Session = Depends(deps.get_db),
  current_user:User = Depends(deps.get_current_user)
) -> Any:
  res = IResponse()
  req.createdUserID = current_user.id
  author = crud.author.create(db, obj_in=req)
  # crud.user.update(db, db_obj= current_user, obj_in=IUser(authorID=author.id))
  res.data = author
  return res

@router.put("/{id}", response_model=IResponse)
def author_update(
  req:IAuthor,
  id: Union[int, None] = None,
  db:Session = Depends(deps.get_db),
  current_user:User = Depends(deps.get_current_user)
) -> Any:
  # if not current_user.isAdmin:
  #   raise HTTPException(status_code=401, detail="Must be a admin to operate")
  req.updatedUserID = current_user.id
  db_obj = crud.author.get(db, id=id)
  if not db_obj:
    raise HTTPException(status_code=404, detail='There no Data of this ID')
  if db_obj.user and db_obj.user.id != current_user.id:
    raise HTTPException(status_code=403, detail='Author of User can not be modified by other User')
  author = crud.author.update(db, db_obj=db_obj, obj_in=req)
  res = IResponse()
  res.data = author
  return res

@router.put("/", response_model=IResponse)
def author_self_update(
  req:IAuthor,
  db:Session = Depends(deps.get_db),
  current_user:User = Depends(deps.get_current_user)
) -> Any:
  db_obj = crud.author.get(db, id=current_user.authorID)
  if not db_obj:
    raise HTTPException(status_code=404, detail='There no Data of this ID')
  req.updatedUserID = current_user.id
  author = crud.author.update(db, db_obj=db_obj, obj_in=req)
  res = IResponse()
  res.data = author
  return res