from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed

class PostForm(FlaskForm):
    title = StringField('TITLE', validators=[DataRequired()])                  
    content = TextAreaField('CONTENT', validators=[DataRequired()])
    picture = FileField('MEDIA', validators=[FileAllowed(['jpg', 'png', 'MOV'])])
    submit = SubmitField('POST')