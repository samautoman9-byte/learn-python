"""Core data structures for the merchant-facing takeout ordering app draft."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List


class OrderStatus(str, Enum):
    """Lifecycle of an order from creation to completion."""

    NEW = "new"
    ACCEPTED = "accepted"
    PREPARING = "preparing"
    READY = "ready"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class MenuItem:
    id: int
    name: str
    price: float
    category: str = "general"
    available: bool = True
    description: str = ""


@dataclass
class OrderItem:
    menu_item_id: int
    quantity: int = 1
    note: str = ""


@dataclass
class Order:
    id: int
    items: List[OrderItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.NEW
    customer_name: str = "walk-in"
    channel: str = "in_store"
    special_instructions: str = ""

    def calculate_total(self, menu_lookup: Dict[int, MenuItem]) -> float:
        """Compute total with a provided menu lookup."""
        total = 0.0
        for item in self.items:
            menu_item = menu_lookup.get(item.menu_item_id)
            if not menu_item:
                continue
            total += menu_item.price * item.quantity
        return round(total, 2)
