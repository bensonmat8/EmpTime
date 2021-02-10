from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class SignupForm(FlaskForm):
    empid = StringField('EmpId', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Name', validators=[DataRequired(),
                                            Email(message='Enter Valid Email.')])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=6,
                                                            message='Select stronger password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    empid = StringField('EmpID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
