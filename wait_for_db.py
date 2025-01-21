import time
import psycopg2
from django.db import connections
from django.db.utils import OperationalError

def wait_for_db():
    db_conn = None
    print("Waiting for the database...")
    while not db_conn:
        try:
            db_conn = connections['default']
            print("Database is ready!")
        except OperationalError:
            print("Database is not ready, retrying in 1 second...")
            time.sleep(1)
