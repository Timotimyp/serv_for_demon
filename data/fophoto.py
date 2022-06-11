import sqlalchemy
from .db_session import SqlAlchemyBase


class Form_photo(SqlAlchemyBase):
    __tablename__ = 'photos'
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    form_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    photo = sqlalchemy.Column(sqlalchemy.Text, nullable=False)