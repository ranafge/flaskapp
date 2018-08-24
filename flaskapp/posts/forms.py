from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length
from flaskapp.models import Posts


class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=60)])
    author = StringField('Author', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired(),Length(min=30)])

    def validate_title(self, title):
        title = Posts.query.filter_by(title=title.data).first()
        if title is not None:
            raise ValidationError('Please use different title.')

    def __repr__(self):
        return "<Article %r>" % self.title
