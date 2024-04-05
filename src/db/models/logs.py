"""logs model file"""

from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import mapped_column
from .base import Base


class Logs(Base):
    __tablename__ = "logs"

    time = mapped_column(DateTime, nullable=False)
    level = mapped_column(String(100), nullable=False)
    client_id = mapped_column(Integer, nullable=False)
    role = mapped_column(String(100), nullable=False)
    method = mapped_column(String(150), nullable=False)
    message = mapped_column(String(250), nullable=False)
