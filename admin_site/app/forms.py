from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class InventoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=100)])
    description = TextAreaField('Description', validators=[Optional()])
    type = SelectField('Type', choices=[
        ('PAINT', 'Paint (Liters)'),
        ('CARPET', 'Carpet (Meters)'),
        ('TINT', 'Tint/Pigment (Liters)')
    ], validators=[DataRequired()])
    unit_amount = FloatField('Unit Amount', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Save')

class StockMovementForm(FlaskForm):
    movement_type = SelectField('Type', choices=[('IN', 'IN'), ('OUT', 'OUT')], validators=[DataRequired()])
    quantity = FloatField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    reason = StringField('Reason', validators=[DataRequired(), Length(min=1, max=100)])
    po_id = StringField('PO Number (optional)')
    submit = SubmitField('Record Movement')

class PurchaseOrderForm(FlaskForm):
    
    client_name = StringField('Client Name', validators=[DataRequired(), Length(max=255)])
    item_id = SelectField('Item', coerce=int, validators=[DataRequired()])
    quantity_ordered = FloatField('Quantity Ordered', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Create PO')
class TintForm(FlaskForm):
    pigment_item_id = StringField('Pigment/Tint Item ID', validators=[DataRequired()])
    amount_used = FloatField('Amount of Pigment Used (Liters)', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Tint Paint')

class StockInForm(FlaskForm):
    item_id = SelectField('Product (Paint/Carpet)', coerce=int, validators=[DataRequired()])
    quantity = FloatField('Quantity to Add', validators=[DataRequired(), NumberRange(min=0)])
    reason = StringField('Reason', default='stock_in', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Stock In')

class TintingForm(FlaskForm):
    base_paint_id = SelectField('Base Paint', coerce=int, validators=[DataRequired()])
    tint_id = SelectField('Tint', coerce=int, validators=[DataRequired()])
    quantity = FloatField('Tint Quantity (Liters)', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Apply Tinting')
