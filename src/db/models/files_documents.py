"""files_documents model file"""

from sqlalchemy import Integer, LargeBinary, ForeignKey
from sqlalchemy.orm import mapped_column
from .base import Base


class FilesDocuments(Base):
    __tablename__ = "files_documents"

    id = mapped_column(Integer, ForeignKey("data_about_documents.id", ondelete='CASCADE'), primary_key=True)
    file = mapped_column(LargeBinary, nullable=False)
