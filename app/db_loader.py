import psycopg2
from psycopg2.extras import execute_values
from loguru import logger
from app import config

def get_connection():
    try:
        conn = psycopg2.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASS
        )
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return None
    
def create_table():
    """Create table if it does not exist"""

    conn = get_connection()
    if not conn:
        return
    with conn.cursor() as cur:
        cur.execute("""
    CREATE TABLE IF NOT EXISTS exchange_rates (
        id SERIAL PRIMARY KEY,
        currency VARCHAR(10),
        rate FLOAT,
        reference_date DATE,
        created_at TIMESTAMP WITH TIME ZONE,
        created_at_converted TIMESTAMP WITH TIME ZONE
    );
""")

        conn.commit()
    conn.close()
    logger.info("Table 'exchange_rates' is ready.")

def load_to_db(df):
    if df is None or df.empty:
        logger.warning("No data to insert")
        return
    
    conn = get_connection()
    if not conn:
        return
    
    try:
        with conn.cursor() as cur:
            records = df.values.tolist()
            execute_values(cur, """
                INSERT INTO exchange_rates (currency, rate, reference_date, created_at, created_at_converted)
                VALUES %s; 
                """, records)
            conn.commit()
        logger.info(f"Inserted {len(df)} records into database.")
    except Exception as e:
        logger.error(f"Error inserting data: {e}")
    finally:
        conn.close()
