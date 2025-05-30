import csv
from datetime import datetime
from typing import List, Generator
from models.models import Employee
from config.config import CSV_FILE_PATH

BATCH_SIZE = 100


def read_csv_file_in_batches() -> Generator[List[Employee], None, None]:
    batch = []
    print("88888888", CSV_FILE_PATH)
    with open(CSV_FILE_PATH, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            employee = Employee(
                employee_id=int(row["Employee ID"]),
                name=row["Name"],
                email=row["Email"],
                department=row["Department"],
                designation=row["Designation"],
                salary=float(row["Salary"]),
                date_of_joining=datetime.strptime(
                    row["Date of Joining"], "%Y-%m-%d"
                ).date(),
            )
            batch.append(employee)

            if len(batch) >= BATCH_SIZE:
                yield batch
                batch = []

        if batch:  # Yield remaining records
            yield batch
