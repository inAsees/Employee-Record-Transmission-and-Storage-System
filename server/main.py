import uvicorn
from fastapi import FastAPI
from routes import employee
from utils.logger.logger import setup_logger

app = FastAPI()
app.include_router(employee.router)

setup_logger("logs/server.log")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
