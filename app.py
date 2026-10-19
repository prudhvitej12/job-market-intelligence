import streamlit as st
import mysql.connector
import re

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Job Market Intelligence",
    page_icon="💼",
    layout="wide"
)

# -----------------------------
# MySQL Connection
# -----------------------------
def get_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
    )


# -----------------------------
# Load Jobs
# -----------------------------
def load_jobs():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            job_title,
            company,
            location,
            salary,
            experience,
            skills,
            job_type,
            posted_date
        FROM jobs
    """)

    jobs = cursor.fetchall()

    cursor.close()
    connection.close()

    return jobs


# -----------------------------
# Salary Conversion
# -----------------------------
def get_salary_range(salary):
    numbers = re.findall(r"\d+(?:\.\d+)?", str(salary))

    if len(numbers) >= 2:
        minimum = float(numbers[0])
        maximum = float(numbers[1])
        return minimum, maximum

    if len(numbers) == 1:
        value = float(numbers[0])
        return value, value

    return 0, 0


# -----------------------------
# Header
# -----------------------------
st.title("💼 Job Market Intelligence")
st.subheader("Explore Job Demand, Locations and Salary Trends")

st.write(
    "Analyze job opportunities based on job title, location, "
    "experience level and salary."
)

# -----------------------------
# Load Data
# -----------------------------
try:
    jobs = load_jobs()

except Exception as e:
    st.error("Could not connect to MySQL.")
    st.error(str(e))
    st.stop()


if not jobs:
    st.warning("No job data found in the database.")
    st.stop()


# -----------------------------
# Prepare Salary Data
# -----------------------------
for job in jobs:
    minimum, maximum = get_salary_range(job["salary"])

    job["min_salary"] = minimum
    job["max_salary"] = maximum
    job["average_salary"] = (minimum + maximum) / 2


# -----------------------------
# Dashboard Metrics
# -----------------------------
total_jobs = len(jobs)

average_salary = sum(
    job["average_salary"] for job in jobs
) / total_jobs

highest_salary = max(
    job["max_salary"] for job in jobs
)

locations = {}

for job in jobs:
    location = job["location"]

    if location not in locations:
        locations[location] = 0

    locations[location] += 1


top_location = max(
    locations,
    key=locations.get
)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Jobs", total_jobs)

with col2:
    st.metric("Average Salary", f"{average_salary:.1f} LPA")

with col3:
    st.metric("Highest Salary", f"{highest_salary:.1f} LPA")

with col4:
    st.metric("Top Job Location", top_location)


st.divider()


# -----------------------------
# Filters
# -----------------------------
st.header("🔎 Explore Jobs")

col1, col2, col3 = st.columns(3)

job_titles = sorted(
    set(job["job_title"] for job in jobs)
)

job_locations = sorted(
    set(job["location"] for job in jobs)
)

experiences = sorted(
    set(job["experience"] for job in jobs)
)


with col1:
    selected_title = st.selectbox(
        "Job Title",
        ["All"] + job_titles
    )

with col2:
    selected_location = st.selectbox(
        "Location",
        ["All"] + job_locations
    )

with col3:
    selected_experience = st.selectbox(
        "Experience",
        ["All"] + experiences
    )


# -----------------------------
# Apply Filters
# -----------------------------
filtered_jobs = jobs

if selected_title != "All":
    filtered_jobs = [
        job for job in filtered_jobs
        if job["job_title"] == selected_title
    ]

if selected_location != "All":
    filtered_jobs = [
        job for job in filtered_jobs
        if job["location"] == selected_location
    ]

if selected_experience != "All":
    filtered_jobs = [
        job for job in filtered_jobs
        if job["experience"] == selected_experience
    ]


st.write(f"### {len(filtered_jobs)} matching jobs")


# -----------------------------
# Job Results
# -----------------------------
for job in filtered_jobs:

    with st.expander(
        f"💼 {job['job_title']} | {job['company']}"
    ):

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Location:** {job['location']}")
            st.write(f"**Experience:** {job['experience']}")
            st.write(f"**Job Type:** {job['job_type']}")

        with col2:
            st.write(f"**Salary:** {job['salary']}")
            st.write(f"**Skills:** {job['skills']}")
            st.write(f"**Posted Date:** {job['posted_date']}")


st.divider()


# -----------------------------
# Jobs by Location
# -----------------------------
st.header("📍 Where Are Most Jobs?")

location_counts = {}

for job in filtered_jobs:

    location = job["location"]

    if location not in location_counts:
        location_counts[location] = 0

    location_counts[location] += 1


if location_counts:

    st.bar_chart(location_counts)

    top_filtered_location = max(
        location_counts,
        key=location_counts.get
    )

    st.success(
        f"📍 **{top_filtered_location}** has the highest number "
        f"of matching jobs."
    )


# -----------------------------
# Average Salary by Job Title
# -----------------------------
st.header("💰 Average Salary by Job Title")

salary_by_title = {}

for job in filtered_jobs:

    title = job["job_title"]

    if title not in salary_by_title:
        salary_by_title[title] = []

    salary_by_title[title].append(
        job["average_salary"]
    )


average_salary_by_title = {}

for title, salaries in salary_by_title.items():

    average_salary_by_title[title] = (
        sum(salaries) / len(salaries)
    )


if average_salary_by_title:

    st.bar_chart(average_salary_by_title)

    highest_paying_title = max(
        average_salary_by_title,
        key=average_salary_by_title.get
    )

    highest_title_salary = (
        average_salary_by_title[highest_paying_title]
    )

    st.success(
        f"💰 **{highest_paying_title}** has the highest "
        f"average salary at **{highest_title_salary:.1f} LPA**."
    )


# -----------------------------
# Salary Range
# -----------------------------
st.header("📊 Salary Range by Job")

salary_data = {}

for job in filtered_jobs:

    salary_data[
        job["job_title"]
    ] = {
        "Minimum Salary": job["min_salary"],
        "Maximum Salary": job["max_salary"]
    }


if salary_data:

    for title, values in salary_data.items():

        st.write(
            f"**{title}:** "
            f"{values['Minimum Salary']:.1f} - "
            f"{values['Maximum Salary']:.1f} LPA"
        )


# -----------------------------
# Footer
# -----------------------------
st.divider()

st.caption(
    "Job Market Intelligence | Python + MySQL"
)