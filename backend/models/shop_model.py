from bson.objectid import ObjectId

def get_shop_status(mongo):
    """Get current shop status from database"""
    shop = mongo.db.shop.find_one({})
    if shop:
        return {
            "status": shop.get("status", "open"),
            "last_updated": shop.get("last_updated")
        }
    else:
        # Initialize shop status if not exists
        mongo.db.shop.insert_one({"status": "open"})
        return {"status": "open"}

def update_shop_status(mongo, status):
    """Update shop status (open/closed)"""
    if status not in ["open", "closed"]:
        return False
    
    result = mongo.db.shop.update_one(
        {},
        {
            "$set": {
                "status": status,
                "last_updated": __import__('datetime').datetime.utcnow()
            }
        },
        upsert=True
    )
    
    return result.modified_count > 0 or result.upserted_id is not None
