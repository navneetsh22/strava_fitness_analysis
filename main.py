from calendar import weekday

import psycopg2
from dotenv import load_dotenv
import os
import pandas as pd
from scipy import stats
from scipy.stats import pearsonr
import glob
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import seaborn as sns
from scipy.stats import ttest_ind
from scipy.stats import f_oneway

load_dotenv()
#file = ('dailyActivity_merged.csv','dailyCalories_merged.csv','dailyIntensities_merged.csv','dailySteps_merged.csv','heartrate_seconds_merged.csv','hourlyCalories_merged.csv','hourlyIntensities_merged.csv','hourlySteps_merged.csv','minuteCaloriesNarrow_merged.csv','minuteCaloriesWide_merged.csv','minuteIntensitiesNarrow_merged.csv','minuteIntensitiesWide_merged.csv','minuteMETsNarrow_merged.csv','minuteSleep_merged.csv','minuteStepsNarrow_merged.csv','minuteStepsWide_merged.csv','sleepDay_merged.csv','weightLogInfo_merged.csv' )
files = glob.glob("data/*.csv")
df = []
for file in files:
        data = pd.read_csv(file)
        df.append(data)

        
    
    
for i in range(len(df)):
    df[i].columns = df[i].columns.str.strip()
    df[i].columns = df[i].columns.str.lower()
    
    
df[i].duplicated().sum()
df[i].drop_duplicates(inplace=True)

df[i]["date"] = pd.to_datetime(
    df[i]["date"],
    format="%Y-%m-%d",
    errors="coerce"
)

df[i].columns = df[i].columns.str.strip()
df[i].columns = df[i].columns.str.lower()
df[17] = df[17].rename(columns={'Id': 'id'})

df[16] = df[16].drop_duplicates("id")

df[17] = df[17].drop_duplicates("id")
merged_file1 = pd.merge(df[0], df[1], on='id', how='outer')


merged_file2 = pd.merge(
    merged_file1,
    df[16][['id','sleepday']],   # select only the column you want
    on='id',
    how='left'
)
df = merged_file2.merge(df[17], on='id', how='outer')
print(df.info())


mean_steps = df['totalsteps'].mean()
median_steps = df['totalsteps'].median()
mode_steps = df['totalsteps'].mode()[0]
std_steps = df['totalsteps'].std()
variance_steps = df['totalsteps'].var()

print("Mean:", mean_steps)
print("Median:", median_steps)
print("Mode:", mode_steps)
print("Std:", std_steps)
print("Variance:", variance_steps)
Q1 = df['totalsteps'].quantile(.25)
Q3 = df['totalsteps'].quantile(.75)
Q1 = df['bmi'].quantile(.25)
Q3 = df['bmi'].quantile(.75)
IQR = Q3-Q1
df = df[(df['bmi'] >= Q1- 1.5 * IQR ) & (df['bmi']<= Q3 + 1.5 *IQR )]
Q1 = df['weightkg'].quantile(.25)
Q3 = df['weightkg'].quantile(.75)
IQR = Q3-Q1
df = df[(df['weightkg'] >= Q1- 1.5 * IQR ) & (df['weightkg']<= Q3 + 1.5 *IQR )]
Q1 = df['trackerdistance'].quantile(.25)
Q3 = df['trackerdistance'].quantile(.75)
IQR = Q3-Q1
df = df[(df['trackerdistance'] >= Q1- 1.5 * IQR ) & (df['trackerdistance']<= Q3 + 1.5 *IQR )]
Q1 = df['totaldistance'].quantile(.25)
Q3 = df['totaldistance'].quantile(.75)
IQR = Q3-Q1
df = df[(df['totaldistance'] >= Q1- 1.5 * IQR ) & (df['totaldistance']<= Q3 + 1.5 *IQR )]
print(df.info())
df['activitydate'] = pd.to_datetime (df['activitydate'])
df['activityday'] = pd.to_datetime(df['activityday'])
df['ismanualreport'] = df['ismanualreport'].map({'true':'True', 'false':'False'})


#    Steps vs BMI

# Test: Pearson Correlation

# Hypothesis
#  H₀: There is no relationship between TotalSteps and BMI
#  H₁: There is a relationship between TotalSteps and BMI

corr, p = pearsonr(df["totalsteps"], df["bmi"])

print("Correlation:", corr)
print("P value:", p)
if p<0.05:
    print("The correlation is statistically significant.")
else:
    print("The correlation is not statistically significant.")

# Pearson correlation analysis was conducted to examine the relationship between daily steps and BMI.
# The results showed a very weak negative correlation (r = -0.091).
# The relationship was statistically significant (p < 0.05), indicating that higher step counts are slightly associated with lower BMI, though the effect size is minimal.

# visualizing the relationship between TotalSteps and BMI using a scatter plot with a regression line

sns.regplot(x="totalsteps", y="bmi", data=df)

plt.title("Relationship between Total Steps and BMI")
plt.xlabel("Total Steps")
plt.ylabel("BMI")
plt.title("Relationship between Steps and BMI")
plt.show()
# Now we create BMI categories based on standard BMI classifications and visualize the distribution of total steps across these categories using a boxplot.  

df["BMI_Category"] = pd.cut(df["bmi"],
bins=[0,18.5,25,30,100],
labels=["Underweight","Normal","Overweight","Obese"])

sns.boxplot(x="BMI_Category", y="totalsteps", data=df)
plt.title("Total Steps Distribution by BMI Category")
plt.show()

# Steps vs Weight

# Test: Pearson Correlation

# Hypothesis

# H₀: TotalSteps and WeightKg are not related
# H₁: TotalSteps and WeightKg are related

corr, p = pearsonr(df["totalsteps"], df["weightkg"])

print("Correlation:", corr)
print("P value:", p)
if p<0.05:
    print("The correlation is statistically significant.")
else:
    print("The correlation is not statistically significant.")

sns.regplot(x="totalsteps", y="weightkg", data=df)

plt.title("Relationship between total Steps and Weight kg")
plt.show()

# Distance vs Steps

# Test: Pearson Correlation

# Hypothesis

# H₀: No relationship between steps and distance
# H₁: Steps and distance are related
corr, p = pearsonr(df["totalsteps"], df["totaldistance"])
print("Correlation:", corr)
print("P value:", p)
if p<0.05:
    print("The correlation is statistically significant.")
else:
    print("The correlation is not statistically significant.")
sns.regplot(x="totalsteps", y="totaldistance", data=df)
plt.title("Relationship between total Steps and total distance")
plt.show()


    
#  Weekday vs Steps

# Test: ANOVA

# We compare steps across multiple groups (days).

# Hypothesis

# H₀: Average steps are same for all days
# H₁: At least one day has different steps



mon = df[df["activityday"]=="Monday"]["totalsteps"]
tue = df[df["activityday"]=="Tuesday"]["totalsteps"]
wed = df[df["activityday"]=="Wednesday"]["totalsteps"]
thu = df[df["activityday"]=="Thursday"]["totalsteps"]
fri = df[df["activityday"]=="Friday"]["totalsteps"]
sat = df[df["activityday"]=="Saturday"]["totalsteps"]
sun = df[df["activityday"]=="Sunday"]["totalsteps"]


# Perform one-way ANOVA

f_statistic, p_value = stats.f_oneway(mon, tue, wed, thu, fri, sat, sun)

print(f"F-statistic: {f_statistic:.4f}")
print(f"P-value: {p_value:.4f}")

# Interpretation (alpha = 0.05)
alpha = 0.05
if p_value < alpha:
    print("Reject null hypothesis: Group means differ significantly.")
else:
    print("Fail to reject null: No significant difference in means.")

sns.boxplot(x="activityday", y="totalsteps", data=df)

plt.title("Total Steps Distribution by Day")
plt.show()






# BMI Groups vs Steps

# Test: ANOVA

# Create BMI categories.

df["BMI_Category"] = pd.cut(df["bmi"],
bins=[0,18.5,25,30,100],
labels=["Underweight","Normal","Overweight","Obese"])
sns.boxplot(x="BMI_Category", y="totalsteps", data=df)
plt.title("Total Steps Distribution by BMI Category")
plt.show()


# Weight vs BMI

# Test: Pearson Correlation
corr, p = pearsonr(df["weightkg"], df["bmi"])
print("Correlation:", corr)
print("P value:", p)
if p<0.05:
    print("The correlation is statistically significant.")
else:
    print("The correlation is not statistically significant.")
sns.regplot(x="bmi", y="weightkg", data=df)

plt.title("Relationship between BMI and Weight kg")
plt.show()


# Activity by weekday

sns.boxplot(x="activityday", y="totalsteps", data=df)
plt.title("Total Steps Distribution by Day")
plt.show()

# Steps vs Calories burned

sns.regplot(x="totalsteps", y="calories_x", data=df)
plt.title("Relationship between Steps and Calories Burned")
plt.show()



# Sedentary minutes vs steps

sns.regplot(x="sedentaryminutes", y="totalsteps", data=df)
plt.title("Relationship between Sedentary Minutes and Total Steps")
plt.show()
import pandas as pd

df["sleepday"] = pd.to_datetime(df["sleepday"], format="%m/%d/%Y %I:%M:%S %p")

engine = create_engine(f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@localhost:5432/{os.getenv('DB_NAME')}")
df.to_sql(
    name="merged_table",
    con = engine,
    if_exists="append",
    index=False
)
print("data loaded successfully")

