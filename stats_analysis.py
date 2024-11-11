# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Load the data
df = pd.read_csv('ms_data_combined.csv')

# Analyze walking speed:
## Multiple regression with education and age
mdl = smf.ols('walking_speed ~ age + education_level', data=df).fit()
mdl.summary()

## Account for repeated measures
mixed_mdl = smf.mixedlm('walking_speed ~ age + education_level', df, groups=df['patient_id']).fit()
mixed_mdl.summary()

## Test for significant trends
age_walking_correlation, p_value = stats.pearsonr(df['age'], df['walking_speed'])
print(f"\nCorrelation: {age_walking_correlation}, p-value: {p_value}")

# Analyze costs:
## Simple analysis of insurance type effect
## Basic statistics
cost_insurance = df.groupby('insurance_type')['visit_cost'].agg(['mean', 'std'])
print("\nSimple analysis of insurance type effect:\n", cost_insurance)
## Box plots and basic statistics
df = df.sort_values('insurance_type')
plt.figure(figsize=(10, 6))
sns.boxplot(x='insurance_type', y='visit_cost', data=df)
plt.xlabel("Insurance")
plt.ylabel("Cost / Visit")
plt.title("Visiting Cost by Insurance")
plt.show()
## Calculate effect sizes
### Set the unique insurance groups
insurance_groups = df['insurance_type'].unique()

### Calculate Cohen's d between each pair of insurance types
for i, insurance_a in enumerate(insurance_groups):
    for insurance_b in insurance_groups[i+1:]:
        # Select visit_cost data for each specific insurance group
        group_a = df[df['insurance_type'] == insurance_a]['visit_cost']
        group_b = df[df['insurance_type'] == insurance_b]['visit_cost']
        # Set the sample size for each group
        nx = len(group_a)
        ny = len(group_b)
        # Calculate the mean of each group
        mean_a = np.mean(group_a)
        mean_b = np.mean(group_b)
        # Calculate the variance of each group (using sample variance, ddof=1)
        var_a = np.var(group_a, ddof=1)
        var_b = np.var(group_b, ddof=1)
        # Calculate the pooled standard deviation
        pooled_std = np.sqrt(((nx - 1) * var_a + (ny - 1) * var_b) / (nx + ny - 2))
        # Calculate Cohen's d for effect size
        effect_size = (mean_a - mean_b) / pooled_std
        # Print the results
        print(f"Cohen's d comparing {insurance_a} and {insurance_b}: {effect_size}")

# Advanced analysis:
## Education age interaction effects on walking speed
interaction_mdl = smf.ols('walking_speed ~ education_level * age', data=df).fit()
print("\nInteraction Model:\n", interaction_mdl.summary())
## Control for relevant confounders
confounder_mdl = smf.ols('walking_speed ~ education_level * age + insurance_type*visit_cost', data=df).fit()
print("\nAdjusted Confounder Model:\n", confounder_mdl.summary())