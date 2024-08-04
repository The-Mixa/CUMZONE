from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, IntegerField, SubmitField, EmailField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed


# регистрация пользователя
# почта, пароль, имя, фамилия, никнейм, аватар
class RegisterForm(FlaskForm):
    nickname = StringField('Никнейм', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')
    profile_image = FileField('Аватар профиля', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Только изображения!')])


class EditForm(FlaskForm):
    nickname = StringField('Никнейм', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')
    profile_image = FileField('Аватар профиля', validators=[
                              FileAllowed(['jpg', 'png', 'jpeg'], 'Только изображения!')])
