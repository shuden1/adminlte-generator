import os
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Set up the Selenium driver
options = Options()
service = Service(executable_path=r"C:\Python3\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('ParkerScripts/clutch.csv')

# Iterate over the rows of the DataFrame
for index, row in df.iterrows():
    # Get the URL from the 'url' column
    url = row['url']

    # Navigate to the URL
    driver.get(url)

    # Get the page source
    page_source = driver.page_source

    # Save the page source to a temporary HTML file
    with open('temp.html', 'w', encoding='utf-8') as f:
        f.write(page_source)

    # Parse the HTML file with BeautifulSoup
    with open('temp.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Locate the required element
    element = soup.select_one('.profile-quick-menu__visit-website a')
    href = element['href'] if element else None

    # Save the 'href' attribute into the 'website' column
    df.loc[index, 'website'] = href
    df.to_csv("D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\ParkerScripts\\clutch.csv", index=False)

    # Delete the temporary HTML file
    os.remove('temp.html')

# Quit the driver
driver.quit()
