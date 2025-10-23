from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv("API_URL")
ORIGINAL_TIMEZONE = os.getenv("ORIGINAL_TIMEZONE", "UTC")
TARGET_TIMEZONE = os.getenv("TARGET_TIMEZONE", "Europe/Sofia")


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
