from flask import Blueprint, jsonify, request
from models.mobile_model import (
    add_mobile,
    get_all_mobiles,
    get_mobile_by_id,
    update_mobile,
    delete_mobile,
)
from bson.objectid import ObjectId

mobile_bp = Blueprint("mobile", __name__)


# OWNER → ADD MOBILE
@mobile_bp.route("/add", methods=["POST"])
def add_mobile_route():
    data = request.json

    if not data:
        return jsonify({"message": "No data received"}), 400

    data["views"] = 0
    new_id = add_mobile(mobile_bp.mongo, data)
    return jsonify({"message": "Mobile added successfully", "id": new_id})


# CUSTOMER / OWNER → GET ALL MOBILES
@mobile_bp.route("/", methods=["GET"])
def get_mobiles():
    mobiles = get_all_mobiles(mobile_bp.mongo)
    return jsonify(mobiles)


# GET single mobile
@mobile_bp.route("/<id>", methods=["GET"])
def get_mobile(id):
    m = get_mobile_by_id(mobile_bp.mongo, id)
    if not m:
        return jsonify({"message": "Not found"}), 404
    
    # Increment view count
    try:
        mobile_bp.mongo.db.mobiles.update_one(
            {"_id": ObjectId(id)},
            {"$inc": {"views": 1}}
        )
    except Exception as e:
        print("View tracking error:", e)
    
    return jsonify(m)


# OWNER → UPDATE mobile
@mobile_bp.route("/<id>", methods=["PUT"])
def update_mobile_route(id):
    data = request.json
    if not data:
        return jsonify({"message": "No data received"}), 400
    update_mobile(mobile_bp.mongo, id, data)
    return jsonify({"message": "Mobile updated"})


# OWNER → DELETE mobile
@mobile_bp.route("/<id>", methods=["DELETE"])
def delete_mobile_route(id):
    delete_mobile(mobile_bp.mongo, id)
    return jsonify({"message": "Mobile deleted"})
