import sqlalchemy
from .db_session import SqlAlchemyBase


class User_maker(SqlAlchemyBase):
    __tablename__ = 'user_maker'
    chat_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    now_red = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)