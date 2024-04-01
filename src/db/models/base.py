"""admins_data model file"""
from sqlalchemy import Integer
from sqlalchemy.orm import as_declarative, mapped_column


@as_declarative()
class Base:
    id = mapped_column(Integer, autoincrement=True, primary_key=True)

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
