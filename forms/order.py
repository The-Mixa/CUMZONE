from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms import SelectField


class OrderForm(FlaskForm):
    point = SelectField('Категория', validators=[DataRequired()], choices=[('Спавн', 'Спавн'),
                                                                           ('Кримпай Сити', 'Кримпай Сити')])
    submit = SubmitField('Оформить')
