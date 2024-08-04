import sqlalchemy
from .db_session import SqlAlchemyBase

from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin

from datetime import datetime


class Product(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    seller_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.now())
    sells_count = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    category = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='blocks')
    status = sqlalchemy.Column(sqlalchemy.Integer)
    count = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    photos = orm.relationship('Photo', back_populates='product')
    comments = orm.relationship('ProductComment', back_populates='product')
    seller = orm.relationship('User')