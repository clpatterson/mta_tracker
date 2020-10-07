import logging

from lxml import html
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from mta_tracker.tasks.celery import app

# Create custom logger
logger = logging.getLogger(__name__)
f_handler = logging.FileHandler("/mta_tracker/logs/line_status.log")
f_handler.setLevel(logging.INFO)
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)

def get_mta_page():
    """Get page data from dynamic mta info page."""
    driver = webdriver.Remote("http://chrome:4444/wd/hub", 
    DesiredCapabilities.CHROME)
    
    url = 'https://new.mta.info/'
    driver.get(url)

    # Wait for page to load, then check for status-block element
    wait = WebDriverWait(driver, 5)
    wait.until(EC.visibility_of_element_located((By.XPATH,
     "//div[@class='status-block']")))

    data = driver.page_source
    driver.close()

    return data

def get_delayed_lines(page_data):
    """Parse mta info page and return delayed lines."""
    tree = html.fromstring(page_data)
    delays = tree.xpath(
    "//div[@class='by-status']/h5[text()='Planned Work']/following-sibling::ul/li/a/span/text()")
    
    lines = []
    
    for line in delays:
        lines.append(line)

    return lines

@app.task(name="mta_tracker.scrape-mta")
def scrape_mta_status():
    """Scrape and store line delay updates from mta info page."""
    updated_delayed_lines = set(get_delayed_lines(get_mta_page()))
    for line in updated_delayed_lines:
        logger.info(f"Line {line} is experiencing delays.")
        logger.info(f"Line {line} is now recovered.")
    
    return None