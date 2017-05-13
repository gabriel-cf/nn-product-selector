from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.tfg_users
users = db.users_collection.find()

for user in users:
	#print(user)
	print("{};{}".format(user['nat'], user['login']['username']))


