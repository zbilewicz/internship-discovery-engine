import requests
import pandas as pd
from datetime import datetime
import re
from bs4 import BeautifulSoup


# Companies likely to have internships
companies = [
    "stripe",
    "databricks",
    "palantir",
    "notion",
    "asml",
    "booking"
]

all_internships = []

for company in companies:
    print(f"Checking {company}...")

    url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"

    response = requests.get(url)

    # Skip if company doesn't exist or request fails
    if response.status_code != 200:
        print(f"Skipping {company} (status {response.status_code})")
        continue

    data = response.json()

    for job in data.get("jobs", []):
        title = job["title"]
        job_id = job["id"]
        job_url = job["absolute_url"]
        location = job["location"]["name"] if job.get("location") else ""

        pattern = r"\b(intern|internship|working student|apprentice)\b"

        if re.search(pattern, title.lower()):

            # Fetch full job details
            detail_url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs/{job_id}"
            detail_response = requests.get(detail_url)

            description = ""
            if detail_response.status_code == 200:
                detail_data = detail_response.json()
                html_content = detail_data.get("content", "")
                soup = BeautifulSoup(html_content, "lxml")
                description = soup.get_text(separator=" ", strip=True)

            all_internships.append({
                "company": company,
                "title": title,
                "location": location,
                "url": job_url,
                "description_raw": description,
                "date_scraped": datetime.now()
            })

print("\nInternships found:")
for job in all_internships:
    print(job["company"], "|", job["title"], "|", job["location"])

# Save to CSV
if all_internships:
    df = pd.DataFrame(all_internships)
    df.to_csv("data/internships_raw.csv", index=False)
    print("\nSaved to data/internships_raw.csv")
else:
    print("\nNo internships found.")
