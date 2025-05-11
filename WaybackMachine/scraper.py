# pip install requests beautifulsoup4
import requests
from bs4 import BeautifulSoup
import re

# Wayback Machine snapshot URL
url = "<https://web.archive.org/web/20040603144435/http://insider.espn.go.com/insider/story?id=1774429>"

# Send GET request
response = requests.get(url)

# Parse HTML content
soup = BeautifulSoup(response.text, "html.parser")

# Where to store the scraped data
nba_draft_prospects_2024 = []

# Select all table elements containing the player selection data
for table_element in soup.select("a[name] > table"):
    # Extract the title of the table
    category = table_element.select_one("tr").get_text(strip=True)

    # Where to store the player info for the current category
    players = []

    # Scrape player info from all rows
    row_elements = table_element.select("tr")[2:]  # Skip title and header
    for row_element in row_elements:
        col_elements = row_element.select("td")
        if len(col_elements) == 4:
            rank = col_elements[0].get_text(strip=True).rstrip(".")
            name = col_elements[1].get_text(strip=True)
            hwage = col_elements[2].get_text(strip=True)
            school_country = col_elements[3].get_text(strip=True)

            # Extract height, weight, and age from the aggregated text field
            match = re.match(r"(?P<height>\d+-\d+)/(?P<weight>\d+)\s*lbs\s*-\s*(?P<age>\d+)\s*yrs", hwage)
            if match:
                height = match.group("height")
                weight = match.group("weight")
                age = match.group("age")
            else:
                # Fallback logic in case format is unexpected
                height = None
                weight = None
                age = None

            # Populate a player info with the scraped data
            # and append it to the list
            player = {
                "rank": int(rank),
                "name": name,
                "height": height,
                "weight": weight,
                "age": age,
                "school_country": school_country
            }
            players.append(player)

    # Populate the NBA draft data for 2024
    nba_draft_prospects_2024.append({
        "category": category,
        "players": players
    })

    # Export/Analyze/Visualize the scraped data...