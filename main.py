# Web scrapper for ucsc course catalog

# Breakdown: Year -> Major Type (Undergrad, Minor, PHD, etc) -> Program -> Major -> Courses  -> Prereqs

import requests
from bs4 import BeautifulSoup

home = "https://catalog.ucsc.edu"
base_url = "https://catalog.ucsc.edu/en/current/general-catalog/academic-programs/"
page = requests.get(base_url)

major_types = input("Enter the major type you want to search for(bachelors/phd/masters-degrees or undergraduate minors): ")
base_url += major_types + "/"


# major = input("Enter the major you want to search for: ")
page = requests.get(base_url)
major_list = BeautifulSoup(page.content, "html.parser")

majors = major_list.find_all('a')
major_links = []
for major in majors:
    if 'href' in major.attrs:  # Ensure the 'href' attribute exists
        major_links.append({
            "name": major.get_text(strip=True),  # Major name (with degree type)
            "link": major['href']
        })

# Function to find a specific major and differentiate by degree
def find_major(input_major, degree_type=None):
    results = []
    for major in major_links:
        if input_major.lower() in major['name'].lower():  # Partial match on major name
            if degree_type:  # Check for degree type if specified
                if degree_type.lower() in major['name'].lower():
                    results.append(major)
            else:
                results.append(major)
    return results

# User input for major and optional degree type
user_input_major = input("Enter the name of the major to search for: ").strip()
user_input_degree = input("Specify degree type (B.A. / B.S.), or press Enter to skip: ").strip()

# Find and display the major(s)
results = find_major(user_input_major, user_input_degree)
major_link = ""
if results:
    for result in results:
        major_page = home  + result['link']
        print(result['name'] + ": " + major_page)
        print(major_page)
else:
    print("Major not found.")


major_table = requests.get(major_page)
major_table = BeautifulSoup(major_table.content, "html.parser")
tables = major_table.find_all('table')

# Function to parse tables
def parse_course_table(table):
    course_data = []
    rows = table.find_all('tr')  # Find all rows
    for row in rows:
        cols = row.find_all('td')  # Find all columns
        if len(cols) >= 3:  # Ensure valid row
            course_number = cols[0].get_text(strip=True)
            course_link = cols[0].find('a')['href'] if cols[0].find('a') else None
            course_title = cols[1].get_text(strip=True)
            credits = cols[2].get_text(strip=True)
            course_data.append({
                "course_number": course_number,
                "course_title": course_title,
                "credits": credits,
                "link": course_link
            })
    return course_data

# Parse all tables and store results
all_courses = []
for table in tables:
    all_courses.extend(parse_course_table(table))

# Display parsed data
for course in all_courses:
    print(course['course_number'])

html_cutoff = major_page.split("Entering")[0]  # Stop parsing after "Entering"
soup_cutoff = BeautifulSoup(html_cutoff, "html.parser")
first_table_cutoff = soup_cutoff.find('table')  # Find the first table before "Entering"

# Parse the table
if first_table_cutoff:
    parsed_courses = major_table(first_table_cutoff)
    for course in parsed_courses:
        print(f"Course: {course['course_number']}, Title: {course['course_title']}, "
              f"Credits: {course['credits']}, Link: {course['link']}")
else:
    print("No table found before 'Entering'.")