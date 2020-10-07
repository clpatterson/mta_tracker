from datetime import datetime
import logging

from lxml import html
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from mta_tracker.tasks.celery import app
from mta_tracker.app import create_app
from mta_tracker.extensions import db
from mta_tracker.models import Lines, Delays

# Create app context for db
flask_app = create_app()
db.app = flask_app

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
    "//div[@class='by-status']/h5[text()='Delays']/following-sibling::ul/li/a/span/text()")
    
    lines = []
    
    for line in delays:
        lines.append(line)

    return lines

@app.task(name="mta_tracker.scrape-mta")
def scrape_mta_status():
    """Scrape and store subway line delay updates from mta info page."""
    # Get new delayed statuses
    updated_delayed_lines = get_delayed_lines(get_mta_page())
    
    # Get old delayed statuses
    delayed_lines = Lines.query.filter_by(current_status="Delayed").all()
    delayed_lines = [line.line for line in delayed_lines]

    # Store new delayed statuses in db
    if len(updated_delayed_lines) == 0:
        delay = Delays(time=datetime.now(),delayed_lines='')
    else:
        lines = ",".join(updated_delayed_lines)
        delay = Delays(time=datetime.now(),delayed_lines=lines)
    delay.add_delay()

    if len(updated_delayed_lines) == 0 and len(delayed_lines) == 0:
        return None
    
    # Compare old and new statuses
    delayed_lines = set(delayed_lines)
    updated_delayed_lines = set(updated_delayed_lines)

    still_delayed = delayed_lines.intersection(updated_delayed_lines)
    newly_delayed = updated_delayed_lines.difference(delayed_lines)
    newly_renewed = delayed_lines.difference(updated_delayed_lines)

    # Take action on comparison results
    if still_delayed:
        for line in still_delayed:
            line = Lines.query.filter_by(line=line).first()
            line.total_min_delayed += 1
            line.last_updated = datetime.now()
            db.session.commit()

    if newly_delayed:
        for line in newly_delayed:
            logger.info(f"Line {line} is experiencing delays.")
            line = Lines.query.filter_by(line=line).first()
            line.current_status = 'Delayed'
            line.last_updated = datetime.now()
            db.session.commit()
    
    if newly_renewed:
        for line in newly_renewed:
            logger.info(f"Line {line} is now recovered.")
            line = Lines.query.filter_by(line=line).first()
            line.total_min_delayed += 1
            line.current_status = 'On-time'
            line.last_updated = datetime.now()
            db.session.commit()
    
    return None