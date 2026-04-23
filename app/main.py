from fastapi import FastAPI
from app.logger import get_logger
from app.db.db import Database
from app.config import get_settings
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

app = FastAPI()
logger = get_logger(__name__)
settings = get_settings()

is_hide_docs = settings.environment == "production"
docs_url = None if is_hide_docs else "/docs"
redoc_url = None if is_hide_docs else "/redoc"
openapi_url = None if is_hide_docs else "/openapi.json"


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Database.connect()
    yield
    await Database.disconnect()
    print("Disconnected from database")


app = FastAPI(
    lifespan=lifespan, docs_url=docs_url, redoc_url=redoc_url, openapi_url=openapi_url
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


logger = get_logger(__name__)
logger.info("Starting the application")


@app.get("/")
def read_root():
    logger.debug("Received request for root endpoint")
    return {"Hello": "World"}


@app.get("/health")
async def health_check():
    logger.debug("Received request for health check")
    # TODO check database connection and other dependencies here
    try:
        result = await Database.fetchval("SELECT 1")
        logger.debug(f"Database connection test result: {result}")
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return {"status": "error", "details": "Database connection failed"}
    return {"status": "ok"}
