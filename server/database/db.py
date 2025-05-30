import mysql.connector
from mysql.connector import Error, IntegrityError
from models.models import Employee
from config.config import DB_PASSWORD, DB_USER, DB_HOST, DB_PORT, DB_NAME
import logging


def get_connection():
    print(DB_USER, " ", DB_HOST, " ", DB_NAME, " ", DB_PASSWORD, " ", DB_PORT)
    try:
        return mysql.connector.connect(
            user=DB_USER,
            host=DB_HOST,
            port=DB_PORT,
            password=DB_PASSWORD,
            database=DB_NAME,
        )
    except Error as e:
        logging.critical(f"Failed to connect to database: {e}")
        raise RuntimeError("Database connection failed.")


def bulk_insert_employees(employees: list[Employee]):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        data = [
            (
                e.employee_id,
                e.name,
                e.email,
                e.department,
                e.designation,
                e.salary,
                e.date_of_joining,
            )
            for e in employees
        ]
        query = """
        INSERT INTO employee_records (employee_id, name, email, department, designation, salary, date_of_joining)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            name=VALUES(name),
            email=VALUES(email),
            department=VALUES(department),
            designation=VALUES(designation),
            salary=VALUES(salary),
            date_of_joining=VALUES(date_of_joining)
        """
        cursor.executemany(query, data)
        conn.commit()
    except IntegrityError as e:
        conn.rollback()
        logging.error(f"Integrity error during insert: {e}")
        raise ValueError("Duplicate or invalid data encountered.")
    except Error as e:
        conn.rollback()
        logging.error(f"MySQL error during insert: {e}")
        raise RuntimeError("Database insert failed.")
    finally:
        cursor.close()
        conn.close()
