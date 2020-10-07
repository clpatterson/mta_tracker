from lxml import html

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_mta_page():
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
    tree = html.fromstring(page_data)
    delays = tree.xpath(
    "//div[@class='by-status']/h5[text()='Delays']/following-sibling::ul/li/a/span/text()")
    
    lines = []
    
    for line in delays:
        lines.append(line)

    return lines

def main():
    lines = get_delayed_lines(get_mta_page())
    with open("/mta_tracker/logs/test_log.txt", mode="w+") as f:
        f.write(str(lines))
    return lines

if __name__ == '__main__':
    print(main())