# Use official Python image
FROM python:3.13.3

# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install  -r requirements.txt

# Copy the rest of the server code
COPY . .

# Start the FastAPI server
CMD ["python3", "main.py"]
