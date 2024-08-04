import sqlalchemy
from .db_session import SqlAlchemyBase

from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from datetime import datetime


# id, путь до файла, id игры
class ProductComment(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'product_comments'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    product_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('products.id'))
    create_date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.now())
    
    user = orm.relationship('User')
    product = orm.relationship('Product')
