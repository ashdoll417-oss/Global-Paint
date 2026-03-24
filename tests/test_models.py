import pytest
from shared.models import User, InventoryItem, ItemType, StockMovement, PurchaseOrder, GlobalSetting, Base
from app import db

@pytest.mark.usefixtures("init_database")
class TestModels:
    
    def test_user_creation(self, app):
        with app.app_context():
            user = User(username="admin", email="admin@example.com", hashed_password="testpass", is_admin=True)
            db.session.add(user)
            db.session.commit()
            assert user.id is not None
            assert user.username == "admin"
            assert user.is_admin is True

    def test_inventory_item_creation(self, app):
        with app.app_context():
            item = InventoryItem(
                name="Premium White Paint",
                description="High quality base paint",
                type=ItemType.PAINT,
                unit_amount=100.5
            )
            db.session.add(item)
            db.session.commit()
            assert item.id is not None
            assert item.name == "Premium White Paint"
            assert item.type == ItemType.PAINT
            assert item.unit_amount == 100.5

    def test_relationships(self, app):
        with app.app_context():
            user = User(username="testuser")
            item = InventoryItem(name="Test Item", type=ItemType.PAINT)
            db.session.add_all([user, item])
            db.session.commit()
            
            item.owner_id = user.id
            db.session.commit()
            
            assert item.owner.username == "testuser"
            assert user.inventory_items[0].name == "Test Item"

    def test_stock_movement(self, app):
        with app.app_context():
            item = InventoryItem(name="Test Paint", type=ItemType.PAINT)
            db.session.add(item)
            db.session.commit()
            
            movement = StockMovement(
                item_id=item.id,
                movement_type="IN",
                quantity=50.0,
                reason="purchase"
            )
            db.session.add(movement)
            db.session.commit()
            
            assert len(item.stock_movements) == 1
            assert item.stock_movements[0].quantity == 50.0

    def test_purchase_order(self, app):
        with app.app_context():
            item = InventoryItem(name="Carpet", type=ItemType.CARPET)
            db.session.add(item)
            db.session.commit()
            
            po = PurchaseOrder(
                po_number="PO001",
                client_name="Test Client",
                quantity_ordered=100.0,
                item_id=item.id
            )
            db.session.add(po)
            db.session.commit()
            
            assert po.item.name == "Carpet"

    def test_global_setting(self, app):
        with app.app_context():
            setting = GlobalSetting(key="business_name", value="Global Paint")
            db.session.add(setting)
            db.session.commit()
            assert setting.key == "business_name"
            assert setting.value == "Global Paint"

    def test_unique_constraint_user(self, app):
        """Test unique username/email constraints."""
        with app.app_context():
            user1 = User(username="test", email="test@example.com", hashed_password="pass")
            db.session.add(user1)
            db.session.commit()
            
            user2 = User(username="test", email="other@example.com", hashed_password="pass")
            db.session.add(user2)
            with pytest.raises(Exception):  # IntegrityError
                db.session.commit()

    def test_invalid_item_type(self, app):
        """Test enum validation."""
        with app.app_context():
            item = InventoryItem(name="Invalid", type="INVALID")  # Invalid enum
            db.session.add(item)
            with pytest.raises(Exception):
                db.session.commit()

    def test_negative_quantity(self, app):
        """Test business logic - negative quantity."""
        with app.app_context():
            item = InventoryItem(name="Negative", unit_amount=-10.0)
            db.session.add(item)
            db.session.commit()  # Allow for now, but flag low_stock
            assert item.unit_amount == -10.0
            assert item.status == 'available'  # Default
