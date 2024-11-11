# Import libraries
import pandas as pd
import numpy as np
from datetime import datetime


# Load and structure the data:
## Read the processed CSV file
df = pd.read_csv('ms_data.csv')
## Convert visit_date to datetime
df['visit_date'] = pd.to_datetime(df['visit_date'])
## Sort by patient_id and visit_date
df.sort_values(by=['patient_id', 'visit_date'], inplace=True)

# Add insurance information:
## Read insurance types from insurance.lst
insurance_list = pd.read_csv('insurance.lst')['insurance_type'].tolist()
## Randomly assign (but keep consistent per patient_id)
np.random.seed(42)
### Initialize an empty dictionary for insurance mapping
insurance_mapping = {}
### Iterate over unique patient IDs and assign a random insurance type to each
for patient_id in df['patient_id'].unique():
    insurance_mapping[patient_id] = np.random.choice(insurance_list)
### Map the insurance type to the data based on patient_id
df['insurance_type'] = df['patient_id'].map(insurance_mapping)

## Generate visit costs based on insurance type:
## Different plans have different effects on cost
## Add random variation
visit_cost = {'A': 100, 'B': 300, 'C': 500}
df['visit_cost'] = df['insurance_type'].map(visit_cost) + np.random.normal(100, 10, len(df))

## Check the data type, data distribution, and Handle missing data
df.info()
df.describe()
## Convert the data type (Note: There is no missing value.)
### education_level: obejct -> category
df['education_level'] = df['education_level'].astype('category')
### Check the data types
print(df.dtypes)

# Save the data
df.to_csv('ms_data_combined.csv')


# Calculate summary statistics:
## Mean walking speed by education level
mean_walking_by_edu = df.groupby('education_level')['walking_speed'].mean()
print("Mean Walking Speed by Education Level:\n", mean_walking_by_edu)
## Mean costs by insurance type
mean_cost_by_insurance = df.groupby('insurance_type')['visit_cost'].mean()
print("\nMean Visit Cost by Insurance Type:\n", mean_cost_by_insurance)
## Age effects on walking speed
correlation_age_walking = df[['age', 'walking_speed']].corr().iloc[0, 1]
print("\nCorrelation between Age and Walking Speed:", correlation_age_walking)
## Consider seasonal variations in the data
df['month'] = df['visit_date'].dt.month
mean_walking_speed_by_month = df.groupby('month')['walking_speed'].mean()
print("\nMean Walking Speed by Month:", mean_walking_speed_by_month)