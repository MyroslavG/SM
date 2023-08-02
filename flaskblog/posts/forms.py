from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('TITLE', validators=[DataRequired()])                  
    content = TextAreaField('CONTENT', validators=[DataRequired()])
    submit = SubmitField('POST')