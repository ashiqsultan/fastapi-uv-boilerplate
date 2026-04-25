from fastapi import FastAPI
from app.logger import get_logger

app = FastAPI()

logger = get_logger(__name__)
logger.info("Starting the application")


@app.get("/")
def read_root():
    logger.debug("Received request for root endpoint")
    return {"Hello": "World"}
