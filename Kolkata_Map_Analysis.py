import pprint
import sqlite3
def get_db(db_name):
	from pymongo import MongoClient
	client = MongoClient('localhost',27017)
	db = client[db_name]
	return db


def make_pipeline():
	pipeline = [
	{ "$group" : { "_id" : "$created.user" , "count" : { "$sum" : 1 } } },
	{ "$sort" : { "count" : -1 } },
	{ "$limit" : 10}
	]
	return pipeline


def aggregate(db, pipeline):
	results = db.kolkala_map.aggregate(pipeline)
	return results

if __name__ == '__main__':
	db = get_db('openstreetmap')

	count = db.kolkata_map.find().count()
	print("Number of Entries : {}".format(count))

	nodes = db.kolkata_map.find({'type' : 'node'}).count()
	print("Number of nodes : {}".format(nodes))

	# ways = db.kolkata_map.find({'type' : 'way'}).count()
	# print("Number of ways : {}".format(ways))

	# num_uinque_users = db.kolkata_map.distinct('created.user')
	# print("Number of distinct users who have contributed to the Kokalta OSM dataset : {}".format(len(num_uinque_users)))

	# top_10_query = make_pipeline()
	# top_10_contributors = list(db.kolkata_map.aggregate(top_10_query))
	# pprint.pprint(top_10_contributors)
	# contribution = 0
	# for item in top_10_contributors:
	# 	contribution += item['count']

	# print(contribution)
	# print("{} %".format((contribution/count)*100))

	
