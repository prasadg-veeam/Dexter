"""Flask Order Board application."""
from flask import Flask, jsonify, request, render_template

from src.data_store import (
    create_order,
    get_all_orders,
    get_order,
    update_order,
    delete_order,
    order_to_dict,
)

app = Flask(__name__)

REQUIRED_FIELDS = ("customer", "item", "quantity", "price")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/orders")
def list_orders():
    return jsonify({"orders": [order_to_dict(o) for o in get_all_orders()]})


@app.post("/api/orders")
def add_order():
    data = request.get_json(silent=True) or {}
    missing = [f for f in REQUIRED_FIELDS if f not in data]
    if missing:
        return jsonify({"error": f"Missing required fields: {missing}"}), 400
    order = create_order(
        customer=data["customer"],
        item=data["item"],
        quantity=data["quantity"],
        price=data["price"],
    )
    return jsonify(order_to_dict(order)), 201


@app.get("/api/orders/<order_id>")
def get_one_order(order_id: str):
    order = get_order(order_id)
    if order is None:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order_to_dict(order))


@app.put("/api/orders/<order_id>")
def update_one_order(order_id: str):
    data = request.get_json(silent=True) or {}
    order = update_order(order_id, **data)
    if order is None:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order_to_dict(order))


@app.delete("/api/orders/<order_id>")
def delete_one_order(order_id: str):
    if not delete_order(order_id):
        return jsonify({"error": "Order not found"}), 404
    return jsonify({"deleted": order_id})


@app.get("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
