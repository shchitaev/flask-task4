from flask import Flask, request, jsonify
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

def get_db():
    client = MongoClient(host='mongo', port=27017, username='root', password='pass', authSource='admin')
    db = client["cluster_db"]
    return db

@app.route('/')
def fetch_counter():
    db = get_db()
    _counters = db.cluster_db.find()
    
    counters = [{"_id": counter["_id"],"value": counter["value"]} for counter in _counters]

    if len(counters) > 0:
        _id = counters[0]["_id"]
        db.cluster_db.find_one_and_update({'_id': _id}, {'$inc': {'value': 1}})
        counted = db.cluster_db.find_one({"_id": _id})

        return "You have visted me {} times".format(counted['value'])
    
    db.cluster_db.insert_one({"value": 1})

    return "You have visted me 1 time"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
