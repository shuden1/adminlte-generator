import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import json
import threading

def scrape_jobs():
    target_html_file = sys.argv[1]  # The HTML file path is expected as the first command-line argument.

    # WebDriver setup with headless Chrome
    profile_folder_path = f"D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\chrome_profile\\{str(threading.get_ident())}"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-data-dir={profile_folder_path}")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    service = Service(executable_path=r"C:\Python3\chromedriver.exe")
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(f"file:///{target_html_file}")

    job_listings = []

    # Attempting different common selectors for robustness
    selectors = [
        {"title": "h2 a", "url": "h2 a"},
        {"title": ".job-title", "url": ".job-title a"},
        {"title": "a.job-title", "url": "a.job-title"},
        {"title": ".job-listing a", "tmpURL": ".job-listing a"},
        {"title": ".opening a", "url": ".opening a[href]"},
        {"title": "article > a", "url": "article > a[href]"}
    ]

    for selector in selectors:
        elements = driver.find_elements(By.CSS_SELECTOR, selector["title"])
        for element in elements:
            title = element.text.strip()
            url = element.get_attribute("href") if "url" in selector else ""
            if title and url:  # Both title and URL must be non-empty
                job_listings.append({"Job-title": title, "URL": url})
        if job_listings:  # Break if any job listing was found
            break
    
    driver.quit()
    return job_listings

if __name__ == "__main__":
    results = scrape_jobs()
    print(json.dumps(results))