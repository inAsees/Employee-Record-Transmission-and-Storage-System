CREATE DATABASE IF NOT EXISTS employee_record_system;

USE employee_record_system;

CREATE TABLE IF NOT EXISTS employee_records (
  employee_id INT NOT NULL,
  name VARCHAR(100) DEFAULT NULL,
  email VARCHAR(100) DEFAULT NULL,
  department VARCHAR(50) DEFAULT NULL,
  designation VARCHAR(50) DEFAULT NULL,
  salary DECIMAL(10,2) DEFAULT NULL,
  date_of_joining DATE DEFAULT NULL,
  PRIMARY KEY (employee_id),
  UNIQUE KEY email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
