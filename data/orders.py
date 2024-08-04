import sqlalchemy
from .db_session import SqlAlchemyBase

from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from datetime import datetime


class Order(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'orders'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    nickname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    status = sqlalchemy.Column(sqlalchemy.String, default="Оформлен")
    create_time = sqlalchemy.Column(sqlalchemy.String, default=datetime.now())
    point = sqlalchemy.Column(sqlalchemy.String)
    seller_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    storage = sqlalchemy.Column(sqlalchemy.Integer)

    seller = orm.relationship('User')
    products = orm.relationship('MultiProduct', back_populates='order')
    
