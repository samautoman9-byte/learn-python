"""Lightweight in-memory storage layer for the draft app."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional

from .models import MenuItem, Order, OrderItem, OrderStatus


@dataclass
class InMemoryStore:
    """Simple store to manage menu items and orders."""

    menu_items: Dict[int, MenuItem] = field(default_factory=dict)
    orders: Dict[int, Order] = field(default_factory=dict)
    _menu_seq: int = 0
    _order_seq: int = 0

    def add_menu_item(
        self, name: str, price: float, *, category: str = "general", description: str = ""
    ) -> MenuItem:
        self._menu_seq += 1
        item = MenuItem(
            id=self._menu_seq, name=name, price=round(price, 2), category=category, description=description
        )
        self.menu_items[item.id] = item
        return item

    def set_availability(self, item_id: int, available: bool) -> Optional[MenuItem]:
        item = self.menu_items.get(item_id)
        if item:
            item.available = available
        return item

    def list_menu(self, *, only_available: bool = False) -> List[MenuItem]:
        items = list(self.menu_items.values())
        if only_available:
            return [item for item in items if item.available]
        return items

    def create_order(
        self,
        items: Iterable[OrderItem],
        *,
        customer_name: str = "walk-in",
        channel: str = "in_store",
        special_instructions: str = "",
    ) -> Order:
        self._order_seq += 1
        order = Order(
            id=self._order_seq,
            items=list(items),
            customer_name=customer_name,
            channel=channel,
            special_instructions=special_instructions,
        )
        self.orders[order.id] = order
        return order

    def update_order_status(self, order_id: int, status: OrderStatus) -> Optional[Order]:
        order = self.orders.get(order_id)
        if order:
            order.status = status
        return order

    def list_orders(self) -> List[Order]:
        return list(self.orders.values())
