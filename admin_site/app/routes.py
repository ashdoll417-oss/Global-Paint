from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ..shared.models import User, InventoryItem, GlobalSetting, StockMovement, PurchaseOrder, ItemType
from . import db
from .forms import InventoryForm, StockMovementForm, PurchaseOrderForm, TintForm, StockInForm, TintingForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def dashboard():
    # Inventory CRUD
    paint_items = InventoryItem.query.filter_by(type=ItemType.PAINT).count()
    carpet_items = InventoryItem.query.filter_by(type=ItemType.CARPET).count()
    recent_movements = StockMovement.query.order_by(StockMovement.timestamp.desc()).limit(10).all()
    recent_pos = PurchaseOrder.query.order_by(PurchaseOrder.created_at.desc()).limit(5).all()
    users = User.query.all()
    settings = GlobalSetting.query.all()
    total_items = paint_items + carpet_items
    return render_template('main/dashboard.html', 
                         total_items=total_items, paint_items=paint_items, carpet_items=carpet_items,
                         recent_movements=recent_movements, recent_pos=recent_pos,
                         users=users, settings=settings)
@main_bp.route('/inventory')
@login_required
def inventory_list():
    items = InventoryItem.query.all()
    return render_template('inventory/list.html', items=items)

@main_bp.route('/inventory/new', methods=['GET', 'POST'])
@login_required
def inventory_create():
    form = InventoryForm()
    if form.validate_on_submit():
        return render_template('inventory/form.html', form=form, title='New Inventory Item')
            name=form.name.data,
            sku=form.sku.data,
            description=form.description.data,
            type=form.type.data,
            unit_amount=form.unit_amount.data,
            owner_id=current_user.id
        )
        db.session.add(item)
        db.session.commit()
        flash('Product created successfully!')
        return redirect(url_for('main.inventory_list'))

@main_bp.route('/inventory/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def inventory_edit(item_id):
    item = InventoryItem.query.get_or_404(item_id)
    form = InventoryForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        flash('Inventory item updated!')
        return redirect(url_for('main.inventory_list'))
    return render_template('inventory/form.html', form=form, title='Edit Inventory Item')

@main_bp.route('/inventory/<int:item_id>/delete', methods=['POST'])
@login_required
def inventory_delete(item_id):
    item = InventoryItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Inventory item deleted!')
    return redirect(url_for('main.inventory_list'))

# Tinting
@main_bp.route('/inventory/<int:item_id>/tint', methods=['GET', 'POST'])
@login_required
def inventory_tint(item_id):
    base_item = InventoryItem.query.get_or_404(item_id)
    if base_item.type != ItemType.PAINT or base_item.status != 'available':
        flash('Can only tint base paint items.')
        return redirect(url_for('main.inventory_list'))
    
    form = TintForm()
    if form.validate_on_submit():
        pigment_item = InventoryItem.query.get_or_404(form.pigment_item_id.data)
        if pigment_item.type != ItemType.TINT or pigment_item.unit_amount < form.amount_used.data:
            flash('Invalid pigment item or insufficient stock.')
            return render_template('inventory/tint.html', form=form, base_item=base_item)
        
        # Deduct pigment
        pigment_item.unit_amount -= form.amount_used.data
        # Update base to tinted (no amount change for base, just status)
        base_item.status = 'tinted'
        # Create movements
        pigment_movement = StockMovement(
            item_id=pigment_item.id, movement_type='OUT', quantity=form.amount_used.data,
            reason='tinting_usage', user_id=current_user.id
        )
        tint_movement = StockMovement(
            item_id=base_item.id, movement_type='OUT', quantity=form.amount_used.data,
            reason='tinting_base', user_id=current_user.id
        )
        db.session.add(pigment_movement)
        db.session.add(tint_movement)
        db.session.commit()
        flash('Paint tinted successfully! Pigment deducted.')
        return redirect(url_for('main.inventory_list'))
    
    return render_template('inventory/tint.html', form=form, base_item=base_item)

# Stock Movements
@main_bp.route('/movements')
@login_required
def movements_list():
    movements = StockMovement.query.order_by(StockMovement.timestamp.desc()).all()
    return render_template('movements/list.html', movements=movements)

@main_bp.route('/movements/<int:item_id>/new', methods=['GET', 'POST'])
@login_required
def movement_create(item_id):
    form = StockMovementForm()
    item = InventoryItem.query.get_or_404(item_id)
    if form.validate_on_submit():
        movement = StockMovement(
            item_id=item_id,
            movement_type=form.movement_type.data,
            quantity=form.quantity.data,
            reason=form.reason.data,
            user_id=current_user.id
        )
        if form.po_id.data:
            po = PurchaseOrder.query.filter_by(po_number=form.po_id.data).first()
            if po:
                movement.po_id = po.id
        # Update item amount
        if form.movement_type.data == 'IN':
            item.unit_amount += form.quantity.data
        else:
            item.unit_amount -= form.quantity.data
            if item.unit_amount <= 0:
                item.status = 'out_of_stock'
        db.session.add(movement)
        db.session.commit()
        flash('Stock movement recorded!')
        return redirect(url_for('main.inventory_list'))
    return render_template('movements/form.html', form=form, item=item)

# Purchase Orders
@main_bp.route('/purchase-orders')
@login_required
def purchase_orders_list():
    pos = PurchaseOrder.query.all()
    return render_template('purchase_orders/list.html', pos=pos)

@main_bp.route('/purchase-orders/new', methods=['GET', 'POST'])
@login_required
def po_create():
    
    if form.validate_on_submit():
    @main_bp.route('/users')
            po_number=form.po_number.data,
            client_name=form.client_name.data,
            quantity_ordered=form.quantity_ordered.data,
            item_id=request.form.get('item_id')  # From select in template
        )
        db.session.add(po)
        db.session.commit()
        flash('Purchase order created!')
        return redirect(url_for('main.purchase_orders_list'))
@login_required
def users_list():
    users = User.query.all()
    return render_template('users/list.html', users=users)

@main_bp.route('/settings')
@login_required
def settings_list():
    settings = GlobalSetting.query.all()
    return render_template('settings/list.html', settings=settings)
