from flask_wtf import FlaskForm
from flask_wtf import Form
from wtforms import TextAreaField, SubmitField, validators
from wtforms import StringField, BooleanField

class BrandForm(FlaskForm):
    name = StringField("Name",  [validators.DataRequired()])
    email = StringField("Email",  [validators.DataRequired(
        "Please enter your email address."), validators.Email("Please enter your email address.")])
    subject = StringField("Subject",  [validators.DataRequired()])
    message = TextAreaField("Message",  [validators.DataRequired()])
    submit = SubmitField("Send")
    