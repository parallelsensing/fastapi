from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models import Institution
from app.schemas import IInstitution

class CRUDInstitution(CRUDBase[Institution, IInstitution, IInstitution]):
  def search(self, db: Session, *, keyword: str) -> Optional[Institution]:
    query = db.query(Institution)
    if keyword:
      query = query.filter(Institution.institution.like(f'%{keyword}%'))
    return query.limit(20).all()

institution = CRUDInstitution(Institution)
