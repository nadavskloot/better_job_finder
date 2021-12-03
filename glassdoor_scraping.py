from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service

from bs4 import BeautifulSoup
import time
import re
import sys
import pprint
import requests


def setupDriver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True) # So window doesn't close
    chrome_options.add_argument("--disable-single-click-autofill")
    s=Service('/Users/nadavskloot/Documents/GitHub/comp446/better_job_finder/chromedriver')
    driver = webdriver.Chrome(service=s, options=chrome_options) # add your path to chromedriver, mine is "/Users/nadavskloot/Documents/GitHub/comp446/better_job_finder/chromedriver"
    driver.get("https://www.glassdoor.com/Search/")
    return driver

def search(driver, kewWord, location):
    jobInput = driver.find_elements(By.ID, "sc.keyword")[0]
    jobLocation = driver.find_elements(By.ID, "sc.location")[0]
    # str(jobInput.is_displayed())
    jobInput.clear()
    jobInput.send_keys(kewWord + " Jobs")
    jobLocation.clear()
    jobLocation.send_keys(location)
    base = driver.find_element(By.TAG_NAME, "html")
    jobInput.send_keys(Keys.RETURN) # search

    # time.sleep(10)
    

    try:
        element = WebDriverWait(driver, 20).until(
        EC.staleness_of(base)
    )
    except TimeoutException:
        print("baddd")
        raise TimeoutError
    
    base = driver.find_element(By.TAG_NAME, "html")
    seeMoreButton = driver.find_element(By.CSS_SELECTOR, "a[data-test='jobs-location-see-all-link']")
    seeMoreButton.click()

    try:
        element = WebDriverWait(driver, 20).until(
        EC.staleness_of(base)
    )
        return driver
    except TimeoutException:
        print("baddd")
        raise TimeoutError

def scrape(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # jobPosts = soup.find_all("a", attrs={'class': re.compile("job-tile")})
    jobTitles = soup.find_all("p", attrs={'class': re.compile("css-forujw")})
    jobEmployers = soup.find_all("p", attrs={'class': re.compile("css-1xznj1f")})
    jobLocations = soup.find_all("p", attrs={'class': re.compile("css-56kyx5 small")})
    
    
    jobsUl = soup.find("ul", attrs={'class': re.compile("job-search-key")})
    # print(jobsUl)
    # print()
    jobLinks = jobsUl.find_all("a", href=True, limit=5)
    # print(jobLinks)
    # print()
    for job in jobLinks:
        base_url = "https://www.glassdoor.com" + job['href']
        r = requests.get(base_url)
        soup = BeautifulSoup(r.content, 'html.parser')

        jobTitle = soup.find("div", attrs={'class': re.compile("css-16nw49e")})
        jobDescriptionDiv = soup.find("div", attrs={"id": re.compile("JobDesc")})
        # jobStuff = jobDescriptionDiv.find_all("b")
        print(soup)
        print(jobTitle)
        # print(jobStuff)
        print()

    # print(jobPosts)
    # print(jobTitles)
    # print(jobEmployers)
    # print(jobLocations)

    # jobs = {}
    # for i in range(len(jobTitles)):
    #     job = jobEmployers[i].text.strip() + " - " + jobTitles[i].text.strip()
    #     jobs[job] = {
    #         "title": jobTitles[i].text.strip(),
    #         "employer": jobEmployers[i].text.strip(),
    #         'location': jobLocations[i].text.strip()
    #     }
        
    # print()
    # pp = pprint.PrettyPrinter()
    # pp.pprint(jobs)


    


if __name__ == "__main__":
    keyWord = sys.argv[1]
    location = sys.argv[2]
    driver = setupDriver()
    driver = search(driver, keyWord, location)
    scrape(driver)
    # driver.quit()