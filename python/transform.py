import pandas as pd
import glob
import os
from sqlalchemy import create_engine

def load_data(df):
    engine = create_engine(f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@localhost:5432/{os.getenv('DB_NAME')}"
)
    df.to_sql(
        name="merged_table",
        con = engine,
        if_exists="replace",
        index=False
)
print("Data loaded successfully")

    


