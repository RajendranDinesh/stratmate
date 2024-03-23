# StratMate

## Description
A Full Stack Application utilizing FastAPI, PostgreSQL, and ReactJS to showcase chess player data from the lichess API. (was my testing project to get into an internship)

## Setup Instructions

Clone the repository:

```bash
git clone https://github.com/RajendranDinesh/StratMate
```

Create `.env` files in both the frontend and backend folders.

### Frontend's .env

```bash
REACT_APP_API_URL = <your_fast_api_url> (e.g., `http://127.0.0.1:8000`)
```

### Backend's .env

```bash
JWT_SECRET = <some_random_key>
DATABASE_URL = <your_postgresql_db_url>
```

After setting up `.env` files:

```bash
# FastAPI
cd backend
pip install -r requirements.txt
python3 init_db.py  # only for the first time
python3 main.py

# React
cd frontend
npm i
npm start
```

### Run Tests with pytest

```bash
pip install pytest
pytest
```

### Optimization Strategies

To enhance efficiency and maintainability, the codebase incorporates the following optimization strategies:

1. **Function Utilization:** Streamlining the codebase through strategic use of functions, reducing redundancy and promoting an organized and readable structure.

2. **Debouncing for API Calls:** Optimization of performance by implementing a debouncing mechanism, minimizing unnecessary API calls and ensuring judicious request handling.

3. **Modular Code Design:** Emphasis on writing modular code to improve readability, encourage reusability, and facilitate easier maintenance. Each module serves a specific purpose, contributing to a cohesive and well-organized software architecture.

These optimization strategies collectively aim to create a more efficient, responsive, and maintainable codebase.