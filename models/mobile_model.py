from bson.objectid import ObjectId


def add_mobile(mongo, mobile):
    res = mongo.db.mobiles.insert_one(mobile)
    return str(res.inserted_id)


def get_all_mobiles(mongo):
    docs = mongo.db.mobiles.find()
    result = []
    for d in docs:
        d['id'] = str(d['_id'])
        d.pop('_id', None)
        result.append(d)
    return result


def get_mobile_by_id(mongo, id):
    doc = mongo.db.mobiles.find_one({"_id": ObjectId(id)})
    if not doc:
        return None
    doc['id'] = str(doc['_id'])
    doc.pop('_id', None)
    return doc


def update_mobile(mongo, id, data):
    mongo.db.mobiles.update_one({"_id": ObjectId(id)}, {"$set": data})


def delete_mobile(mongo, id):
    mongo.db.mobiles.delete_one({"_id": ObjectId(id)})
