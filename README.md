
# **📘 Project Documentation (Simplified README)**

This project provides a **prediction API** that analyzes client purchase patterns from a **remote MySQL database (via SSH tunnel)**.
The API runs on **FastAPI**, and exposes endpoints at:
**[http://localhost:8000/docs](http://localhost:8000/docs)**

---

# **🚀 Getting Started**

## **1. Install Dependencies**

Make sure you have Python 3.10+.

```bash
pip install -r requirements.txt
```

---

## **2. Check Your `.env`**

You must configure your SSH + MySQL credentials in the `.env` file.


If these values are wrong, the API will not be able to connect to the remote DB.

---

## **3. Start the API Server**

```bash
uvicorn backend.main:app --reload
```

Open API docs:

➡️ **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

# **📂 Project Structure (Simplified)**

```
project/
│
├── core/
│   ├── remote_db.py         # Remote MySQL connector (via SSH tunnel)
│   └── prediction.py        # Main prediction logic (cycle analysis)
│
├── requests/
│   └── rq.py                # Request layer calling MySQL using RemoteMySQL
│
├── api/
│   └── predict.py           # FastAPI router for predictions
│
├── .env                     # Environment variables (SSH + SQL)
├── requirements.txt         # Dependencies
└── backend/main.py          # FastAPI app entrypoint
```

---

# **🔌 How It Works (Simple Explanation)**

### **1. `core/remote_db.py` – Remote DB Connector**

This file contains the `RemoteMySQL` class, which:

* Opens an SSH tunnel
* Connects to the remote MySQL database
* Allows running `.query()` and `.execute()`
* Returns results as Python dictionaries

This class is used everywhere you need DB access.

---

### **2. `requests/rq.py` – Request Layer**

This module contains functions that:

* Use the `RemoteMySQL` object
* Run SQL queries (e.g., get sales, clients, goods)
* Return clean structured data for prediction
* Prepare datasets for the prediction engine

Think of it like the **service layer**.

---

### **3. `core/prediction.py` – Main Prediction Logic**

This file contains:

* Purchase cycle calculation
* Variance / confidence scoring
* Next expected order date
* Predicted order amount
* Pattern classification
* Filtering logic

This is the **brain** of the system.

---

### **4. `api/predict.py` – API Router**

This exposes an endpoint:

```
GET /predict/
```

It:

* Accepts filters (`min_requirements`, `confidence_threshold`)
* Fetches DB data using `rq.py`
* Applies prediction logic from `core/prediction.py`
* Returns clean JSON results to the client

All output is visible in Swagger UI.

---

# **📊 What the API Does**

For each **client + product** pair, the system detects:

* How often they buy
* How stable their pattern is
* Last purchase date
* Expected next purchase date
* Predicted amount
* Confidence score

Used for:

* CRM integrations
* Sales forecasting
* Manager reminders
* Detecting lost clients

---

# **🔧 Example Output**

```json
{
  "client_id": 17834,
  "client_name": "Customer 1",
  "goods_id": 2726,
  "goods_name": "Chemical A",
  "last_requirement_date": "2025-06-23",
  "predicted_next_purchase_date": "2025-11-10",
  "avg_interval_days": 140,
  "predicted_amount": 33.33,
  "confidence_score": 0.95,
  "pattern_consistency": "highly_regular"
}
```

---

# **✔️ Summary**

What you need to understand:

* `.env` → credentials
* `remote_db.py` → connects to DB
* `rq.py` → runs queries
* `prediction.py` → processes data
* `predict.py` → API endpoint
* `localhost:8000/docs` → test everything
