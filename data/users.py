import sqlalchemy
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin

from datetime import datetime


class User(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    nickname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    create_date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.now())
    orders_count = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    orders_bougth = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    profile_image = sqlalchemy.Column(sqlalchemy.String, default='/static/profile_images/0.jpg')

    purchased_products = orm.relationship('Product')
    products = orm.relationship("Product", back_populates='seller')
    cart = orm.relationship("MultiProduct", back_populates='user')
    comments_for_products = orm.relationship("ProductComment", back_populates='user')
    orders = orm.relationship("Order", back_populates='seller')


    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
