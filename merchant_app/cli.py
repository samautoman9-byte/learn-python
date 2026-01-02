"""Tiny CLI demo for the merchant-facing takeout ordering draft."""

from __future__ import annotations

import argparse
from textwrap import indent

from .services import advance_order, order_with_items, seed_demo_store, summarize_order


def run_demo() -> None:
    store = seed_demo_store()
    print("=== 商家工作台：外卖点餐初稿演示 ===")
    print("\n可售卖菜品：")
    for item in store.list_menu(only_available=True):
        print(f"- #{item.id} {item.name} ¥{item.price:.2f} [{item.category}]")

    print("\n下单：美团渠道（午高峰套餐）")
    order = order_with_items(
        store,
        [
            (1, 1),  # 黄焖鸡
            (2, 1),  # 番茄牛腩
            (4, 2),  # 冰豆浆
        ],
    )
    order.customer_name = "李雷"
    order.channel = "meituan"
    order.special_instructions = "少辣，提前5分钟出餐"
    print(indent(summarize_order(order, store.menu_items), "  "))

    print("\n更新状态：接单 → 制作 → 待取 → 完成")
    final_order = advance_order(store, order)
    print(f"订单状态已到达：{final_order.status.value}")

    print("\n售罄处理：将凉拌木耳下架")
    removed = store.set_availability(3, False)
    print(f"菜品 {removed.name} 是否在售：{removed.available}")

    print("\n所有订单（含状态）：")
    for existing in store.list_orders():
        print(indent(summarize_order(existing, store.menu_items), "  "))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Merchant-side takeout ordering draft CLI")
    parser.add_argument("--demo", action="store_true", help="run the scripted demo")
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.demo or not any(vars(args).values()):
        run_demo()


if __name__ == "__main__":
    main()
