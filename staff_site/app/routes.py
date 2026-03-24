from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from . import db
from .forms import AccessForm, SaleForm
from ..shared.models import StockMovement, InventoryItem
from sqlalchemy import text
from datetime import datetime
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def access():
    if session.get('staff_access'):
        return redirect(url_for('main.dashboard'))
    
    form = AccessForm()
    if form.validate_on_submit():
        staff_code = os.getenv('STAFF_ACCESS_CODE')
        if staff_code and form.access_code.data == staff_code:
            session['staff_access'] = True
            flash('Access granted!')
            return redirect(url_for('main.dashboard'))
        flash('Invalid staff access code')
    return render_template('access.html', form=form)

@main_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get('staff_access'):
        return redirect(url_for('main.access'))
    
    # Handle sale form POST
    form = SaleForm()
    if form.validate_on_submit():
        item = InventoryItem.query.filter_by(name=form.item_name.data).first()
        if not item:
            flash('Item not found')
        else:
            movement = StockMovement(
                item_id=item.id,
                movement_type='deduction',
                quantity=form.quantity.data,
                reason=form.reason.data
            )
            item.unit_amount -= form.quantity.data
            if item.unit_amount <= 0:
                item.status = 'out_of_stock'
            db.session.add(movement)
            db.session.commit()
            flash('Sale/Usage recorded successfully!')
            return redirect(url_for('main.dashboard'))
    
    # Query staff_inventory_view for GET
    with db.engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM staff_inventory_view ORDER BY name"))
        inventory_data = [dict(row._mapping) for row in result]
    
    return render_template('dashboard.html', inventory=inventory_data, form=form)

@main_bp.route('/logout')
def logout():
    session.pop('staff_access', None)
    flash('Logged out')
    return redirect(url_for('main.access'))
