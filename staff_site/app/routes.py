from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, current_user
from werkzeug.security import check_password_hash
from ..shared.models import User, InventoryItem, StockMovement, PurchaseOrder, ItemType
from admin_site.app.forms import StockInForm, TintingForm, PurchaseOrderForm
from . import db
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.hashed_password, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid credentials')
    return render_template('main/login.html')

@main_bp.route('/')
@login_required
def dashboard():
    current_user_items = InventoryItem.query.filter_by(owner_id=current_user.id).all()
    return render_template('main/dashboard.html',
                           current_user_items=current_user_items,
                           total_items=len(current_user_items))

@main_bp.route('/movements')
@login_required
def movements_list():
    movements = StockMovement.query.filter_by(user_id=current_user.id).order_by(StockMovement.timestamp.desc()).all()
    return render_template('main/movements_list.html', movements=movements)

@main_bp.route('/po-create', methods=['GET', 'POST'])
@login_required
def po_create():
    items = InventoryItem.query.filter_by(owner_id=current_user.id).all()
    form = PurchaseOrderForm()
    form.item_id.choices = [(item.id, item.name) for item in items]
    if form.validate_on_submit():
        po_number = f"PO-{datetime.now().strftime('%Y%m%d')}-{current_user.id}"
        po = PurchaseOrder(
            po_number=po_number,
            client_name=form.client_name.data,
            quantity_ordered=form.quantity_ordered.data,
            item_id=form.item_id.data
        )
        db.session.add(po)
        db.session.commit()
        flash('Purchase order created!')
        return redirect(url_for('main.movements_list'))
    return render_template('main/po_create.html', form=form)

@main_bp.route('/stock-in', methods=['GET', 'POST'])
@login_required
def stock_in():
    items = InventoryItem.query.filter_by(owner_id=current_user.id).all()
    form = StockInForm()
    form.item_id.choices = [(item.id, f"{item.name} ({item.type.value})") for item in items]
    if form.validate_on_submit():
        item = InventoryItem.query.get_or_404(form.item_id.data)
        movement = StockMovement(
            item_id=item.id,
            movement_type='IN',
            quantity=form.quantity.data,
            reason=form.reason.data,
            user_id=current_user.id
        )
        item.unit_amount += form.quantity.data
        db.session.add(movement)
        db.session.commit()
        flash('Stock in recorded successfully!')
        return redirect(url_for('main.dashboard'))
    return render_template('main/stock_in.html', form=form)

@main_bp.route('/tinting', methods=['GET', 'POST'])
@login_required
def tinting():
    paints = InventoryItem.query.filter_by(owner_id=current_user.id, type=ItemType.PAINT).all()
    tints = InventoryItem.query.filter_by(owner_id=current_user.id, type=ItemType.TINT).all()
    form = TintingForm()
    form.base_paint_id.choices = [(p.id, p.name) for p in paints]
    form.tint_id.choices = [(t.id, t.name) for t in tints]
    if form.validate_on_submit():
        base_paint = InventoryItem.query.get_or_404(form.base_paint_id.data)
        tint_item = InventoryItem.query.get_or_404(form.tint_id.data)
        if tint_item.unit_amount < form.quantity.data:
            flash('Insufficient tint stock!')
            return render_template('main/tinting.html', form=form)
        # Deduct tint
        tint_item.unit_amount -= form.quantity.data
        # Create new tinted paint
        tinted_paint = InventoryItem(
            name=f"Tinted {base_paint.name}",
            description=f"Tinted with {tint_item.name} ({form.quantity.data}L)",
            type=ItemType.PAINT,
            unit_amount=form.quantity.data,
            status='tinted',
            owner_id=current_user.id
        )
        # Movements
        tint_out = StockMovement(
            item_id=tint_item.id, movement_type='OUT', quantity=form.quantity.data,
            reason='tinting_usage', user_id=current_user.id
        )
        tinted_in = StockMovement(
            item_id=tinted_paint.id, movement_type='IN', quantity=form.quantity.data,
            reason='tinting_created', user_id=current_user.id
        )
        db.session.add_all([tinted_paint, tint_out, tinted_in])
        db.session.commit()
        flash('Tinting completed! New tinted paint created.')
        return redirect(url_for('main.dashboard'))
    return render_template('main/tinting.html', form=form)
