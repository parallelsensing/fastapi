from typing import Any, Dict, Optional, List
from datetime import datetime, timedelta
from sqlalchemy import or_, join
from sqlalchemy.orm import Session, selectinload,joinedload,subqueryload
from sqlalchemy.sql import update, func
from sqlalchemy.ext.hybrid import hybrid_property
from fastapi.encoders import jsonable_encoder
from app.crud.base import CRUDBase
from app.models import Article, UserArticle, Author, ArticleAuthor
from app.schemas import IArticle, IStatusType, ISearchType, IAdvancedSearch
from app.core.config import settings

class CRUDArticle(CRUDBase[Article, IArticle, IArticle]):

  def get_list(self, db: Session) -> Optional[Article]:
    arr = db.query(Article) \
      .where(Article.status == IStatusType.Published, Article.earlyAccess==False) \
      .all()
    return arr
  

  def search(self, db: Session, keyword:str, type:ISearchType) -> Article:
    query = db.query(Article).where(Article.status == IStatusType.Published)
    param = f'%{keyword}%'
    filter_condtion = or_(
      Article.title.ilike(param),
      Article.articleAuthors.any(ArticleAuthor.author.has(
        or_(Author.firstName.ilike(param), Author.lastName.ilike(param), Author.email.ilike(param))
      )),
      func.array_to_string(Article.keywords, ',').contains(keyword),
      Article.abstract.ilike(param)
    )
    if type == ISearchType.Title:
      filter_condtion = Article.title.ilike(param)
    elif type == ISearchType.Author:
      filter_condtion = Article.articleAuthors.any(ArticleAuthor.author.has(
        or_(Author.firstName.ilike(param), Author.lastName.ilike(param), Author.email.ilike(param))
      ))
    elif type == ISearchType.Keyword:
      filter_condtion = func.array_to_string(Article.keywords, ',').contains(keyword)
    elif type == ISearchType.Abstract:
      filter_condtion = Article.abstract.ilike(param)
    query = query.where(filter_condtion)
    return query.all()

  def advanced_search(self, db: Session, arr: list[IAdvancedSearch]) -> Article:
    query = db.query(Article).where(Article.status == IStatusType.Published)
    query.where(Article.title.contains(arr[0].keyword))
    return query.all()

  def early_access(self, db: Session) -> Article:
    return db.query(Article).where(Article.earlyAccess==True).all()


  
  def read(self, db: Session, article_id: int) -> Article:
    db_obj = super().get(db, id=article_id)
    db_obj.readCount += 1
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
  
  def download(self, db: Session, article_id: int) -> Article:
    db_obj = super().get(db, id=article_id)
    db_obj.downloadCount += 1
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
    


  def remove(self, db: Session, *, db_obj: Article) -> Article:
    db.delete(db_obj)
    db.commit()
    return db_obj

article = CRUDArticle(Article)
