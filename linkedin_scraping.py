from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service

from bs4 import BeautifulSoup
import requests
import re
import sys
import random
import pprint
import time
from textblob import TextBlob

def setupDriver():
    chrome_options = Options()
    # chrome_options.add_experimental_option("detach", True) # So window doesn't close
    s=Service('/Users/nadavskloot/Documents/GitHub/comp446/better_job_finder/chromedriver')
    driver = webdriver.Chrome(service=s, options=chrome_options) # add your path to chromedriver, mine is "/Users/nadavskloot/Documents/GitHub/comp446/better_job_finder/chromedriver"
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
    base = driver.find_element(By.TAG_NAME, "html")
    jobInput.send_keys(Keys.RETURN) # search
    waitForRefresh(driver, base)
    return driver

def scrape(driver, userInput):
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    jobsUl = soup.find("ul", attrs={"class": re.compile("jobs-search__results-list")})
    jobLinks = jobsUl.find_all("a", href=True, attrs={"class": re.compile("base-card__full-link")})
    print(len(jobLinks))
    
    for job in jobLinks:
        print(job['href'])
        # base_url = job['href']
        # base = driver.find_element(By.TAG_NAME, "html")
        # driver.get(base_url)
        
        # waitForRefresh(driver, base)
        
        # soup = BeautifulSoup(driver.page_source, "html.parser")
        sleepTime = random.randint(4,10)
        time.sleep(sleepTime)
        base_url = job['href']
        r = requests.get(base_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        # print(soup)
        jobHeader = soup.find("section", attrs={"class": re.compile("top-card-layout")})
        jobTitle = jobHeader.find("h1", attrs={"class": re.compile("topcard__title")})
        jobEmployer = jobHeader.find("a", attrs={"class": re.compile("topcard__org-name-link")})
        # jobLocation = jobHeader.find("a", attrs={"class": re.compile("topcard__org-name-link")})
        jobLocation = jobHeader.find("span", attrs={"class": "topcard__flavor"}).findNextSibling()

        jobDict = {
            "title": jobTitle.string.strip(),
            "employer": jobEmployer.text.strip(),
            "location": jobLocation.text.strip(),
        }

        jobInfoUl = soup.find("ul", attrs={"class": re.compile("description__job-criteria-list")})
        if jobInfoUl:
            jobType = jobInfoUl.find("h3", text=re.compile("Employment type")).findNextSibling()
            print(jobType.text.strip())
            jobDict["job_type"] = jobType.text.strip()

        
        jobDescriptionDiv = soup.find("div", attrs={"class": re.compile("show-more-less-htm")})
        
        search_description(jobDescriptionDiv.text)
        yearsExperienceSentence = jobDescriptionDiv.find(text=re.compile("year(.)*experience"))
        educationLevelSentence = jobDescriptionDiv.find(text=[re.compile("Bachelor"), re.compile("Master"), re.compile("BS"), re.compile("MS")])
        if yearsExperienceSentence:
            yearsExperience = [int(s) for s in re.findall(r'\b\d+\b', str(yearsExperienceSentence))]
            print(yearsExperience)

        # print(jobHeader)
        print(jobTitle.string)
        print(jobEmployer.text.strip())
        print(jobLocation.text.strip())
        print(yearsExperienceSentence)
        print(educationLevelSentence)
        # print(jobInfo)
        # print(jobDescriptionDiv.text)
        print()


def search_description(text):
    blob = TextBlob(text)
    for sentence in blob.sentences:
        if sentence == re.compile("year"):
            print(sentence)

def waitForRefresh(driver, base):
    try:
        element = WebDriverWait(driver, 20).until(
        EC.staleness_of(base)
    )
        return
    except TimeoutException:
        print("baddd")
        raise TimeoutError

def main(keyWord, location,):
    print("hello")
    driver = setupDriver()
    driver = search(driver, keyWord, location)
    scrape(driver)
    driver.quit()

if __name__ == "__main__":
    keyWord = sys.argv[1]
    location = sys.argv[2]
    driver = setupDriver()
    driver = search(driver, keyWord, location)
    userInput = {}
    scrape(driver)
    driver.quit()
