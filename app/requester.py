import requests
from app import config
from loguru import logger

def fetch_data():
    try:
        if not config.API_URL:
            raise ValueError("API_URL is not set in environment variables.")
        
        response = requests.get(config.API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()  
        logger.info(f"Successfully fetch data for date: {data.get('date')}")
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"Error: {e}")
        return None
