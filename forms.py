from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField


class MyUpdateImageForm(FlaskForm):
    image = FileField('image')
    submit = SubmitField('Обновить')
