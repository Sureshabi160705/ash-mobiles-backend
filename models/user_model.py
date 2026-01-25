def create_user(mongo, user):
    mongo.db.users.insert_one(user)

def find_user_by_email(mongo, email):
    return mongo.db.users.find_one({"email": email})
