from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed
from wtforms import SelectField


class ProductForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    price = IntegerField('Цена в алмазах', validators=[DataRequired()])
    count = IntegerField('Количество товара', validators=[DataRequired()])
    category = SelectField('Категория', validators=[DataRequired()], choices=[('block', 'Строительные блоки'),
                                                                              ('resource', 'Ресурсы'),
                                                                              ('building', 'Постройка'),
                                                                              ('job', 'Работа'),
                                                                              ('other', 'другое')])
    screenshots = MultipleFileField('Скриншоты',
                                    validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Только изображения!')])
    submit = SubmitField('Опубликовать')
