
________________________________________
📊 Strava Fitness Activity Analysis
1. Project Overview
This project analyzes fitness activity data to understand the relationship between physical activity and health metrics. The analysis explores how daily activity such as steps and distance relate to BMI, weight, and behavioral patterns.
The project demonstrates a complete data analytics pipeline, including data cleaning, statistical analysis, database storage, and dashboard visualization.
Tools used:
•	Python
•	Pandas
•	PostgreSQL
•	Microsoft Power BI
________________________________________
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
2. Objectives
The main objectives of this project were:
•	Analyze daily physical activity patterns
•	Study the relationship between steps and BMI
•	Identify weekly activity behavior
•	Evaluate device tracking reliability
•	Create an interactive dashboard for insights
________________________________________
3. Dataset Description
The dataset contains information about user fitness activity including:
Column	Description
Id	User identifier
ActivityDate	Date of activity
ActivityDay	Day of the week
TotalSteps	Total steps walked
TotalDistance	Total distance travelled
TrackerDistance	Distance recorded by tracker
WeightKg	User weight
BMI	Body Mass Index
IsManualReport	Whether activity was manually reported
LogId	Activity log identifier
________________________________________
4. Data Cleaning and Preparation
Data preprocessing was performed using Python.
Steps included:
Handling data types
df["ActivityDate"] = pd.to_datetime(df["ActivityDate"])
df["IsManualReport"] = df["IsManualReport"].astype(bool)
Handling missing values
•	Checked for null values
•	Removed or imputed inconsistent records
Merging datasets
Multiple CSV files were merged into a single dataset using Pandas.
df = pd.concat(dfs, ignore_index=True)
________________________________________
5. Exploratory Data Analysis (EDA)
EDA helped understand patterns in activity data.
Key analyses performed:
•	Distribution of daily steps
•	Trend of activity over time
•	Relationship between steps and BMI
•	Activity variation across weekdays
Example visualization:
Scatter plot:
Steps vs BMI
Histogram:
Distribution of Total Steps
________________________________________
6. Hypothesis Testing
Statistical tests were conducted to validate relationships in the dataset.
Hypothesis Test 1
Steps vs BMI
Test used: Pearson Correlation
Null Hypothesis:
There is no relationship between TotalSteps and BMI.
Result:
•	Correlation = -0.091
•	p-value < 0.05
Conclusion:
There is a statistically significant but very weak negative relationship between daily steps and BMI.
 
________________________________________
Hypothesis Test 2
Steps vs Weight
Test used: Pearson Correlation
Purpose:
To determine if increased physical activity relates to lower body weight.
 
________________________________________
Hypothesis Test 3
Distance vs Steps
Purpose:
To validate the consistency between step counts and recorded distance.
Expected result:
Strong positive correlation
 .
________________________________________



Hypothesis Test 4
Steps across Weekdays
Test used: ANOVA
Purpose:
To identify whether physical activity varies across different days of the week.

 
________________________________________
Hypothesis Test 5
Relationship between steps and calories burned
 


7. Database Storage
Cleaned data was loaded into PostgreSQL for further analysis.
Example code:
df.to_sql(
    "merged_table",
    engine,
    if_exists="replace",
    index=False
)
________________________________________
8. SQL Analysis
Several analytical queries were created to support dashboard insights.
Example query:
Average steps by weekday:
CREATE VIEW avg_daily_steps AS
SELECT activityday,
AVG(totalsteps) AS avg_steps
FROM fitness_activity
GROUP BY activityday;
BMI category analysis:
SELECT
CASE
WHEN bmi < 18.5 THEN 'Underweight'
WHEN bmi < 25 THEN 'Normal'
WHEN bmi < 30 THEN 'Overweight'
ELSE 'Obese'
END AS bmi_category,
AVG(totalsteps)
FROM fitness_activity
GROUP BY bmi_category;

Daily activity summary:


CREATE OR REPLACE VIEW strava.daily_activity_summary
 AS
 SELECT activitydate,
    sum(totalsteps) AS total_steps,
    avg(totaldistance) AS avg_distance,
    avg(bmi) AS avg_bmi
   FROM merged_table
  GROUP BY activitydate;

Average BMI:

CREATE OR REPLACE VIEW strava.avg_bmi
 AS
 SELECT avg(bmi) AS avg
   FROM merged_table;

Views were created to simplify dashboard integration.
________________________________________
9. Power BI Dashboard
The cleaned dataset and SQL views were connected to Power BI for visualization.
KPI Metrics
•	Average Daily Steps
•	Average BMI
•	Average Weight
•	Total Distance Walked
Visualizations
•	Steps by weekday
•	Steps vs BMI scatter plot
•	BMI category analysis
•	Activity trend over time
The dashboard allows interactive filtering and exploration of fitness behavior.
 
________________________________________
 
 
 
 
 

 
 

10. Key Insights
Important findings from the analysis:
•	There is a very weak negative correlation between steps and BMI.
•	Physical activity shows variation across weekdays.
•	Distance and steps are strongly correlated, confirming tracking accuracy.
•	Some activities are manually logged, which may introduce reporting bias.
______________________________________