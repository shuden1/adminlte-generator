from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import sys
import time
import uuid
import shutil

import threading

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
from dotenv import load_dotenv
load_dotenv()

def remove_script_tags(input_html_file):
    """
    Remove all <script> tags from the input HTML file and update the file.

    Parameters:
    input_html_file (str): Path to the HTML file to be processed.
    """
    with open(input_html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    for script in soup.find_all('script'):
        script.decompose()

    with open(input_html_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))

def click_buttons(browser):
    button_counter = 0  # Initialize the button counter
    while True:
        try:
            # Find the first .company-vacancies-group__title button element that doesn't have the 'clicked' attribute
            wait = WebDriverWait(browser, 10)
            if len(browser.find_elements(By.CSS_SELECTOR, ".content--hBoUSbJDqRH4ckoAMooa")) > 0:
                # If it is, click on the ".buttons--rsxVkXYwWxeySpkbMj0J button" element
                other_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".buttons--rsxVkXYwWxeySpkbMj0J button")))
                other_button.click()
                time.sleep(5)  # Wait for the JavaScript to load additional information

            button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".company-vacancies-group__title button:not([clicked])")))

            # Add the 'clicked' attribute to the button
            browser.execute_script("arguments[0].setAttribute('clicked', 'true');", button)

            button.click()
            time.sleep(5)  # Wait for the JavaScript to load additional information
            button_counter += 1  # Increment the button counter
            print(f"Button {button_counter} clicked.")  # Print the number of the button clicked

            # Re-fetch the page source and re-parse it with BeautifulSoup
            html_content = browser.page_source
            soup = BeautifulSoup(html_content, 'html.parser')

            # Now, `soup` contains the updated HTML content
        except Exception as e:
            print(f"Error clicking button: {e}")
            break  # Break the loop if no more buttons are found or an error occurs

def get_dynamic_html(url, output_file, scrolls=2):
    options = Options()

    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())

    os.makedirs(profile_folder_path, exist_ok=True)

    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument('--remote-allow-origins="*"')
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    browser = webdriver.Chrome(service=service, options=options)

    try:
        browser.get(url)
        time.sleep(10)  # Wait for the initial page to load
        for i in range(scrolls):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait 2 seconds between scrolls

        browser.refresh()
        time.sleep(8)  # Wait for the page to load after refresh

        for i in range(scrolls):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait 2 seconds between scrolls


        click_buttons(browser)

        # Get main page source
        html_content = browser.page_source
        soup = BeautifulSoup(html_content, 'html.parser')


        iframe_elements = browser.find_elements(By.TAG_NAME, "iframe")

        # Assign a unique ID to each iframe for later identification
        for iframe in iframe_elements:
            unique_id = str(uuid.uuid4())
            browser.execute_script(f"arguments[0].setAttribute('data-unique-id', '{unique_id}');", iframe)

        # Now, reload the page content with the unique IDs applied
        # This is to ensure our BeautifulSoup object includes the iframes with their unique IDs
        main_page_content = browser.page_source
        soup = BeautifulSoup(main_page_content, 'html.parser')



        tags_to_remove = ['script', 'meta', 'style']
        # Remove specified tags
        for tag in tags_to_remove:
            for element in soup.find_all(tag):
                element.decompose()

        # Iterate through each iframe by its unique ID
        for iframe in soup.find_all('iframe', attrs={"data-unique-id": True}):
            unique_id = iframe['data-unique-id']
            src = iframe['src'] if iframe.has_attr('src') else None
            if src:
                try:
                    # Switch to the iframe using its unique ID
                    browser.switch_to.frame(browser.find_element(By.XPATH, f"//iframe[@data-unique-id='{unique_id}']"))
                    iframe_content = browser.page_source
                    iframe_soup = BeautifulSoup(iframe_content, 'html.parser')
                    new_div = soup.new_tag("div", **{"class": "replaced-iframe"})

                    iframe_body = iframe_soup.find('body')
                    if iframe_body:
                        html_content = ''.join(str(content) for content in iframe_body.contents)
                        new_div.append(BeautifulSoup(html_content, 'html.parser'))
                    # Replace the original iframe in soup with new_div
                    iframe.replace_with(new_div)

                    # Switch back to the main content
                    browser.switch_to.default_content()

                except Exception as e:
                    print(f"Error processing iframe {unique_id}: {e}")

                # Write the modified HTML content to a file
                with open(output_file, 'w', encoding='utf-8') as file:
                    file.write(str(soup))
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(str(soup))
    finally:
        browser.quit()
        remove_script_tags(output_filename)
#        if os.path.exists(profile_folder_path) and os.path.isdir(profile_folder_path):
#            shutil.rmtree(profile_folder_path)

if __name__ == "__main__":
    url = sys.argv[1]
    output_filename = sys.argv[2]

    get_dynamic_html(url, output_filename)
