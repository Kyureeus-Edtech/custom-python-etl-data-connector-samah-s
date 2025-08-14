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

```bash
SamahSyed_3122225001120_C
├── etl_connector.py: Main ETL pipeline script
├── test_integration.py: Integration tests for full ETL flow
├── test_validation.py: Unit tests for validation and transformation logic
├── .env: Environment variables (excluded from Git)
├── requirements.txt: Python dependencies
└── README.md: Documentation (this file)
.gitignore: Ignore sensitive & unnecessary files such as .env, __pycache__, venv
```

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


## Testing Overview

This project includes two main test scripts to ensure correctness and reliability of the ETL pipeline.

### Test coverage includes:
- Handles invalid entries in the blocklist.  
- Logs skipped entries with reasons.  
- Ensures consistent data insertion on repeated runs (**idempotent**).  
- Includes timestamps for audit purposes.

### Integration Test (`test_integration.py`)

**Purpose**: Runs the entire ETL pipeline end-to-end against a dedicated test MongoDB database/collection.

**Scenarios Tested**:
- Records are successfully inserted into MongoDB.
- Each record contains an `ingested_at` timestamp.
- The `type` field is correctly classified as either `"ip"` or `"cidr"`.
- No duplicate IP/CIDR entries are stored.

**Sample Test Output**
```bash
2025-08-14 14:57:30,386 - INFO - ETL Pipeline started.
2025-08-14 14:57:30,420 - INFO - Connected to MongoDB database: test_etl_db, collection: test_etl_collection
2025-08-14 14:57:30,422 - INFO - Extracting data from https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/firehol_level1.netset ...
2025-08-14 14:57:30,895 - INFO - Transforming data ...
2025-08-14 14:57:30,964 - INFO - Transformation complete. 4565 unique valid records found.
2025-08-14 14:57:30,965 - INFO - Loading 4565 records into MongoDB ...
2025-08-14 14:57:49,183 - INFO - Data loaded successfully.
2025-08-14 14:57:49,183 - INFO - ETL Pipeline finished. Duration: 0:00:18.797049
Integration test passed.
```


### Validation Test (`test_validation.py`)

**Purpose**: Tests the `transform()` function in isolation without touching the database.

**Scenarios Tested**:
- Only valid IPs and CIDRs are kept — invalid entries are removed.
- Duplicate entries are removed.
- Correct classification between `"ip"` and `"cidr"`.
- Original IP/CIDR strings are preserved in the output.

**Sample Input Used for Validation**:
\```python
raw_data = [
    "192.168.0.1",    # valid IP
    "192.168.0.0/24", # valid CIDR
    "invalid_ip",     # invalid
    "192.168.0.1"     # duplicate
]
\```

**Assertions Performed**:
- Only two records should remain after cleaning (`"192.168.0.1"` and `"192.168.0.0/24"`).
- `"192.168.0.1"` is classified as `"ip"`.
- `"192.168.0.0/24"` is classified as `"cidr"`.

**Sample Test Output**
```bash
2025-08-14 14:58:25,711 - INFO - Transforming data ...
2025-08-14 14:58:25,711 - WARNING - Skipping invalid entry: invalid_ip
2025-08-14 14:58:25,712 - INFO - Transformation complete. 2 unique valid records found.
Validation test passed.
```

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
