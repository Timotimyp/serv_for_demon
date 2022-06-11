import sqlalchemy
from .db_session import SqlAlchemyBase


class Form_video(SqlAlchemyBase):
    __tablename__ = 'video'
    id  = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    form_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    video = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
