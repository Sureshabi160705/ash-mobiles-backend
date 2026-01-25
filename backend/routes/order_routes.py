from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from datetime import datetime

order_bp = Blueprint("order", __name__)


def get_next_order_id(mongo):
    """Generate the next sequential order ID (1-1000)"""
    counter = mongo.db.order_counter.find_one_and_update(
        {"_id": "order_id"},
        {"$inc": {"sequence": 1}},
        upsert=True,
        return_document=True
    )
    return counter["sequence"]


@order_bp.route("/place", methods=["POST"])
def place_order():
    data = request.get_json()

    if not data:
        return jsonify({"message": "No data received"}), 400

    try:
        # Generate sequential order ID
        order_id = get_next_order_id(order_bp.mongo)
        
        order = {
            "order_id": order_id,
            "customer_email": data["customer_email"].strip().lower(),
            "customer_name": data.get("customer_name", ""),
            "customer_phone": data.get("customer_phone", ""),
            "shipping_address": data.get("shipping_address", ""),
            "shipping_city": data.get("shipping_city", ""),
            "shipping_state": data.get("shipping_state", ""),
            "shipping_pincode": data.get("shipping_pincode", ""),
            "shipping_notes": data.get("shipping_notes", ""),
            "brand": data["brand"],
            "model": data["model"],
            "price": data["price"],
            "description": data.get("description", ""),
            "payment_method": data.get("payment_method", "upi"),
            "payment_status": data.get("payment_status", "Pending"),
            "payment_screenshot": data.get("payment_screenshot", ""),
            "payment_screenshot_submitted": datetime.now() if data.get("payment_screenshot") else None,
            "status": data.get("status", "Pending"),
            "created_date": datetime.now()
        }

        res = order_bp.mongo.db.orders.insert_one(order)
        return jsonify({"message": "Order placed successfully", "id": order_id})

    except Exception as e:
        print("ORDER ERROR:", e)
        return jsonify({"message": "Order failed"}), 500



@order_bp.route("/my-orders/<email>", methods=["GET"])
def my_orders(email):
    email = email.strip().lower()

    docs = order_bp.mongo.db.orders.find({"customer_email": email})
    orders = []
    for d in docs:
        d.pop('_id', None)
        orders.append(d)
    return jsonify(orders)


@order_bp.route("/all", methods=["GET"])
def all_orders():
    docs = order_bp.mongo.db.orders.find().sort("order_id", -1)
    orders = []
    for d in docs:
        d.pop('_id', None)
        orders.append(d)
    return jsonify(orders)



@order_bp.route("/<int:id>/status", methods=["PUT"])
def update_status_by_id(id):
    data = request.get_json()
    try:
        order_bp.mongo.db.orders.update_one(
            {"order_id": id},
            {"$set": {"status": data["status"]}}
        )
        return jsonify({"message": "Order status updated"})
    except Exception as e:
        print("UPDATE ERROR:", e)
        return jsonify({"message": "Update failed"}), 500


@order_bp.route("/update-status", methods=["PUT"])
def update_status():
    data = request.get_json()
    try:
        order_bp.mongo.db.orders.update_one(
            {"order_id": int(data["id"])},
            {"$set": {"status": data["status"]}}
        )
        return jsonify({"message": "Order status updated successfully"})
    except Exception as e:
        print("UPDATE ERROR:", e)
        return jsonify({"message": "Update failed"}), 500


@order_bp.route("/update-payment-status", methods=["PUT"])
def update_payment_status():
    data = request.get_json()
    try:
        order_bp.mongo.db.orders.update_one(
            {"order_id": int(data["id"])},
            {"$set": {"payment_status": data["payment_status"]}}
        )
        return jsonify({"message": f"Payment status updated to {data['payment_status']}"})
    except Exception as e:
        print("UPDATE PAYMENT STATUS ERROR:", e)
        return jsonify({"message": "Update failed"}), 500


@order_bp.route("/<int:id>", methods=["DELETE"])
def delete_order(id):
    try:
        order_bp.mongo.db.orders.delete_one({"order_id": id})
        return jsonify({"message": "Order deleted successfully"})
    except Exception as e:
        print("DELETE ERROR:", e)
        return jsonify({"message": "Delete failed"}), 500
