# Personal Finance Tracker

## Features and Functionalities

**Register a User**

**Log in a User**

**Get Profile Information**

**Filter Expense**

**Installation and Setup**

**Clone the Repo**

```bash
git clone -b main personal-finance-tracker
```

**Go to the Directory**

```bash
cd personal-finance-tracker
```

**Create Virtual Environment and Activate**

For Windows

```bash
python -m venv env

env/Scripts/activate
```

For Linux

```bash
python3 -m venv env && source env/bin/activate
```

**Install requirements**

```bash
pip install -r requirements.txt
```

Once intalled use the command to run the server

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8080
```
