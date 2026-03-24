from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class InventoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=100)])
    sku = StringField('SKU', validators=[DataRequired(), Length(min=1, max=50)])
    description = TextAreaField('Description', validators=[Optional()])
    type = SelectField(
        'Type',
        choices=[
            ('PAINT', 'Paint (liters)'),
            ('CARPET', 'Carpet (meters)'),
            ('TINT', 'Tint (liters)')
        ],
        validators=[DataRequired()]
    )
    unit_amount = FloatField('Unit Amount', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Save')
