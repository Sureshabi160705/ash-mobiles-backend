from flask import Blueprint, request, jsonify
from models.shop_model import get_shop_status, update_shop_status

shop_bp = Blueprint("shop", __name__)

@shop_bp.route("/status", methods=["GET"])
def get_status():
    """Get current shop status"""
    try:
        status_info = get_shop_status(shop_bp.mongo)
        return jsonify({
            "status": status_info["status"],
            "message": "Shop status retrieved successfully"
        }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@shop_bp.route("/status", methods=["PUT"])
def set_status():
    """Update shop status"""
    try:
        data = request.json
        new_status = data.get("status")
        
        if not new_status:
            return jsonify({"message": "Status is required"}), 400
        
        success = update_shop_status(shop_bp.mongo, new_status)
        
        if success:
            return jsonify({
                "status": new_status,
                "message": "Shop status updated successfully"
            }), 200
        else:
            return jsonify({"message": "Failed to update shop status"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500
