from pymongo import MongoClient
from sys import argv

client = MongoClient('localhost', 27017)
db = client.amazon_products
key = argv[1]
value = argv[2]
#collection = db.products_collection.find({key: value})
collection = db.products_collection.find()
for product in collection:
	print(product)
	#print(product['sections'][0])
