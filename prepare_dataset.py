import pandas as pd
import ast
import json
import os

# Load dataset
df = pd.read_parquet("job_skill_set.parquet")


# Convert string representation into Python list
def convert_to_list(value):
    if isinstance(value, str):
        return ast.literal_eval(value)
    return value


df["job_skill_set"] = df["job_skill_set"].apply(convert_to_list)


# Normalize skills
def clean_skill(skill):
    return skill.lower().strip().replace("&", "and")


# Create complete skill vocabulary
all_skills = []

for skills in df["job_skill_set"]:
    for skill in skills:
        all_skills.append(clean_skill(skill))


skill_vocabulary = sorted(set(all_skills))


# Create data folder
os.makedirs("data", exist_ok=True)


# Save skills
with open("data/skills.json", "w", encoding="utf-8") as file:
    json.dump(skill_vocabulary, file, indent=2)


print("Dataset loaded:", len(df), "jobs")
print("Unique skills:", len(skill_vocabulary))
print("Saved to data/skills.json")
