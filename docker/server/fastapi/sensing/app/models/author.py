from typing import Set,TYPE_CHECKING
from sqlalchemy import Column, Integer, Table, String, ForeignKey, event, ARRAY
from sqlalchemy.orm import relationship, Mapped
from app.db.base import Base, Common
from app.schemas import IAuthor
from .user import User
from .institution import Institution
  
author_institution_table = Table('author_institution', Base.metadata,
  Column('author_id', Integer, ForeignKey('author.id'), primary_key=True),
  Column('institution_id', Integer, ForeignKey('institution.id'), primary_key=True),
  Column('sequence', Integer, default=0)
)

class Author(Base, Common):
  id = Column(Integer, primary_key=True, autoincrement=True)
  email = Column(String(200), nullable=False)
  orcid = Column(String(200), nullable=True)
  firstName = Column("first_name", String(200), nullable=False)
  lastName = Column("last_name", String(200), nullable=False)
  zones = Column(ARRAY(String), nullable=False)

  updatedUserID = Column("updated_user_id", Integer)
  createdUserID = Column("created_user_id", Integer)
  @property
  def fullName(self):
    return f"{self.firstName} {self.lastName}"

  institutions = relationship(Institution, secondary=author_institution_table)
  user:Mapped["User"] = relationship("User", uselist=False, back_populates="author")

  def jsonable_encoder(cls, **kwargs):
    values = super().jsonable_encoder(**kwargs)
    values['institutions'] = cls.institutions
    return values
  def to_model(self):
    return IAuthor(id=self.id, email=self.email, institutions=self.institutions)


# 监听 Author 模型的 after_insert 事件
@event.listens_for(Author, 'after_insert')
def after_author_insert(mapper, connection, target):
  # 更新相关的 User 记录的 author_id
  connection.execute(
    User.__table__.update()
    .where(User.authorID.is_(None))
    .where(User.email == target.email)
    .values(author_id=target.id)
  )


class Zone(Base, Common):
  name = Column(String(200), nullable=False)

