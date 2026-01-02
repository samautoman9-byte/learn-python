"""Domain services for the merchant-facing draft app."""

from __future__ import annotations

from typing import Iterable, List, Tuple

from .models import MenuItem, Order, OrderItem, OrderStatus
from .storage import InMemoryStore


def seed_demo_store() -> InMemoryStore:
    """Create a store with demo data."""
    store = InMemoryStore()
    store.add_menu_item("招牌黄焖鸡", 28.0, category="main", description="每天限量，经典必点")
    store.add_menu_item("番茄牛腩饭", 32.0, category="main")
    store.add_menu_item("小份凉拌木耳", 12.0, category="side")
    store.add_menu_item("冰豆浆", 8.0, category="drink")
    store.set_availability(3, False)  # sold out side dish
    return store


def order_with_items(store: InMemoryStore, items: Iterable[Tuple[int, int]]) -> Order:
    """Create an order from (menu_item_id, qty) pairs."""
    order_items: List[OrderItem] = []
    for menu_item_id, qty in items:
        order_items.append(OrderItem(menu_item_id=menu_item_id, quantity=qty))
    return store.create_order(order_items)


def summarize_order(order: Order, menu_lookup: dict) -> str:
    """Return a human-readable summary."""
    lines = [
        f"订单 #{order.id} · 客户: {order.customer_name} · 渠道: {order.channel} · 状态: {order.status.value}",
    ]
    for item in order.items:
        menu_item: MenuItem | None = menu_lookup.get(item.menu_item_id)
        name = menu_item.name if menu_item else f"未知菜品 {item.menu_item_id}"
        price = menu_item.price if menu_item else 0
        lines.append(f"  - {name} x{item.quantity} · ¥{price * item.quantity:.2f}")
    total = order.calculate_total(menu_lookup)
    if order.special_instructions:
        lines.append(f"备注: {order.special_instructions}")
    lines.append(f"合计: ¥{total:.2f}")
    return "\n".join(lines)


def advance_order(store: InMemoryStore, order: Order) -> Order:
    """Move an order through the basic merchant-facing steps."""
    flow = [
        OrderStatus.ACCEPTED,
        OrderStatus.PREPARING,
        OrderStatus.READY,
        OrderStatus.COMPLETED,
    ]
    for status in flow:
        store.update_order_status(order.id, status)
    return store.orders[order.id]
