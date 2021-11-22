from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import requests
import re
import sys


def setupDriver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True) # So window doesn't close
    driver = webdriver.Chrome("/Users/nadavskloot/Documents/GitHub/comp446/better_job_finder/chromedriver", chrome_options=chrome_options) # add your path to chromedriver, mine is "/Users/nadavskloot/Documents/GitHub/comp446/better_job_finder/chromedriver"
    driver.get("https://www.linkedin.com/jobs")
    #cookie for username: rroczbikpplzvhotou@mrvpt.com, pass: hebedebe
    # cookie = {'name': "li_at",'value':"AQEDATiE-woDvY3iAAABfRYyfewAAAF9Oj8B7E4AySbBRJeEri4Uig-2B1hlS4dhO7btpUwcnJljINARdtGB6IUdmWiWhDxpSWc0P9rhH5wlCx_2ugoDz0lvQumpl-gOuHVp-7uBGeYDhEkwXVi9ETBn"}
    # driver.add_cookie(cookie)
    return driver

def search(driver, kewWord, location):
    jobInput = driver.find_elements(By.NAME, "keywords")[0]
    jobLocation = driver.find_elements(By.NAME, "location")[0]
    # str(jobInput.is_displayed())
    jobInput.clear()
    jobInput.send_keys(kewWord)
    jobLocation.clear()
    jobLocation.send_keys(location)
    jobInput.send_keys(Keys.RETURN) # search

    return driver.page_source

def scrape(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')

    jobTitles = soup.find_all("h3", attrs={'class': re.compile("base-search-card__title")})
    jobEmployers = soup.find_all("h4", attrs={'class': re.compile("base-search-card__subtitle")})
    jobLocations = soup.find_all("span", attrs={'class': re.compile("job-search-card__location")})
    

    jobs = {}
    for i in range(len(jobTitles)):
        job = jobEmployers[i].text.strip() + " - " + jobTitles[i].text.strip()
        jobs[job] = {
            "title": jobTitles[i].text.strip(),
            "employer": jobEmployers[i].text.strip(),
            'location': jobLocations[i].text.strip()
        }
    print()
    print(jobs)


if __name__ == "__main__":
    keyWord = sys.argv[1]
    location = sys.argv[2]
    driver = setupDriver()
    page_source = search(driver, keyWord, location)
    scrape(page_source)
