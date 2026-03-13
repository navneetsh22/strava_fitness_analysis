import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import random
df=[pd.read_csv(file) for file in glob.glob("data/*.csv")]
for i in range(len(df)):
    df[i].columns= df[i].columns.str.strip().str.lower()
print(df[i].info())
df=pd.merge(df[0],df[17], on="id" , how = "outer")

group1 = df['totalsteps']
group2 = df['activitydate']
stat, p_test = ttest_ind(group1, group2)
print("t-static" ,stat)
print("p-value", p_test)
