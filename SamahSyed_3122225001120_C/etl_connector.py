import os
import requests
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

# Load env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def extract():
    url = "https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/firehol_level1.netset"
    response = requests.get(url)
    response.raise_for_status()
    return response.text.splitlines()

def transform(data):
    # Remove comments & empty lines
    cleaned = [line.strip() for line in data if line and not line.startswith("#")]
    return [{"ip": ip, "ingested_at": datetime.utcnow()} for ip in cleaned]

def load(records):
    if records:
        collection.insert_many(records)
        print(f"Inserted {len(records)} records into MongoDB.")
    else:
        print("No records to insert.")

def run_pipeline():
    raw_data = extract()
    transformed_data = transform(raw_data)
    load(transformed_data)

if __name__ == "__main__":
    run_pipeline()
