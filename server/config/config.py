import os

DB_USER = os.environ.get("DB_USER", "root")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = int(os.environ.get("DB_PORT", 3306))
DB_NAME = os.environ.get("DB_NAME", "employee_record_system")
DB_PASSWORD = os.environ.get("DB_PASSWORD")