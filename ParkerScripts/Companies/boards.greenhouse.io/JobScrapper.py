from selenium import webdriver
from selenium.webdriver.chrome.service import Service


# Set up WebDriver (using Chrome in this example)
driver = webdriver.Chrome()

target_html_file_name = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\ParkerScripts\\Companies\\boards.greenhouse.io\\HTMLs\\template.html"
# Open a webpage
driver.get("https://boards.greenhouse.io/droplet/jobs/4018378007")

# Get the text of the entire body of the webpage
page_text = driver.find_element("tag name", "body").text

output_filename = "D:\\Mind\\CRA\\AI_Experiments\\Job_Crawlers\\Peter\\adminlte-generator\\ParkerScripts\\Companies\\boards.greenhouse.io\\HTMLs\\job.html"
# Print the text content
with open(output_filename, 'w', encoding='utf-8') as file:
    file.write(page_text)
# Clean up and close the browserW
driver.quit()
