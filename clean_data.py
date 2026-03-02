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
    print(f"DataFrame {i+1} info:")
    print(df.info())
    dfs[i].head()
    dfs[i].describe()

    print(f"\nCleaning DataFrame {i+1}")
    
    # Remove extra spaces from column names
    dfs[i].columns = dfs[i].columns.str.strip()
    
    # Remove extra spaces from string values
    dfs[i] = dfs[i].apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    
    # Convert numeric columns
    if "sales" in dfs[i].columns:
        dfs[i]["sales"] = pd.to_numeric(dfs[i]["sales"], errors="coerce")
    
    # Convert date columns
    if "date" in dfs[i].columns:
        dfs[i]["date"] = pd.to_datetime(dfs[i]["date"], errors="coerce")
    
    # Save cleaned dataframe back
    dfs[i] = df
    print(f"DataFrame {i+1} cleaned successfully.")
    print(f"DataFrame {i+1} info:")
    print(dfs[i].info())
    print(f"DataFrame {i+1} head:")
    print(dfs[i].head())
    

    


    