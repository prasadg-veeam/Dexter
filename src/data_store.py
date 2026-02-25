"""In-memory Order store."""
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import uuid


@dataclass
class Order:
    customer: str
    item: str
    quantity: int
    price: float
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: str = "pending"
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


_orders: dict[str, Order] = {}


def create_order(customer: str, item: str, quantity: int, price: float) -> Order:
    order = Order(customer=customer, item=item, quantity=quantity, price=price)
    _orders[order.id] = order
    return order


def get_all_orders() -> list[Order]:
    return sorted(_orders.values(), key=lambda o: o.created_at)


def get_order(order_id: str) -> Order | None:
    return _orders.get(order_id)


def update_order(order_id: str, **kwargs) -> Order | None:
    order = _orders.get(order_id)
    if order is None:
        return None
    for key, value in kwargs.items():
        if hasattr(order, key) and key not in ("id", "created_at"):
            setattr(order, key, value)
    return order


def delete_order(order_id: str) -> bool:
    if order_id in _orders:
        del _orders[order_id]
        return True
    return False


def clear_orders() -> None:
    """Remove all orders (used in tests)."""
    _orders.clear()


def order_to_dict(order: Order) -> dict:
    return asdict(order)
