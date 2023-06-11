from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField,DateTimeField,TextAreaField,SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired,EqualTo
import datetime

class Loginform(FlaskForm):
    #initialize the form fields with datatypes
    uname = StringField('User Name', validators=[DataRequired()])#,message='Enter valid user'])
    pwd = PasswordField('passwords', validators=[DataRequired(message = "enter password")])
    remember = BooleanField('Remember me')
    

class Signupform(FlaskForm):
    #initialize the form fields with datatypes
    uname = StringField('User Name', validators=[DataRequired()])#,message='Enter valid user'])
    email = StringField('User Email', validators=[DataRequired()])#,message='Enter valid user'])
    pwd = PasswordField('passwords', validators=[DataRequired()])
    cp = PasswordField('confirm password', validators=[DataRequired(),EqualTo('pwd',message = 'passwords must match')])

class Newpwdform(FlaskForm):
    #initialize the form fields with datatypes
    curpwd = PasswordField('Enter current password', validators=[DataRequired()])
    paswrd = PasswordField('Enter New Password', validators=[DataRequired()])
    newpwd = PasswordField('confirm password', validators=[DataRequired(),EqualTo('paswrd',message = 'passwords must match')])


    
def get_id(self):
    return self.uname