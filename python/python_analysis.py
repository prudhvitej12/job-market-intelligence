import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tonystark1@",
    database="job_market_intelligence"
)

print("Connected to MySQL successfully!")

# Load jobs data into Pandas DataFrame
query = "SELECT * FROM jobs"

df = pd.read_sql(query, connection)

# Display the data
print("\nJob Market Data:")
print(df)

# Display basic information
print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

# Most common job titles using Python
job_title_counts = df["job_title"].value_counts()

print("\nMost Common Job Titles:")
print(job_title_counts)

# Create job title chart
job_titles = job_title_counts.index
job_counts = job_title_counts.values

plt.figure(figsize=(10, 6))
plt.bar(job_titles, job_counts)
plt.xlabel("Job Title")
plt.ylabel("Number of Jobs")
plt.title("Most Common Job Titles")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Jobs by location using Python
location_counts = df["location"].value_counts()

print("\nJobs by Location:")
print(location_counts)

# Jobs by location using Python
location_counts = df["location"].value_counts()

print("\nJobs by Location:")
print(location_counts)

# Create jobs by location chart
locations = location_counts.index
location_jobs = location_counts.values

plt.figure(figsize=(10, 6))
plt.bar(locations, location_jobs)
plt.xlabel("Location")
plt.ylabel("Number of Jobs")
plt.title("Jobs by Location")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
# Jobs by Location
location_counts = df["location"].value_counts()

print("\nJobs by Location:")
print(location_counts)


# Salary Analysis using Python
print("\nSalary Data:")
print(df["salary"])

df["min_salary"] = df["salary"].str.extract(r"(\d+)-").astype(float)
df["max_salary"] = df["salary"].str.extract(r"-(\d+)").astype(float)

df["average_salary"] = (df["min_salary"] + df["max_salary"]) / 2

print("\nSalary Analysis:")
print(df[["job_title", "salary", "average_salary"]])

print("\nOverall Average Salary:")
print(df["average_salary"].mean())
# Salary Analysis Chart
plt.figure(figsize=(10, 6))

plt.bar(df["job_title"], df["average_salary"])

plt.xlabel("Job Title")
plt.ylabel("Average Salary (LPA)")
plt.title("Average Salary by Job Title")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
# Minimum and Maximum Salary by Job Title
salary_range = df.groupby("job_title")[["min_salary", "max_salary"]].mean()

print("\nSalary Range by Job Title:")
print(salary_range)

plt.figure(figsize=(10, 6))

x = range(len(salary_range))

plt.bar(x, salary_range["min_salary"], width=0.4, label="Minimum Salary")
plt.bar(
    [i + 0.4 for i in x],
    salary_range["max_salary"],
    width=0.4,
    label="Maximum Salary"
)

plt.xlabel("Job Title")
plt.ylabel("Salary (LPA)")
plt.title("Minimum vs Maximum Salary by Job Title")
plt.xticks([i + 0.2 for i in x], salary_range.index, rotation=45)
plt.legend()

plt.tight_layout()
plt.show()
# Overall Salary Statistics

print("\nOverall Salary Statistics:")

print("Lowest Salary:", df["min_salary"].min(), "LPA")
print("Highest Salary:", df["max_salary"].max(), "LPA")
print("Average Salary:", df["average_salary"].mean(), "LPA")
# Experience Level Analysis

experience_counts = df["experience"].value_counts()

print("\nJobs by Experience Level:")
print(experience_counts)

plt.figure(figsize=(10, 6))

plt.bar(experience_counts.index, experience_counts.values)

plt.xlabel("Experience Level")
plt.ylabel("Number of Jobs")
plt.title("Jobs by Experience Level")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
# Company Analysis

company_counts = df["company"].value_counts()

print("\nJobs by Company:")
print(company_counts)

plt.figure(figsize=(10, 6))

plt.bar(company_counts.index, company_counts.values)

plt.xlabel("Company")
plt.ylabel("Number of Jobs")
plt.title("Jobs by Company")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
