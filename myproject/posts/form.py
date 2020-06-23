from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SubmitField, TextAreaField


class AddPost(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message='provide title')])
    post_image = FileField('Image', validators=[FileAllowed(['jpg', 'png'])])
    content = TextAreaField('Content', render_kw={"rows": 11, "cols": 70}, validators=[DataRequired(message='provide content')])
    submit = SubmitField('Create Post!')


class UpdatePost(FlaskForm):
    title = StringField('Title', validators=[DataRequired(message='provide heading')])
    post_image = FileField('Image', validators=[FileAllowed(['jpg', 'png'])])
    content = TextAreaField('Content', render_kw={"rows": 11, "cols": 70}, validators=[DataRequired(message='provide content')])
    submit = SubmitField('Edit Post!')
