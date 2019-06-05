from flask_wtf import FlaskForm
from wtforms import (SelectField, IntegerField, SubmitField, PasswordField,
                     BooleanField, StringField)
from wtforms.validators import NumberRange
from flask_wtf.file import FileField, FileRequired, FileAllowed
from CIS.models import User
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError


class AlgorithmForm(FlaskForm):
    algorithm = SelectField('Algorithm', choices=[
        ('K-Means', 'K-Means'), ('FCM', 'FCM'),
        ('PFCM', 'PFCM'), ('VIBGYOR', 'VIBGYOR')])
    clusters = IntegerField(
        'Number Of Clusters', validators=[NumberRange(min=2)], default=2)
    colors = SelectField('Color to Extract', choices=[
        ('v', 'Violet'), ('i', 'Indigo'), ('b', 'Blue'),
        ('g', 'Green'), ('y', 'Yellow'), ('o', 'Orange'), ('r', 'Red')],
            default='v')
    image = FileField('Choose an Input Image', validators=[
        FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'bmp'])])
    run = SubmitField('Run')


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose another one.')


class LoginForm(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
