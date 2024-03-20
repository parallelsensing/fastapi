from typing import Set, Any, List, Optional
from pydantic import BaseModel,Field
from enum import Enum
from .author import IAuthor

class IArticle(BaseModel):
  doi:str|None = Field(
    default=None,
    title="doi"
  )
  title:str|None = Field(
    default=None,
    title="title"
  )
  abstract:str|None = Field(
    default=None,
    title="abstract"
  )
  graphic:str|None = Field(
    default=None,
    title="graphic"
  )
  earlyAccess:bool|None = Field(
    default=None,
    title="early_access"
  )
  issue_number:int|None = Field(
    default=None,
    title="issue_number"
  )
  html_link:str|None = Field(
    default=None,
    title="html_link"
  )
  show_html:bool|None = Field(
    default=None,
    title="show_html"
  )
  pdfLink:str|None = Field(
    default=None,
    title="pdf_link"
  )
  pdfSize:int|None = Field(
    default=None,
    title="pdf_size"
  )
  read_count:int|None = Field(
    default=None,
    title="read_count"
  )
  citation_count:int|None = Field(
    default=None,
    title="citation_count"
  )
  download_count:int|None = Field(
    default=None,
    title="download_count"
  )
  keywords: Optional[List[str]] = Field(
    default=None,
    title='article keywords'
  )
  authors: Optional[List[IAuthor]] = Field(
    default=None,
    title='article authors'
  )
  orderID: Optional[int] = Field(
    default=None,
    title="buy article order id"
  )


class IArticleAuthor(BaseModel):
  authorID:int|None = Field(
    default=None,
    title="author id"
  )
  articleID:str|None = Field(
    default=None,
    title="article id"
  )
  sequence:int|None = Field(
    default=None,
    title="sequence"
  )


class ISearchType(str, Enum):
  All = 0
  Title = 1
  Author = 2
  Keyword = 3
  Abstract = 4


class IStatusType(str, Enum):
  Draft = 0 # 草稿
  Processing = 1 # 已提交，处理中
  Verifing = 2 # 验证中
  Rejected = 3 # 已驳回
  Verified = 4 # 已审核
  Signed = 5 # 已签署
  Proofed = 6 # 已发表
  Published = 10 # 已发布
  Issue = 21 # 期刊号

  
class ISearch(BaseModel):
  type:ISearchType = Field(
    default=0,
    title="type"
  )
  keyword:str|None = Field(
    default=None,
    title="keyword"
  )


class IAdvancedSearch(BaseModel):
  type:str|None = Field(
    default=None,
    title="type"
  )
  keyword:str|None = Field(
    default=None,
    title="keyword"
  )
  condition:str|None = Field(
    default=None,
    title="condition"
  )




class IPopularType(str, Enum):
  topCited = 'top-cited'
  topDownload = 'top-download'
  topRead = 'top-read'

