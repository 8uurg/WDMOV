import time
import psycopg2
import datetime

conn = psycopg2.connect(user="postgres", host="db")

while True:
    currcur = conn.cursor()
    currcur.execute("""
        SELECT avg(CASE WHEN punctuality > 0 THEN punctuality ELSE 0 END) 
        FROM tripstatus 
        WHERE punctuality IS NOT NULL 
        AND timestamp > now() - interval '5 minutes';
    """)
    print(f"[{datetime.datetime.now()}] Current average delay is {currcur.fetchone()[0]} seconds.")
    currcur.close()
    time.sleep(5)