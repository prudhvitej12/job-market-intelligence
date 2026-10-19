import mysql.connector

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tonystark1@",
    database="job_market_intelligence"
)

print("Connected to MySQL successfully!")

# Create cursor
cursor = connection.cursor()

# Get all job data
cursor.execute("SELECT * FROM jobs")

# Fetch results
rows = cursor.fetchall()

# Display data
for row in rows:
    print(row)

# Job count by job title
cursor.execute("""
    SELECT job_title, COUNT(*) AS job_count
    FROM jobs
    GROUP BY job_title
    ORDER BY job_count DESC
""")

job_counts = cursor.fetchall()

print("\nJob Count by Job Title:")
for job in job_counts:
    print(job)


# Create chart
import matplotlib.pyplot as plt

titles = [job[0] for job in job_counts]
counts = [job[1] for job in job_counts]

plt.figure(figsize=(10, 6))
plt.bar(titles, counts)
plt.xlabel("Job Title")
plt.ylabel("Number of Jobs")
plt.title("Job Market by Job Title")
plt.xticks(rotation=45)
plt.tight_layout()


# Average salary by job title
salary_query = """
SELECT
    job_title,
    AVG(
        (
            CAST(SUBSTRING_INDEX(salary, '-', 1) AS DECIMAL(10,2))
            +
            CAST(
                SUBSTRING_INDEX(
                    SUBSTRING_INDEX(salary, '-', -1),
                    ' ', 1
                ) AS DECIMAL(10,2)
            )
        ) / 2
    ) AS avg_salary
FROM jobs
GROUP BY job_title
ORDER BY avg_salary DESC
"""

cursor.execute(salary_query)

salary_data = cursor.fetchall()

print("\nAverage Salary by Job Title:")
for row in salary_data:
    print(row)

# Create salary chart
salary_titles = [row[0] for row in salary_data]
avg_salaries = [row[1] for row in salary_data]

plt.figure(figsize=(10, 6))
plt.bar(salary_titles, avg_salaries)
plt.xlabel("Job Title")
plt.ylabel("Average Salary (LPA)")
plt.title("Average Salary by Job Title")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Jobs by location
location_query = """
SELECT location, COUNT(*) AS job_count
FROM jobs
GROUP BY location
ORDER BY job_count DESC
"""

cursor.execute(location_query)

location_data = cursor.fetchall()

print("\nJob Count by Location:")
for row in location_data:
    print(row)

# Create location chart
locations = [row[0] for row in location_data]
location_counts = [row[1] for row in location_data]

plt.figure(figsize=(10, 6))
plt.bar(locations, location_counts)
plt.xlabel("Location")
plt.ylabel("Number of Jobs")
plt.title("Job Market by Location")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Jobs by experience level
experience_query = """
SELECT experience, COUNT(*) AS job_count
FROM jobs
GROUP BY experience
ORDER BY job_count DESC
"""

cursor.execute(experience_query)

experience_data = cursor.fetchall()

print("\nJob Count by Experience Level:")
for row in experience_data:
    print(row)

# Create experience chart
experiences = [row[0] for row in experience_data]
experience_counts = [row[1] for row in experience_data]

plt.figure(figsize=(10, 6))
plt.bar(experiences, experience_counts)
plt.xlabel("Experience Level")
plt.ylabel("Number of Jobs")
plt.title("Job Market by Experience Level")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Average salary by location
location_salary_query = """
SELECT
    location,
    AVG(
        (
            CAST(SUBSTRING_INDEX(salary, '-', 1) AS DECIMAL(10,2))
            +
            CAST(
                SUBSTRING_INDEX(
                    SUBSTRING_INDEX(salary, '-', -1),
                    ' ', 1
                ) AS DECIMAL(10,2)
            )
        ) / 2
    ) AS avg_salary
FROM jobs
GROUP BY location
ORDER BY avg_salary DESC
"""

cursor.execute(location_salary_query)

location_salary_data = cursor.fetchall()

print("\nAverage Salary by Location:")
for row in location_salary_data:
    print(row)

# Create salary by location chart
locations = [row[0] for row in location_salary_data]
avg_location_salaries = [row[1] for row in location_salary_data]

plt.figure(figsize=(10, 6))
plt.bar(locations, avg_location_salaries)
plt.xlabel("Location")
plt.ylabel("Average Salary (LPA)")
plt.title("Average Salary by Location")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Average salary by experience level
experience_salary_query = """
SELECT
    experience,
    AVG(
        (
            CAST(SUBSTRING_INDEX(salary, '-', 1) AS DECIMAL(10,2))
            +
            CAST(
                SUBSTRING_INDEX(
                    SUBSTRING_INDEX(salary, '-', -1),
                    ',', 1
                ) AS DECIMAL(10,2)
            )
        ) / 2
    ) AS avg_salary
FROM jobs
GROUP BY experience
ORDER BY avg_salary DESC
"""

cursor.execute(experience_salary_query)

experience_salary_data = cursor.fetchall()

print("\nAverage Salary by Experience Level:")
for row in experience_salary_data:
    print(row)

# Create experience salary chart
experience_levels = [row[0] for row in experience_salary_data]
avg_experience_salaries = [row[1] for row in experience_salary_data]

plt.figure(figsize=(10, 6))
plt.bar(experience_levels, avg_experience_salaries)
plt.xlabel("Experience Level")
plt.ylabel("Average Salary (LPA)")
plt.title("Average Salary by Experience Level")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Figure 7: Most Demanded Skills

skills_query = """
SELECT
    TRIM(skill) AS skill,
    COUNT(*) AS demand
FROM jobs
JOIN JSON_TABLE(
    CONCAT(
        '["',
        REPLACE(skills, ', ', '","'),
        '"]'
    ),
    '$[*]' COLUMNS (
        skill VARCHAR(100) PATH '$'
    )
) AS skill_data
GROUP BY TRIM(skill)
ORDER BY demand DESC
"""

cursor.execute(skills_query)

skills_data = cursor.fetchall()

print("\nMost Demanded Skills:")
for row in skills_data:
    print(row)

# Create skills chart
skills = [row[0] for row in skills_data]
skill_demand = [row[1] for row in skills_data]

plt.figure(figsize=(10, 6))
plt.bar(skills, skill_demand)
plt.xlabel("Skill")
plt.ylabel("Number of Jobs")
plt.title("Most Demanded Skills")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Job type distribution
job_type_query = """
SELECT
    job_type,
    COUNT(*) AS job_count
FROM jobs
GROUP BY job_type
ORDER BY job_count DESC
"""

cursor.execute(job_type_query)

job_type_data = cursor.fetchall()

print("\nJob Type Distribution:")
for row in job_type_data:
    print(row)

# Create job type chart
job_types = [row[0] for row in job_type_data]
job_type_counts = [row[1] for row in job_type_data]

plt.figure(figsize=(10, 6))
plt.bar(job_types, job_type_counts)
plt.xlabel("Job Type")
plt.ylabel("Number of Jobs")
plt.title("Job Type Distribution")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Close connection
cursor.close()
connection.close()
print("Connection closed.")
