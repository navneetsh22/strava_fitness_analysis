import psycopg2
import os
import pandas as p
conn = psycopg2.connect(
    host = os.getenv("POSTGRES_HOST"),
    database = os.getenv("POSTGRES_DB"),
    user = os.getenv("POSTGRES_USER"),
    password = os.getenv("POSTGRES_PASSWORD")
    )
print("connected succesfully")
cur = conn.cursor()
cur.executemany("insert into merged_table values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" , data)
conn.commit()
cur.close()
conn.close() 

