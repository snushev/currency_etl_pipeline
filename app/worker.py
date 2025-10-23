import pandas as pd
from loguru import logger
from app import helpers, config

def process_data(data):
    if not data or 'rates' not in data:
        logger.error("Invalid or empty data received for processing.")
        return None
    
    rates = data.get('rates')
    date = data.get('date', helpers.get_current_time(config.ORIGINAL_TIMEZONE) )

    df = pd.DataFrame(list(rates.items()), columns=['currency', 'rate'])

    df['reference_date'] = date

    current_time = helpers.get_current_time(config.ORIGINAL_TIMEZONE)
    df['created_at'] = current_time
    df['created_at_converted'] = helpers.convert_timezone(current_time, config.TARGET_TIMEZONE)

    df['rate'] = df['rate'].astype(float)
    df['currency'] = df['currency'].astype(str)
    df['reference_date'] = df['reference_date'].astype(str)
    
    logger.info(f"Processed {len(df)} exchange rates for {date}.")

    return df
