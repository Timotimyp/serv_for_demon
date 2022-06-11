import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    chat_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, primary_key=True)
    sex = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    now_search = sqlalchemy.Column(sqlalchemy.String)
    search_count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)