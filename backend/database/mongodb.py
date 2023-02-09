from pymongo import MongoClient

client = MongoClient(
    "mongodb://admin_user:password@localhost:27017/?authMechanism=DEFAULT"
)
db = client["submit"]
