from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import base
from src.model.config import config

# "``dialect[+driver]://user:password@host/dbname[?key=value..]``"
engine = create_engine(
    f"{config.DIALECT_DB}+{config.DRIVER_DB}://{config.LOGIN_DB}:{config.PASSWORD_DB}@{config.HOST}:"
    f"{config.PORT}/{config.NAME_DB}",
    echo=True)

print(engine.connect())

if __name__ == "__main__":
    with Session(engine) as session:
        with session.begin():
            base.Base.metadata.create_all(engine)
            # base.Base.metadata.drop_all(engine)
