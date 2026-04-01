import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_cities(state):
    driver_options=webdriver.ChromeOptions()
    driver_options.add_argument("--headless")

    driver=webdriver.Chrome(options=driver_options)
    driver.get(url="https://www.city-data.com/")

    state=driver.find_element(By.XPATH,f"//a[@title='{state.title()} cities']")
    state.click()
    cities_sel=driver.find_elements(By.CSS_SELECTOR,".rB td a")
    cities=[city.text for city in cities_sel]
    driver.quit()
    return cities


def setup_driver():

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")


    driver = webdriver.Chrome(options=options)
    return driver


def extract_email_from_page(url, use_selenium=False):

    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    if use_selenium:
        try:
            driver = setup_driver()
            driver.get(url)

            for _ in range(3):
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
                time.sleep(0.8)

            page_source = driver.page_source  # Get full loaded page HTML
            driver.quit()
        except Exception:
            return None
    else:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            page_source = response.text
        except requests.exceptions.RequestException:
            return None

    match = re.search(email_pattern, page_source)
    return match.group() if match else None


def find_contact_page(base_url):

    try:
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for a in soup.find_all("a", href=True):
            link = a["href"].lower()
            if "contact" in link or "about" in link or "contact-us" in link or "contact us" in link:
                return urljoin(base_url, a["href"])
        return None
    except requests.exceptions.RequestException:
        return None


def get_email(url):

    if url=="Couldn't find website":
        return "Couldn't find an email"

    email = extract_email_from_page(url, use_selenium=True)
    if email:
        return email

    contact_url = find_contact_page(url)
    if contact_url:
        email = extract_email_from_page(contact_url, use_selenium=True)
        if email:
            return email

    return "Couldn't find an email"

