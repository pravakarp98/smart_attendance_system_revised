from pymongo import MongoClient
from app.config import settings

client = MongoClient(settings.DATABASE_URL)
db = client.get_database("org_db")
admins_collection = db.get_collection("admins_collection")
students_collection = db.get_collection("students_collection")