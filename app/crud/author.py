from typing import Any, Dict, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import func, inspect
from app.crud.base import CRUDBase
from app.models import Author, Institution, Zone
from app.schemas import IAuthor, IInstitution
from app.utils.tools import get_obj_from_list

class CRUDAuthor(CRUDBase[Author, IAuthor, IAuthor]):
  def search(self, db: Session, *, keyword: str) -> Optional[Author]:
    query = db.query(Author).options(
      selectinload(Author.institutions)
    )
    if keyword:
      query = query.filter(Author.email.like(f'%{keyword}%'))
    return query.limit(200).all()

  def zones(self, db: Session, *, keyword: str) -> Optional[Author]:
    query = db.query(Zone)
    if keyword:
      query = query.filter(Zone.name.like(f'%{keyword}%'))
    return query.limit(200).all()

  def get_single_full(self, db:Session, *, id:Any) -> Optional[Author]:
    """
    got origin data
    """
    return db.query(Author).options(selectinload(Author.institutions)).filter(Author.id == id).first()

  def get_by_email(self, db: Session, *, email: str) -> Optional[Author]:
    return db.query(Author).filter(Author.email == email).first()



  def create(self, db: Session, *, obj_in: IAuthor) -> Author:
    db_obj = Author(
      email=obj_in.email,
      firstName=obj_in.firstName,
      lastName=obj_in.lastName,
      zones=obj_in.zones,
      # institutions=obj_in.institutions,
      updatedAt=datetime.now()
    )
    institutions = []
    if obj_in.institutions is not None:
      for institution in obj_in.institutions:

        refer = None
        if 'id' in institution:
          # if institution from obj_in has id, means modify institution
          refer = get_obj_from_list(db_obj.institutions, institution['id'])
          if refer is not None:
            # if id does not exist in origin data, means insert new institution
            for field in refer.__dict__.keys():
              if field in institution:
                setattr(refer, field, institution[field])
          else:
            institution['id'] = None
        if refer is None:
          # if institution from obj_in has not id, means insert new institution
          refer = Institution()
          for attr_name, attr_value in institution.dict().items():
            setattr(refer, attr_name, attr_value)
          max_id = db.query(func.max(Institution.id)).scalar() or 0
          refer.id = max_id + 1
        institutions.append(refer)
      db_obj.institutions = institutions
      # model_instance = Institution()
      # for attr_name, attr_value in institution.dict().items():
      #   if attr_name != '__class__' and attr_value:
      #     setattr(model_instance, attr_name, attr_value)
      # db_obj.institutions.append(model_instance)
    max_id = db.query(func.max(Author.id)).scalar() or 0
    db_obj.id = max_id + 1
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


  def update(self, db:Session, *, db_obj:Author, obj_in:IAuthor) -> Author:
    for attr, value in obj_in.dict(exclude_unset=True).items():
      if value is not None:
        if attr == 'institutions': # put data to institution model
          institutions = []
          for institution in value:
            refer = None
            if 'id' in institution:
              # if institution from obj_in has id, means modify institution
              refer = get_obj_from_list(db_obj.institutions, institution['id'])
              if refer is not None:
                # if id does not exist in origin data, means insert new institution
                for field in refer.__dict__.keys():
                  if field in institution:
                    setattr(refer, field, institution[field])
              else:
                institution['id'] = None
            if refer is None:
              # if institution from obj_in has not id, means insert new institution
              refer = Institution()
              for attr_name, attr_value in institution.items():
                setattr(refer, attr_name, attr_value)
              max_id = db.query(func.max(Institution.id)).scalar() or 0
              refer.id = max_id + 1
            institutions.append(refer)
          db_obj.institutions = institutions
        else:
          setattr(db_obj, attr, value) # set old data new value
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

author = CRUDAuthor(Author)
