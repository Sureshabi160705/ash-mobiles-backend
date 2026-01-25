def get_all_offers(mongo):
    """Get all offers from database"""
    offers = list(mongo.db.offers.find({}, {"_id": 0}))
    return offers

def get_offer_by_id(mongo, offer_id):
    """Get a specific offer by ID"""
    offer = mongo.db.offers.find_one({"id": offer_id}, {"_id": 0})
    return offer

def add_offer(mongo, offer):
    """Add a new offer to database"""
    # Get the max ID and increment
    existing_offers = mongo.db.offers.find({}, {"id": 1}).sort("id", -1).limit(1)
    max_id = 0
    for doc in existing_offers:
        max_id = doc.get("id", 0)
    
    offer["id"] = max_id + 1
    result = mongo.db.offers.insert_one(offer)
    return offer

def update_offer(mongo, offer_id, updated_data):
    """Update an existing offer"""
    result = mongo.db.offers.update_one(
        {"id": offer_id},
        {"$set": updated_data}
    )
    return result.modified_count > 0

def delete_offer(mongo, offer_id):
    """Delete an offer by ID"""
    result = mongo.db.offers.delete_one({"id": offer_id})
    return result.deleted_count > 0

def initialize_default_offers(mongo):
    """Initialize database with default offers if empty"""
    if mongo.db.offers.count_documents({}) == 0:
        default_offers = [
            {
                "id": 1,
                "title": "Summer Sale",
                "description": "Get up to 30% discount on all phones",
                "discount": "30%",
                "icon": "🌞"
            },
            {
                "id": 2,
                "title": "Free Shipping",
                "description": "Free shipping on orders above ₹5000",
                "discount": "FREE",
                "icon": "🚚"
            },
            {
                "id": 3,
                "title": "Warranty Extension",
                "description": "Extend warranty to 6 months for just ₹999",
                "discount": "50%",
                "icon": "🛡️"
            }
        ]
        mongo.db.offers.insert_many(default_offers)
