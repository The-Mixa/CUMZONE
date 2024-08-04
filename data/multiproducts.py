import sqlalchemy
from .db_session import SqlAlchemyBase

from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class MultiProduct(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'multiproducts'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    product_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('products.id'))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    order_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('orders.id'))

    order = orm.relationship('Order')    
    user = orm.relationship('User')
    product = orm.relationship('Product')



