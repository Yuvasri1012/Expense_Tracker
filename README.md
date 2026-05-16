# 💰 Expense Tracker — Django + MySQL

## Prerequisites
- Python 3.10+
- MySQL 8.0+

---

## 1. MySQL Database Setup

MySQL-ல் login பண்ணி database create பண்ணுங்க:

```sql
CREATE DATABASE expense_tracker CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

## 2. Project Setup

### Step 1 — Virtual Environment Create பண்ணுங்க

```bash
cd expense_tracker_project
python -m venv .venv
```

### Step 2 — Activate பண்ணுங்க

**Windows:**
```bash
.venv\Scripts\activate
```

**Mac / Linux:**
```bash
source .venv/bin/activate
```

### Step 3 — Dependencies Install பண்ணுங்க

```bash
pip install -r requirements.txt
```

> **Note:** `mysqlclient` install ஆக MySQL development libraries வேணும்.
>
> **Ubuntu/Debian:**
> ```bash
> sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
> ```
>
> **Mac (Homebrew):**
> ```bash
> brew install mysql-client pkg-config
> ```
>
> **Windows:** [mysqlclient wheel](https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient) download பண்ணி install பண்ணுங்க.

---

## 3. Database Settings Update

`config/settings.py` open பண்ணி இந்த part update பண்ணுங்க:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'expense_tracker',   # ← உங்க database name
        'USER': 'root',              # ← உங்க MySQL username
        'PASSWORD': 'your_password', # ← உங்க MySQL password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

---

## 4. Run Migrations

```bash
python manage.py migrate
```

---

## 5. Superuser Create (Optional — Admin panel access)

```bash
python manage.py createsuperuser
```

---

## 6. Server Start பண்ணுங்க

```bash
python manage.py runserver
```

Browser-ல் திறங்க: **http://127.0.0.1:8000**

---

## Features

- 📊 Dashboard — Income, Expense, Balance, Savings Rate
- 📈 6-Month Trend Chart
- 🍕 Category-wise Pie Chart
- 📋 Transaction History with Filters
- ➕ Add / Delete Transactions
- 🏷️ Custom Categories (with icon & color)
- 👤 Multi-user support (each user sees only their data)
- 🎁 Demo data auto-added on registration

---

## Project Structure

```
expense_tracker_project/
├── .venv/                  ← Virtual environment (gitignore பண்ணுங்க)
├── config/
│   ├── settings.py         ← MySQL config இங்க
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── tracker/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── apps.py
├── templates/
│   └── tracker/
│       ├── base.html
│       ├── dashboard.html
│       ├── transaction_list.html
│       ├── add_transaction.html
│       ├── category_list.html
│       ├── login.html
│       └── register.html
├── static/
├── manage.py
└── requirements.txt
```
