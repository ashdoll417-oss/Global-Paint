from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, NumberRange

class AccessForm(FlaskForm):
    access_code = PasswordField('Staff Access Code', validators=[DataRequired(), Length(min=4, max=20)])
    submit = SubmitField('Access Dashboard')

class SaleForm(FlaskForm):
    item_name = StringField('Item Name', validators=[DataRequired(), Length(min=1, max=100)])
    quantity = FloatField('Quantity', validators=[DataRequired(), NumberRange(min=0.01)])
    reason = TextAreaField('Reason (e.g., sale to customer)', validators=[DataRequired(), Length(min=5)])
    submit = SubmitField('Record Sale/Usage')
