from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed

class PostForm(FlaskForm):
    title = StringField('TITLE', validators=[DataRequired()])                  
    content = TextAreaField('CONTENT', validators=[DataRequired()])
    media = FileField('MEDIA')
    submit = SubmitField('POST')

class CommentForm(FlaskForm):
    comment_text = TextAreaField('COMMENT', validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField('POST')    