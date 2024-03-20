# test for first git commit
from typing import Set,TYPE_CHECKING, List
from datetime import datetime
from sqlalchemy import Column, Integer, Table, String, ARRAY, TIMESTAMP, sql, Text, Boolean, ForeignKey, event, asc
from sqlalchemy.orm import relationship, Mapped, column_property
from sqlalchemy.ext.hybrid import hybrid_property
from app.db.base import Base, Common, Clock

# if TYPE_CHECKING:
if TYPE_CHECKING:
  from .author import Author

class ArticleKeyword(Base):
  article_id = Column(Integer, ForeignKey("article.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
  keyword = Column(String, primary_key=True)
  sequence = Column(Integer, default=0)



class UserArticle(Base):
  articleID = Column("article_id", Integer, ForeignKey("article.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
  userID = Column("user_id", Integer, primary_key=True)
  article = relationship("Article", back_populates="userArticle", foreign_keys=[articleID], primaryjoin="Article.id==UserArticle.articleID")


class Article(Base, Common):
  doi = Column(String(200), nullable=False)
  title = Column(Text, nullable=False)
  abstract = Column(Text, nullable=False)
  keywords = Column(ARRAY(String), nullable=False)
  graphic = Column(Text, nullable=False)
  earlyAccess = Column("early_access", Boolean, default=False)
  htmlLink = Column("html_link", String(200), nullable=False)
  showHtml = Column("show_html", Boolean, default=True)
  pdfLink = Column("pdf_link", String(200), nullable=False)
  pdfSize = Column("pdf_size", Integer, default=0)
  pdfEdition = Column("pdf_edition", String(200), nullable=False)
  readCount = Column("read_count", Integer, default=0)
  citationCount = Column("citation_count", Integer, default=0)
  downloadCount = Column("download_count", Integer, default=0)
  status = Column(Integer, default=0)
  orderID = Column("order_id", Integer, nullable=True)
  articleAuthors:Mapped[List["ArticleAuthor"]] = relationship('ArticleAuthor', back_populates="article", order_by="ArticleAuthor.sequence == 0, ArticleAuthor.sequence")
  userArticle:Mapped["UserArticle"] = relationship('UserArticle', uselist=False, back_populates="article", primaryjoin="Article.id==UserArticle.articleID")



class ArticleAuthor(Base):
  articleID = Column("article_id", Integer, ForeignKey("article.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
  authorID = Column("author_id", Integer, ForeignKey("author.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
  sequence = Column(Integer, default=0)
  article = relationship(Article, back_populates="articleAuthors", foreign_keys=[articleID])
  author:Mapped["Author"] = relationship("Author", foreign_keys=[authorID])
