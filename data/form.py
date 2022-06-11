import sqlalchemy
from .db_session import SqlAlchemyBase


class Form(SqlAlchemyBase):
    __tablename__ = 'forms'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    chat_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    telephone = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    category = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
