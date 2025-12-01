
# **📘 Project Documentation**

This project provides a **prediction API** that analyzes client purchase patterns from a **remote MySQL database (via SSH tunnel)**.
The API runs on **FastAPI** and exposes endpoints at:
➡️ [http://localhost:8000/docs](http://localhost:8000/docs)

---

# **🚀 Getting Started**

## **1. Clone the Repository**

```bash
git clone <your-repo-url>
cd <your-project-folder>
```

---

## **2. Install Dependencies**

Make sure you have **Python 3.10+** installed.

```bash
pip install -r requirements.txt
```

---

## **3. Configure Environment**

Create a `.env` file with your **SSH and MySQL credentials**:

```dotenv
SSH_HOST=<remote_host>
SSH_PORT=<ssh_port>
SSH_USER=<ssh_user>
SSH_PASSWORD=<ssh_password>

DB_HOST=<db_host>
DB_PORT=<db_port>
DB_USER=<db_user>
DB_PASSWORD=<db_password>
DB_NAME=<db_name>
```

> ⚠️ Incorrect values here will prevent the API from connecting to the database.

---

## **4. Run the API Server**

```bash
uvicorn backend.main:app --reload
```

Open API docs:
➡️ [http://localhost:8000/docs](http://localhost:8000/docs)

---

# **📂 Project Structure**

```
project/
│
├── core/
│   ├── remote_db.py         # Remote MySQL connector (via SSH tunnel)
│   └── prediction.py        # Main prediction logic (cycle analysis)
│
├── requests/
│   └── rq.py                # Service layer: SQL queries using RemoteMySQL
│
├── api/
│   └── predict.py           # FastAPI router for predictions
│
├── .env                     # Environment variables (SSH + SQL)
├── requirements.txt         # Dependencies
└── backend/main.py          # FastAPI app entrypoint
```

---

# **🔌 How It Works**

### **1. `core/remote_db.py` – Remote DB Connector**

* Opens an SSH tunnel
* Connects to remote MySQL
* Runs `.query()` and `.execute()`
* Returns results as Python dictionaries

Used everywhere you need database access.

---

### **2. `requests/rq.py` – Service Layer**

* Runs SQL queries using `RemoteMySQL`
* Fetches sales, clients, goods data
* Returns structured datasets for prediction

Think of it as the **bridge between DB and prediction engine**.

---

### **3. `core/prediction.py` – Prediction Logic**

* Calculates purchase cycles
* Scores variance & confidence
* Predicts next order date & amount
* Classifies patterns (e.g., highly regular)
* Filters out irrelevant data

This is the **brain of the system**.

---

### **4. `api/predict.py` – API Router**

**Endpoint:**

```
GET /predict/
```

* Accepts filters (`min_requirements`, `confidence_threshold`)
* Fetches DB data via `rq.py`
* Runs prediction logic from `core/prediction.py`
* Returns JSON results

All output is visible in Swagger UI.

---

# **📊 API Output**

For each **client + product** pair, the system detects:

* Purchase frequency
* Pattern stability
* Last purchase date
* Predicted next purchase date
* Predicted amount
* Confidence score

Useful for:

* CRM integration
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

# **💡 How to Run (Step by Step)**

1. Clone repo & navigate:

```bash
git clone <your-repo-url>
cd <your-project-folder>
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure `.env` with SSH + MySQL credentials.

4. Start the API:

```bash
uvicorn main:app --reload
```

5. Test endpoints in Swagger UI:
   ➡️ [http://localhost:8000/docs](http://localhost:8000/docs)

6. Optional: Use Postman or any HTTP client to query `/predict/`.

