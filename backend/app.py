from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from routes.order_routes import order_bp
from routes.mobile_routes import mobile_bp
from routes.auth_routes import auth_bp
from routes.analytics_routes import analytics_bp
from routes.shop_routes import shop_bp
from routes.offers_routes import offers_bp

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb://localhost:27017/ash_mobiles"
mongo = PyMongo(app)

# 🔥 THIS IS THE CRITICAL PART
order_bp.mongo = mongo
mobile_bp.mongo = mongo
auth_bp.mongo = mongo
analytics_bp.mongo = mongo
shop_bp.mongo = mongo
offers_bp.mongo = mongo

app.register_blueprint(order_bp, url_prefix="/api/orders")
app.register_blueprint(mobile_bp, url_prefix="/api/mobiles")
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(analytics_bp, url_prefix="/api/analytics")
app.register_blueprint(shop_bp, url_prefix="/api/shop")
app.register_blueprint(offers_bp, url_prefix="/api/offers")

@app.route("/")
def home():
    return "Ash Mobile's Backend API is running"

if __name__ == "__main__":
    app.run(debug=True)