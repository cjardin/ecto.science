import psycopg2
from psycopg2.extras import RealDictCursor

def get_db():
    return psycopg2.connect(host="10.0.1.3",database="ecto", user="ray" ,password="staypuff")

def get_cursor(db):
    return db.cursor(cursor_factory=RealDictCursor)

