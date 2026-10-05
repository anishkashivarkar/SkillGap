import pandas as pd

df = pd.read_parquet("job_skill_set.parquet")

print("Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

print("\nSample job skill sets:")

for i in range(5):
    print(f"\nJob {i + 1}:")
    print(df.loc[i, "job_skill_set"])