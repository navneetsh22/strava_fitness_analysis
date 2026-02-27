import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
from statsmodels.tsa.seasonal import seasonal_decompose 
files = glob.glob('data/*.csv')
dfs = []
for file in files:
    df = pd.read_csv(file)
    dfs.append(df) 
for i,df in enumerate(dfs):
    print(f"\nDataFrame {i+1}")
    df.columns = df.columns.str.strip()

    print(f"\nCleaning DataFrame {i+1}")
    
    # Remove extra spaces from column names
    df.columns = df.columns.str.strip()
    
    # Remove extra spaces from string values
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    
    # Convert numeric columns
    if "sales" in df.columns:
        df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
    
    # Convert date columns
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    
    # Save cleaned dataframe back
    dfs[i] = df
    print(f"DataFrame {i+1} cleaned successfully.")
    print(f"DataFrame {i+1} info:")
    print(df.info())
    

    


    