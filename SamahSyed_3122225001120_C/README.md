# FireHOL IP List ETL Connector

## Overview
This ETL pipeline fetches the FireHOL Level 1 IP blacklist, cleans the data, and stores it in MongoDB.

## API Details
- **Source**: https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/firehol_level1.netset
- **Format**: Plain text, IP addresses
- **Auth**: None

## Setup
1. Create `.env` file:
```env
MONGO_URI=your_mongodb_uri
DB_NAME=firehol_data
COLLECTION_NAME=firehol_level1_raw
```
2. Install dependencies:
```env
pip install -r requirements.txt
```
3. Run:
```env
python etl_connector.py
```

## Output
MongoDB collection: firehol_level1_raw with IPs and timestamps.

