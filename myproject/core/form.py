from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email


class ContactUs(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message='provide name')])
    email = StringField('Email', validators=[DataRequired(message='provide email'), Email()])
    feedback = TextAreaField('Feedback / Questions', render_kw={"rows": 9, "cols": 50}, validators=[DataRequired()])
    submit = SubmitField('Submit')
