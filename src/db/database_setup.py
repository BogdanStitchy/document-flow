from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from .models import base
from src.config import config

# "``dialect[+driver]://user:password@host/dbname[?key=value..]``"
engine = create_engine(
    f"{config.DIALECT_DB}+{config.DRIVER_DB}://{config.LOGIN_DB}:{config.PASSWORD_DB}@{config.HOST}:"
    f"{config.PORT}/{config.NAME_DB}",
    echo=True)


def set_new_engine(new_engine: create_engine):
    global engine
    engine = new_engine


def get_engine() -> create_engine:
    global engine
    return engine


session_factory = sessionmaker(get_engine())

if __name__ == "__main__":
    with Session(engine) as session_factory:
        with session_factory.begin():
            base.Base.metadata.create_all(engine)
            # base.Base.metadata.drop_all(engine)
