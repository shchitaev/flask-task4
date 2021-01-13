import time
import pymongo
from flask import Flask

app = Flask(__name__)
client = pymongo.MongoClient('mongo1',27017, replicaSet='rs0')
db = client['test-database']
collection = db['test-collection']
# cache = redis.Redis(host='redishost', port=6379)


def get_hit_count():
    entity = collection.find_one()
    if entity == None:
        collection.insert_one({"count":"1"})
        return 1
    newValue = int(entity['count']) + 1
    collection.update_one(
    {"_id": entity['_id']},
    {"$set":
        {"count": newValue,
    }})
    return newValue

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
