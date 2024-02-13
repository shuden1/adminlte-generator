import json
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By

# Read the target HTML file name from the console command argument
html_file_path = sys.argv[1]

# Initialize a Chrome webdriver and configure options if needed
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Open the local HTML file
driver = webdriver.Chrome(options=options)
driver.get(f"file:///{html_file_path}")

# no job openings found, an empty list will be returned
job_listings = []

# Convert the job listings to a JSON string
job_listings_json = json.dumps(job_listings)

# Output the JSON string
print(job_listings_json)

# Close the driver
driver.quit()