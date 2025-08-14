# Custom Python ETL Data Connector — FireHOL IP Blocklist

## Overview

This project is part of the Software Architecture Assignment for the Kyureeus EdTech program at SSN CSE.  
The goal is to build a custom Python ETL (Extract, Transform, Load) pipeline that connects to an external data provider, processes the data, and loads it into a MongoDB collection following secure coding and project structure best practices.

For this submission, the chosen data provider is **FireHOL Level 1 IP Blocklist** — a publicly available list of known malicious IP addresses and CIDR ranges.

## API Details 
- **Source**: https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/firehol_level1.netset 
- **Format**: Plain text, IP addresses 
- **Auth**: None

## Features Implemented

### Extract
- Fetches the raw IP and CIDR blocklist from FireHOL’s public repository.  
- Handles connection errors and request timeouts gracefully.

### Transform
- **Validation:** Ensures each entry is a valid IPv4/IPv6 address or CIDR range.  
- **Classification:** Adds a `type` field to classify records as `"ip"` or `"cidr"`.  
- **Normalization:**  
  - IPs are stored in standard string format (e.g., `192.168.0.1`).  
  - CIDRs are normalized to canonical form (e.g., `192.168.0.0/24`).  
- **De-duplication:** Removes duplicate entries in-memory before loading.  
- Adds an ingestion timestamp (`ingested_at`) to each record for auditing.

### Load
- Inserts the transformed records into a MongoDB collection in batches.  
- Uses upsert operations to prevent duplicate records on repeated runs.  
- Handles MongoDB connection errors and write failures.

## Secure Credential Handling
- All database connection details are stored in a local `.env` file (not committed to Git).  
- Environment variables are loaded using the `python-dotenv` library.  
- `.gitignore` is configured to exclude `.env` and other sensitive files.

## Testing
- Integration and validation test scripts written and executed.

## Project Structure


## Environment Variables


## Installation & Setup

### 1. Clone the repository
```bash
git clone <repo_url>
cd <repo_folder>
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file
Create a `.env` file in the project root with the following variables:

```bash
MONGO_URI=your_mongo_uri
DB_NAME=your_db_name
COLLECTION_NAME=your_collection_name
```

## Running the ETL Pipeline
```bash
python etl_connector.py
```

## MongoDB Collection Design
Each document in MongoDB looks like:
```json
{
  "ip": "203.0.113.0/24",
  "type": "cidr",
  "ingested_at": "2025-08-14T10:15:30.000Z"
}
```

## Testing & Validation

### Run all tests
```bash
python test_integration.py
python test_validation.py
```

### Test coverage includes:
- Handles invalid entries in the blocklist.  
- Logs skipped entries with reasons.  
- Ensures consistent data insertion on repeated runs (**idempotent**).  
- Includes timestamps for audit purposes.

## Assignment Requirements Covered
- **Data Provider:** FireHOL public IP blocklist.  
- **Secure Credentials:** Stored in `.env`.  
- **ETL Pipeline:** Extract → Transform → Load.  
- **MongoDB Storage:** One collection, timestamped records.  
- **Validation & Error Handling:** Implemented in all stages.  
- **Git Hygiene:** `.env` ignored, descriptive README included.  
- **Extra Enhancements:** Record classification, CIDR normalization, in-memory de-duplication.

---

**Author:** Samah Syed (Roll No: 3122225001120)
