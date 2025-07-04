import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def test_connection(port):
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=port
        )
        print(f"Successfully connected to the database on port {port}!")
        conn.close()
        return True
    except Exception as e:
        print(f"Error connecting to the database on port {port}: {e}")
        return False

# Test port 5432
print("\nTesting connection on port 5432...")
test_connection(5432)

# Test port 5433
print("\nTesting connection on port 5433...")
test_connection(5433)

# Test port 4532
print("\nTesting connection on port 4532...")
test_connection(4532) 