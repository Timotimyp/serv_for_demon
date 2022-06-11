import sqlalchemy
from .db_session import SqlAlchemyBase


class Category(SqlAlchemyBase):
    __tablename__ = 'category'
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, primary_key=True)
    forms_id = sqlalchemy.Column(sqlalchemy.Text, nullable=False)