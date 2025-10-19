import requests
from bs4 import BeautifulSoup
import csv

# URL of the website
url = "https://www.worldometers.info/gdp/us-gdp/"

# Send a GET request to the website
response = requests.get(url)
response.raise_for_status()

# Parse the HTML content
soup = BeautifulSoup(response.text, "html.parser")

# Locate the table
table = soup.find("table")

# Extract table headers
headers = [header.text.strip() for header in table.find_all("th")]

# Extract table rows
rows = []
for row in table.find_all("tr")[1:]:  # Skip the header row
    cells = row.find_all("td")
    row_data = [cell.text.strip() for cell in cells]
    rows.append(row_data)

# Save the data to a CSV file
csv_file = "us_gdp.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(headers)  # Write headers
    writer.writerows(rows)    # Write rows

print(f"Data has been saved to {csv_file}")