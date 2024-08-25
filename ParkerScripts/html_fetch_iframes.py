import json
import random
from datetime import datetime
import zipfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import sys
import time
import uuid
import threading

import os
from dotenv import load_dotenv
load_dotenv()

def load_proxy_config(proxy_country):
    with open(os.getenv("PROXIES_CONFIG_PATH"), 'r') as file:
        proxies = json.load(file)
    country_proxies = proxies.get(proxy_country, [])
    if country_proxies:
        return random.choice(country_proxies)
    return None

def create_proxy_extension(proxy_config, profile_folder_path):
    PROXY_HOST = proxy_config.get("proxy")
    PROXY_PORT = proxy_config.get("port")
    PROXY_USER = proxy_config.get("username")
    PROXY_PASS = proxy_config.get("password")

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = f"""
    var config = {{
            mode: "fixed_servers",
            rules: {{
            singleProxy: {{
                scheme: "http",
                host: "{PROXY_HOST}",
                port: parseInt("{PROXY_PORT}")
            }},
            bypassList: ["localhost"]
            }}
        }};

    chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

    function callbackFn(details) {{
        return {{
            authCredentials: {{
                username: "{PROXY_USER}",
                password: "{PROXY_PASS}"
            }}
        }};
    }}

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {{urls: ["<all_urls>"]}},
                ['blocking']
    );
    """

    pluginfile = profile_folder_path+'\\proxy_auth_plugin.zip'
    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    print(f"Proxy extension created at {pluginfile}")
    return pluginfile

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


def get_dynamic_html(url, output_file, scrolls=10, proxy_country=None):
    options = Options()
    profile_folder_path = os.getenv("CHROME_PROFILE_PATH") + "\\" + str(threading.get_ident())
    os.makedirs(profile_folder_path, exist_ok=True)

    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument(f"user-data-dir={profile_folder_path}")
    options.add_argument('--remote-allow-origins="*"')


    service = Service(executable_path=r""+os.getenv("CHROME_DRIVER_PATH")+"")

    if proxy_country:
        proxy_config = load_proxy_config(proxy_country)
        if proxy_config:
            pluginfile = create_proxy_extension(proxy_config, profile_folder_path)
            options.add_extension(pluginfile)
        else:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
    else:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

    browser = webdriver.Chrome(service=service, options=options)

    js_pagination = False

    try:
        browser.get(url)
        time.sleep(5)  # Wait for the initial page to load
        page_index = 1
        current_date = datetime.now().strftime("%d-%m-%y")

        while True:
            for i in range(scrolls):
                previous_height = browser.execute_script("return document.body.scrollHeight")
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # Wait 2 seconds between scrolls
                new_height = browser.execute_script("return document.body.scrollHeight")
                if new_height == previous_height:
                    break  # Break the loop if there is nowhere else to scroll


            if not js_pagination:
                browser.refresh()
                time.sleep(5)  # Wait for the page to load after refresh
                for i in range(scrolls):
                    previous_height = browser.execute_script("return document.body.scrollHeight")
                    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)  # Wait 2 seconds between scrolls
                    new_height = browser.execute_script("return document.body.scrollHeight")
                    if new_height == previous_height:
                        break  # Break the loop if there is nowhere else to scroll

            html_content = browser.page_source
            soup = BeautifulSoup(html_content, 'html.parser')

            iframe_elements = browser.find_elements(By.TAG_NAME, "iframe")
            for iframe in iframe_elements:
                if isinstance(iframe, webdriver.remote.webelement.WebElement):
                    unique_id = str(uuid.uuid4())
                    src = iframe.get_attribute('src') if iframe.get_attribute('src') else 'no-src'
                    js_script = f"""
                    var iframe = document.querySelector('iframe[src="{src}"]');
                    if (!iframe) {{
                        iframe = document.querySelector('iframe:not([src])');
                    }}
                    if (iframe) {{
                        iframe.setAttribute('data-unique-id', '{unique_id}');
                    }} else {{
                        console.log('Iframe not found for src: {src}');
                    }}
                    """
                    browser.execute_script(js_script)
                else:
                    print(f"Unexpected element in iframe_elements: {iframe}")

            main_page_content = browser.page_source
            soup = BeautifulSoup(main_page_content, 'html.parser')

            tags_to_remove = ['script', 'meta', 'style']
            for tag in tags_to_remove:
                for element in soup.find_all(tag):
                    element.decompose()

            for iframe in soup.find_all('iframe', attrs={"data-unique-id": True}):
                unique_id = iframe['data-unique-id']
                src = iframe['src'] if iframe.has_attr('src') else None
                if src:
                    try:
                        browser.switch_to.frame(browser.find_element(By.XPATH, f"//iframe[@data-unique-id='{unique_id}']"))
                        iframe_content = browser.page_source
                        iframe_soup = BeautifulSoup(iframe_content, 'html.parser')
                        new_div = soup.new_tag("div", **{"class": "replaced-iframe"})

                        iframe_body = iframe_soup.find('body')
                        if iframe_body:
                            html_content = ''.join(str(content) for content in iframe_body.contents)
                            new_div.append(BeautifulSoup(html_content, 'html.parser'))
                        iframe.replace_with(new_div)

                        browser.switch_to.default_content()

                    except Exception as e:
                        print(f"Error processing iframe {unique_id}: {e}")

            # Extract directory and filename from output_file
            output_dir = os.path.dirname(output_file)
            output_filename = os.path.basename(output_file)

            # Create a new folder named with the current date in the same directory as output_file

            new_folder_path = os.path.join(output_dir, current_date)
            os.makedirs(new_folder_path, exist_ok=True)

            # Save the first page to output_file
            if page_index == 1:
                with open(output_file, 'w', encoding='utf-8') as file:
                    file.write(str(soup))
                    remove_script_tags(output_file)

            # Save all pages, including the first one, into the newly created folder
            output_file_with_index = os.path.join(new_folder_path, output_filename.replace('.html', f'_page{page_index}.html'))
            with open(output_file_with_index, 'w', encoding='utf-8') as file:
                file.write(str(soup))

            remove_script_tags(output_file_with_index)

            pagination_element = f"//a[text()='{page_index + 1}']"
            next_page_link = browser.find_elements(By.XPATH, pagination_element)
            if not next_page_link:
                pagination_element = f"//button[text()='{page_index + 1}']"
                next_page_link = browser.find_elements(By.XPATH, pagination_element)
                if next_page_link:
                    browser.execute_script("arguments[0].setAttribute('href', '#');", next_page_link[0])
            if next_page_link:
                href = next_page_link[0].get_attribute('href')
                original_href = next_page_link[0].get_dom_attribute('href')  # Get the original attribute value
                if original_href == '#':
                    js_pagination = True

                    browser.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", next_page_link[0])
                    time.sleep(1)

                    # Wait until the element is clickable
                    wait = WebDriverWait(browser, 2)
                    wait.until(EC.element_to_be_clickable((By.XPATH, pagination_element)))

                    # Attempt to click the element
                    try:
                        next_page_link[0].click()
                    except Exception as e:
                        print(f"Error clicking the element: {e}")
                else:
                    js_pagination = False
                    browser.get(href)
                time.sleep(4)  # Wait for the page to load after refresh
                page_index += 1
            else:
                break
    finally:
        browser.quit()

if __name__ == "__main__":
    url = sys.argv[1]
    output_filename = sys.argv[2]
    proxy_country = sys.argv[3] if len(sys.argv) > 3 else None
    get_dynamic_html(url, output_filename, proxy_country=proxy_country)
