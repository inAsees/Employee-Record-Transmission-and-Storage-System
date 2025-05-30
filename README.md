# Employee Record Transmission and Storage System

This project implements a secure and scalable system for transmitting and storing employee records. It consists of two main components:

- **Client**: Reads employee data and sends it to the backend server with JWT authentication.
- **Server**: Receives, validates, and asynchronously stores employee records into a MySQL database.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Running with Docker Compose](#running-with-docker-compose)
- [Running Locally](#running-locally)
- [Testing](#testing)

---

## Features

- JWT-based authentication for secure communication between client and server.
- Asynchronous record processing with buffering for efficient storage.
- REST API built with FastAPI for high performance and easy extensibility.
- MySQL backend for persistent employee data storage.
- Dockerized setup for easy deployment using Docker Compose.
- Comprehensive unit tests for both client and server components.

---

## Project Structure

```plaintext
employee_record_system
├── client                      # Client-side code and assets
│   ├── __init__.py             # Python package marker
│   ├── assets                  # Static assets like CSV data files
│   │   └── employee_data.csv   # Employee data CSV file used by client
│   ├── config                  # Configuration files for client
│   │   └── config.py           # Client configuration
│   ├── main.py                 # Main entry point for client app
│   ├── middleware              # Middleware functions like decorators for auth
│   │   └── decorators.py       # Decorators for client-side (e.g., JWT auth)
│   ├── models                  # Data models (e.g., Dataclass models)
│   │   └── models.py           # Client-side data models
│   ├── requirements.txt        # Python dependencies for client
│   ├── services                # Service modules for business logic
│   │   ├── reader.py           # Reads employee data from CSV
│   │   └── sender.py           # Sends data to server asynchronously
│   ├── tests                   # Unit tests for client modules
│   │   ├── __init__.py
│   │   ├── test_decorators.py
│   │   ├── test_reader.py
│   │   ├── test_sender.py
│   │   └── test_token.py
│   └── utils                   # Utility helpers (e.g., JWT handling)
│       └── jwt
│           ├── config.py       # JWT config (secret keys, etc.)
│           └── token.py        # JWT token generation and validation
├── docker-compose.yml          # Docker Compose setup for multi-container app
├── README.md                   # Project README file (this file)
└── server                      # Server-side code and files
    ├── __init__.py            # Python package marker
    ├── config                 # Configuration files for server
    │   └── config.py          # Server config (DB, JWT, etc.)
    ├── database               # Database related files
    │   ├── db.py              # DB connection and queries
    │   └── init.sql           # SQL script to initialize database schema
    ├── Dockerfile             # Dockerfile to build server container image
    ├── logs                   # Server log files
    │   └── server.log         # Main server log
    ├── main.py                # Main entry point for server app (FastAPI)
    ├── middleware             # Middleware like decorators for server
    │   └── decorators.py      # JWT authentication decorators for API
    ├── models                 # Data models (ORM or Pydantic)
    │   └── models.py          # Server-side data models
    ├── requirements.txt       # Python dependencies for server
    ├── routes                 # API route handlers
    │   └── employee.py        # Endpoint(s) to accept employee records
    ├── services               # Server service modules (e.g., buffering)
    │   └── buffer.py          # Buffer logic for incoming data before DB insert
    ├── tests                  # Unit tests for server modules
    │   ├── test_buffer.py
    │   ├── test_db.py
    │   ├── test_token.py
    │   └── test_upload.py
    └── utils                  # Utility helpers
        ├── jwt
        │   ├── config.py      # JWT config for server
        │   └── jwt.py         # JWT encoding/decoding logic
        └── logger
            └── logger.py      # Custom logging setup for server
```

---

## Technologies Used

- Python 3.13
- FastAPI
- MySQL 9.3
- Docker & Docker Compose
- pytest & pytest-asyncio

---

## Setup and Installation

### Prerequisites

- Docker and Docker Compose installed on your machine.
- (Optional) Python 3.13+ for running client/server locally without Docker.

---

### Running with Docker Compose

1. Unzip the file with:
    ```bash
       unzip employee_record_system.zip
    ```
2. Change to the project directory with:
    ```bash
       cd employee_record_system/
    ```
3. Run:
    ```bash
       docker-compose up --build
    ```
   This will:
     - Start a MySQL container with the employee_record_system database initialized.
     - Build and start the backend FastAPI server connected to MySQL.
4. The backend API will be available at: http://localhost:8000
5. Change the directory to the Client with:
    ```bash
       cd client/
    ```
6. Run the client with:
    ```bash
       python3 main.py
    ```

---

### Running Locally

1. Unzip the file with:
    ```bash
       unzip employee_record_system.zip
    ```
2. Change to the project directory with:
    ```bash
       cd employee_record_system/
    ```

#### SERVER
- The server exposes a FastAPI endpoint `/upload` to accept employee records.
- JWT token authentication is enforced.
- Data is buffered asynchronously and stored in MySQL.
- To run the server locally:
    ```bash
     cd server
     pip install -r requirements.txt
     python3 main.py
  ```
- The backend API will be available at: http://localhost:8000

#### CLIENT
- The client reads employee data from `client/assets/employee_data.csv`.
- It sends employee records asynchronously to the server.
- To run the client locally (requires Python and dependencies installed):
    ```bash
     cd client
     pip install -r requirements.txt
     python3 main.py
  ```

---

## Testing

- Both client and server contain unit tests in their respective tests directories.
- To run tests for server:
   ```bash
      cd server
      pytest
   ```
- To run tests for client:
   ```bash
      cd client
      pytest
   ```
