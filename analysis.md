# Cohort Analysis

## Introduction: Part 2- Big Data Analysis

The task assigned is to: 
1. Complete the script- `3_cohort_analysis.py` using polars lazy evaluation and streaming
2. Convert the input csv to a parquet file for efficient processing
3. Filter out BMI outliers (values < 10 or > 60)
4. Group patients by BMI ranges and calculate statistics
5. Print summary statistics of the cohorts

### The Data:

First, we generated the data using `generate_large_health_data.py`. The data generated has columns for: `Pregnancies`, `Glucose`, `BloodPressure`, `SkinThickness`, `Insulin`, `BMI`, `DiabetesPedigreeFunction`, `Age`, `Outcome` & `diagnosis`. 

In our analysis, we want to get the following results:
- `bmi_range`: The BMI range (e.g., "Underweight", "Normal", "Overweight", "Obese")
- `avg_glucose`: Mean glucose level by BMI range
- `patient_count`: Number of patients by BMI range
- `avg_age`: Mean age by BMI range

## Analysis Approach:
The analysis approached used is to simply find out what patterns and groups are present in the data. We will be using polars to read the csv and write it as a parquet file before creating a lazy query to analyze the cohorts. We first filter out any anomalies in the BMI column that are < 10 or > 60. Next, we select the 'BMI', 'Glucose' and 'Age' columns of the dataframe. Then, we cut the `BMI` column into 4 groups: `Underweight, Normal, Overweight, Obese` at intervals: `[10, 18.5, 25, 30, 60]` and store this into a new column-- `bmi_range`. Finally, we use group_by on this bmi_range column and aggregate it while also creating new columns for avg_glucose (mean of Glucose per bmi_range), patient_count and avg_age (mean of Age per bmi_range). We are using a .collect() method to collect our final columns into one dataframe. By setting streaming=True, instead of processing the entire dataset all at once, which might not fit onto local memory, streaming allows us to process the dataset in numerous smaller batches, allowing us to minimize the memory use.

## Patterns Found
Cohort Analysis Summary:

shape: (4, 4)
| **bmi_range**     | **avg_glucose** | **patient_count** | **avg_age** |
|-------------------|----------------:|------------------:|------------:|
| Underweight       |      108.004737 |            664064 |    31.888848 |
| Normal            |      116.373363 |           1165360 |    32.880893 |
| Overweight        |      126.032016 |           3066409 |    33.827130 |
| Obese             |       95.195115 |             26041 |    23.980646 |

Since our features were mostly randomly generated, it is understandable that we may not get any meaningful real life insights from this data. Our data suggests that the average glucose levels and average age shows an increasing trend with BMI until they suddenly plummet on reaching the Obese group. The Obese group however only has 26041 patients compared to the other groups which have atleast 600000 patients. This could suggest that we need more data on the Obese group to be certain in our findings about relating BMI, and glucose and age.
