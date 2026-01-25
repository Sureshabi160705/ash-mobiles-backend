from flask import Blueprint, jsonify
from datetime import datetime, timedelta

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/summary", methods=["GET"])
def get_analytics_summary():
    """Get all analytics data in one call"""
    try:
        # Total orders
        total_orders = analytics_bp.mongo.db.orders.count_documents({})
        
        # Pending orders
        pending_orders = analytics_bp.mongo.db.orders.count_documents({"status": "Pending"})
        
        # This month orders
        now = datetime.now()
        start_of_month = datetime(now.year, now.month, 1)
        this_month = analytics_bp.mongo.db.orders.count_documents({
            "created_date": {"$gte": start_of_month}
        })
        
        # Last month orders
        last_month_end = start_of_month - timedelta(days=1)
        start_of_last_month = datetime(last_month_end.year, last_month_end.month, 1)
        last_month = analytics_bp.mongo.db.orders.count_documents({
            "created_date": {
                "$gte": start_of_last_month,
                "$lt": start_of_month
            }
        })
        
        # Total product views
        mobiles = list(analytics_bp.mongo.db.mobiles.find({}, {"views": 1}))
        total_views = sum(mobile.get("views", 0) for mobile in mobiles)
        
        # Total products
        total_products = analytics_bp.mongo.db.mobiles.count_documents({})
        
        # Top viewed products
        top_products = list(analytics_bp.mongo.db.mobiles.find()
                           .sort("views", -1)
                           .limit(5))
        
        top_products_list = []
        for idx, product in enumerate(top_products, 1):
            top_products_list.append({
                "rank": idx,
                "brand": product.get("brand", ""),
                "model": product.get("model", ""),
                "views": product.get("views", 0),
                "price": product.get("price", 0)
            })
        
        return jsonify({
            "total_orders": total_orders,
            "pending_orders": pending_orders,
            "this_month_orders": this_month,
            "last_month_orders": last_month,
            "total_views": total_views,
            "total_products": total_products,
            "top_products": top_products_list,
            "current_month": now.strftime("%B %Y")
        })
    except Exception as e:
        print("Analytics ERROR:", e)
        return jsonify({"error": str(e)}), 500
