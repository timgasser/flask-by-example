from flask_wtf import Form
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from wtforms import TextField

class RegistrationForm(Form):
    email = EmailField('email', 
                       validators=[validators.DataRequired(),
                                   validators.Email()])
    password = PasswordField('password',
                             validators=[validators.DataRequired(),
                                         validators.Length(min=8, message="Minimum length 8 characters")])

    password2 = PasswordField('password2',
                              validators=[validators.DataRequired(),
                                          validators.EqualTo('password', message="Passwords must match")])

    submit = SubmitField('submit', 
                          validators=[validators.DataRequired()])

class LoginForm(Form):
    email = EmailField('email', validators=[validators.DataRequired(),
                                                 validators.Email()])

    password = PasswordField('password',
                             validators=[validators.DataRequired("Password field is required")])

    submit = SubmitField('submit', 
                        validators=[validators.DataRequired()])

class CreateTableForm(Form):
    tablenumber = TextField('tablenumber', validators=[validators.DataRequired()])
    submit = SubmitField('submit', validators=[validators.DataRequired()])