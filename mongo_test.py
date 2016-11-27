# coding:utf-8
import random, pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
client.drop_database('test')
db = client.test
coll = db.coll

rs = coll.insert_one({'a':1, 'b':2})
object_id = rs.inserted_id

print(object_id)

rs = coll.insert_many([{'a':random.randint(1,10), 'b':22} for _ in range(10)])
print(rs.inserted_ids)

print(coll.count())
