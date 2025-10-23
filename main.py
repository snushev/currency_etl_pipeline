from app.config import API_URL
from app import requester, worker, db_loader
from app import config
print(config.DB_USER, config.DB_PASS)

def main():
    db_loader.create_table()
    raw_data = requester.fetch_data()
    if not raw_data:
        print("No data fetched")
        return
    
    transformed = worker.process_data(raw_data)
    if transformed is not None:
        db_loader.load_to_db(transformed)
        print(transformed.head())
    else:
        print("Data processing failed")

if __name__ == "__main__":
    main()

