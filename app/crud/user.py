from typing import Any, Dict, Optional, Union
from datetime import datetime, timedelta
from sqlalchemy.orm import Session, selectinload

from app.core.security import get_password_hash, verify_password
from .author import author as AuthorCRUD
from app.crud.base import CRUDBase
from app.models import Author, User
from app.schemas import IAccount, ICreateAccount, IAdminStatusType, IUserSearch, IAuthor


class CRUDUser(CRUDBase[User, IAccount, ICreateAccount]):
  def get_info(self, db: Session, id: int) -> Optional[User]:
    return {"id":id}
  
  def search(self, db: Session, params: IUserSearch) -> Any:
    query = db.query(User).options(selectinload(User.author), selectinload(User.role)).where(User.isActive == True, User.authorID != None)
    if params:
      for key, value in params:
        if value and key == "email":
          query = query.where(User.email.ilike(f'%{value}%'))
        elif value and key == "exclude":
          query = query.where(User.id != value)
        elif value and key == "privileges":
          query = query.join(User.role).where(Role.privileges.op('@>')(value))
    print(query)
    return query.limit(200).all()

  def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

  def get_full_info(self, db: Session, id: int) -> Optional[User]:
    return db.query(User).options(
      selectinload(User.author).options(selectinload(Author.institutions)),
      selectinload(User.role)
    ).filter(User.id == id).first()

  def create(self, db: Session, *, obj_in: ICreateAccount) -> User:
    db_obj = User(
      email=obj_in.email,
      password=get_password_hash(obj_in.password),
      updatedAt=datetime.now()
    )
    author = AuthorCRUD.get_by_email(db, email=obj_in.email)
    if(author):
      db_obj.author = author
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
  
  def create_reviewer(self, db: Session, *, obj_in: IAuthor) -> User:
    author = AuthorCRUD.get_by_email(db, email=obj_in.email)
    if author:
      pass
    else:
      author = Author(firstName=obj_in.firstName, lastName=obj_in.lastName, email=obj_in.email, zones=[])
    db_obj = User(
      email=obj_in.email,
      password=get_password_hash('Agist2024'),
      author=author,
      updatedAt=datetime.now()
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

  def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
    user = self.get_by_email(db, email=email)
    if not user:
      return None
    if not verify_password(password, user.password):
      return None
    return user
  
  def change_password(self, db: Session, *, id: int, password: str) -> Optional[User]:
    db_obj = self.get(db, id=id)
    if not db_obj:
      return None
    obj_in = IAccount(password=get_password_hash(password), updatedAt=datetime.now())
    return self.update(db, db_obj=db_obj, obj_in=obj_in)



user = CRUDUser(User)
