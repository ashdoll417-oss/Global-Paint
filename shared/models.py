from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean, Text
from datetime import datetime
from enum import Enum

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    inventory_items = relationship("InventoryItem", back_populates="owner")

    def __repr__(self):
        return f'<User {self.username}>'


class ItemType(Enum):
    PAINT = "liters"
    CARPET = "meters"
    TINT = "liters"


class InventoryItem(Base):
    __tablename__ = 'inventory_items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    sku = Column(String(50), unique=True, index=True)
    description = Column(String)
    type = Column(SQLEnum(ItemType))
    unit_amount = Column(Float, default=0.0)
    status = Column(String, default='available')  # available, low_stock, out_of_stock, tinted
    owner_id = Column(Integer, ForeignKey('users.id'))

    # Relationships
    owner = relationship("User", back_populates="inventory_items")
    stock_movements = relationship("StockMovement", back_populates="item", cascade="all, delete-orphan")
    purchase_orders = relationship("PurchaseOrder", back_populates="item")


class StockMovement(Base):
    __tablename__ = 'stock_movements'

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey('inventory_items.id'), nullable=False)
    movement_type = Column(String(10), nullable=False)  # 'IN', 'OUT'
    quantity = Column(Float, nullable=False)
    reason = Column(String(100))  # purchase, sale, tinting_usage, etc.
    po_id = Column(Integer, ForeignKey('purchase_orders.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    item = relationship("InventoryItem", back_populates="stock_movements")
    po = relationship("PurchaseOrder")
    user = relationship("User")


class PurchaseOrder(Base):
    __tablename__ = 'purchase_orders'

    id = Column(Integer, primary_key=True, index=True)
    po_number = Column(String(50), unique=True, index=True)
    client_name = Column(String(255))
    quantity_ordered = Column(Float)
    status = Column(String(50), default='pending')  # pending, fulfilled, cancelled
    item_id = Column(Integer, ForeignKey('inventory_items.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    item = relationship("InventoryItem", back_populates="purchase_orders")
    stock_movements = relationship("StockMovement", back_populates="po")


class GlobalSetting(Base):
    __tablename__ = 'global_settings'

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(255), unique=True, index=True, nullable=False)
    value = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
