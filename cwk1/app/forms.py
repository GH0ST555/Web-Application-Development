from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField,DateTimeField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,Length
import datetime

class AssesmentForm(FlaskForm):
    #initialize the form fields with datatypes
    ttl = StringField('Title', validators=[DataRequired()])
    mc = StringField('Module Code', validators=[DataRequired()])
    dline = DateTimeField('Deadline',format = '%d-%m-%y',render_kw={'placeholder': 'dd-mm-yyyy'},validators=[DataRequired()])
    desc = TextAreaField('Description', validators=[DataRequired()])

    
