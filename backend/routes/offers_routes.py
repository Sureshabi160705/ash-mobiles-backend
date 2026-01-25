from flask import Blueprint, request, jsonify
from models.offers_model import (
    get_all_offers, 
    get_offer_by_id, 
    add_offer, 
    update_offer, 
    delete_offer,
    initialize_default_offers
)

offers_bp = Blueprint("offers", __name__)

@offers_bp.route("/", methods=["GET"])
def get_offers():
    """Get all offers"""
    try:
        # Initialize default offers if database is empty
        initialize_default_offers(offers_bp.mongo)
        
        offers = get_all_offers(offers_bp.mongo)
        return jsonify({
            "offers": offers,
            "message": "Offers retrieved successfully"
        }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@offers_bp.route("/<int:offer_id>", methods=["GET"])
def get_single_offer(offer_id):
    """Get a specific offer"""
    try:
        offer = get_offer_by_id(offers_bp.mongo, offer_id)
        if offer:
            return jsonify({
                "offer": offer,
                "message": "Offer retrieved successfully"
            }), 200
        else:
            return jsonify({"message": "Offer not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@offers_bp.route("/", methods=["POST"])
def create_offer():
    """Create a new offer"""
    try:
        data = request.json
        
        if not data:
            return jsonify({"message": "Request body is empty"}), 400
        
        # Validate required fields
        required_fields = ["title", "description", "discount", "icon"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"message": f"Missing required fields: {', '.join(missing_fields)}"}), 400
        
        new_offer = {
            "title": data["title"],
            "description": data["description"],
            "discount": data["discount"],
            "icon": data["icon"]
        }
        
        offer = add_offer(offers_bp.mongo, new_offer)
        return jsonify({
            "offer": offer,
            "message": "Offer created successfully"
        }), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@offers_bp.route("/<int:offer_id>", methods=["PUT"])
def update_single_offer(offer_id):
    """Update an existing offer"""
    try:
        data = request.json
        
        success = update_offer(offers_bp.mongo, offer_id, data)
        
        if success:
            updated_offer = get_offer_by_id(offers_bp.mongo, offer_id)
            return jsonify({
                "offer": updated_offer,
                "message": "Offer updated successfully"
            }), 200
        else:
            return jsonify({"message": "Offer not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@offers_bp.route("/<int:offer_id>", methods=["DELETE"])
def delete_single_offer(offer_id):
    """Delete an offer"""
    try:
        success = delete_offer(offers_bp.mongo, offer_id)
        
        if success:
            return jsonify({"message": "Offer deleted successfully"}), 200
        else:
            return jsonify({"message": "Offer not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500
