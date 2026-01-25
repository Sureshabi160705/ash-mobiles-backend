def create_order(mongo, order):
    mongo.db.orders.insert_one(order)

def get_all_orders(mongo):
    return list(mongo.db.orders.find({}, {"_id": 0}))

def get_orders_by_customer(mongo, email):
    return list(
        mongo.db.orders.find(
            {"customer_email": email},
            {"_id": 0}
        )
    )
