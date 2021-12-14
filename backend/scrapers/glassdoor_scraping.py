from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from .setupChromeDriver import downloadDriver

from bs4 import BeautifulSoup
import time
import re
import sys
import pprint
import requests


def setupDriver():
    chrome_options = Options()
    chrome_options.add_experimental_option(
        "detach", True)  # So window doesn't close
    chrome_options.add_argument("--disable-single-click-autofill")
    driverPath = downloadDriver()
    s = Service(driverPath)
    # add your path to chromedriver, mine is "/Users/nadavskloot/Documents/GitHub/comp446/better_job_finder/chromedriver"
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.get("https://www.glassdoor.com/Search/")
    return driver


def search(driver, kewWord, location):
    jobInput = driver.find_elements(By.ID, "sc.keyword")[0]
    jobLocation = driver.find_elements(By.ID, "sc.location")[0]
    jobInput.clear()
    jobInput.send_keys(kewWord + " Jobs")
    jobLocation.clear()
    jobLocation.send_keys(location)
    base = driver.find_element(By.TAG_NAME, "html")
    jobInput.send_keys(Keys.RETURN)  # search

    waitForRefresh(driver, base)

    base = driver.find_element(By.TAG_NAME, "html")
    seeMoreButton = driver.find_element(
        By.CSS_SELECTOR, "a[data-test='jobs-location-see-all-link']")
    seeMoreButton.click()

    waitForRefresh(driver, base)
    return driver


def scrape(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    jobsUl = soup.find("ul", attrs={'class': re.compile("job-search-key")})
    # there is a better way to do this
    jobLinks = jobsUl.find_all("a", href=True, limit=20)
    jobLinks = jobLinks[::4]

    for job in jobLinks:
        base_url = "https://www.glassdoor.com" + job['href']
        base = driver.find_element(By.TAG_NAME, "html")
        driver.get(base_url)

        waitForRefresh(driver, base)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        jobTitle = soup.find("div", attrs={'class': re.compile("css-17x2pwl")})
        jobEmployer = soup.find(
            "div", attrs={'class': re.compile("css-16nw49e")})
        if jobEmployer.span:
            jobEmployer.span.extract()
        jobLocation = soup.find(
            "div", attrs={'class': re.compile("css-1v5elnn")})
        jobDescriptionDiv = soup.find(
            "div", attrs={"id": re.compile("JobDesc")})

        # print(base_url)
        print(jobTitle.string)
        print(jobEmployer.string)
        print(jobLocation.string)

        try:
            element = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[data-tab-type='salary']"))
            )
            salaryButton = driver.find_element(
                By.CSS_SELECTOR, "div[data-tab-type='salary']")
            base = driver.find_element(By.TAG_NAME, "html")
            salaryButton.click()

            soup = BeautifulSoup(driver.page_source, "html.parser")
            salary = soup.find(
                "div", attrs={'class': re.compile("css-1bluz6i")})
            if salary.span:
                salary.span.extract()
            print(salary.string)
        except TimeoutException:
            print("no salary")

        # print(jobDescriptionDiv)
        print(jobDescriptionDiv.text)
        print()


def waitForRefresh(driver, base):
    try:
        element = WebDriverWait(driver, 20).until(
            EC.staleness_of(base)
        )
        return
    except TimeoutException:
        print("baddd")
        raise TimeoutError


if __name__ == "__main__":
    keyWord = sys.argv[1]
    location = sys.argv[2]
    driver = setupDriver()
    driver = search(driver, keyWord, location)
    scrape(driver)
    # driver.quit()
