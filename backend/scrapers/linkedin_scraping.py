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
    return driver

def search(driver, kewWord, location):
    jobInput = driver.find_elements(By.NAME, "keywords")[0]
    jobLocation = driver.find_elements(By.NAME, "location")[0]
    jobInput.clear()
    jobInput.send_keys(kewWord)
    jobLocation.clear()
    jobLocation.send_keys(location)
    base = driver.find_element(By.TAG_NAME, "html")
    jobInput.send_keys(Keys.RETURN) # search
    waitForRefresh(driver, base)
    return driver

def scrape(driver, userSearch):
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    jobsUl = soup.find("ul", attrs={"class": re.compile("jobs-search__results-list")})
    jobLinks = jobsUl.find_all("a", href=True, attrs={"class": re.compile("base-card__full-link")})
    print(len(jobLinks))
    

    jobResults = []
    for job in jobLinks:
        print(job['href'])

        sleepTime = random.randint(4,10)
        time.sleep(sleepTime)

        base_url = job['href']
        r = requests.get(base_url)
        soup = BeautifulSoup(r.content, 'html.parser')

        jobHeader = soup.find("section", attrs={"class": re.compile("top-card-layout")})
        jobTitle = jobHeader.find("h1", attrs={"class": re.compile("topcard__title")})
        jobEmployer = jobHeader.find("a", attrs={"class": re.compile("topcard__org-name-link")})
        jobLocation = jobHeader.find("span", attrs={"class": "topcard__flavor"}).findNextSibling()

        jobDict = {
            "title": jobTitle.string.strip(),
            "employer": jobEmployer.text.strip(),
            "location": jobLocation.text.strip(),
            'income': None,
            'key_words': None, 
            'required_skills': None, 
            'experience': None, 
            'education': None, 
            'job_type': None,
            'score': 0
        }

        jobInfoUl = soup.find("ul", attrs={"class": re.compile("description__job-criteria-list")})
        if jobInfoUl:
            jobType = jobInfoUl.find("h3", text=re.compile("Employment type")).findNextSibling()
            print(jobType.text.strip())
            jobDict["job_type"] = jobType.text.strip()

        
        jobDescriptionDiv = soup.find("div", attrs={"class": re.compile("show-more-less-htm")})
        
        
        print(jobTitle.string)
        print(jobEmployer.text.strip())
        print(jobLocation.text.strip())
        
        search_description(jobDescriptionDiv, jobDict) # educationLevel and years exeriance
        requiredSkills = userSearch["required_skills"].strip()
        search_skills(jobDescriptionDiv, jobDict, requiredSkills)

        pp = pprint.PrettyPrinter()
        pp.pprint(jobDict)
        print()


def search_description(jobDescriptionDiv, jobDict):
            
    yearsExperienceSentence = jobDescriptionDiv.find(text=re.compile("year(.)*experience"))
    if yearsExperienceSentence:
        yearsExperience = [int(s) for s in re.findall(r'\b\d+\b', str(yearsExperienceSentence))]
        if len(yearsExperience) > 0:
            jobDict["experience"] = yearsExperience[0]
            print(yearsExperience)
        print(yearsExperienceSentence)
    educationLevelSentence = jobDescriptionDiv.find(text=[re.compile("Bachelor"), re.compile("Master"), re.compile("BS "), re.compile(" MS ")])
    jobDict["education"] = str(educationLevelSentence).strip()
    print(educationLevelSentence)

    blob = TextBlob(jobDescriptionDiv.text)
    for sentence in blob.sentences:
        if re.match("Bachelor", str(sentence)) or re.match("BS ", str(sentence)):
            print(sentence)

def search_skills(jobDescriptionDiv, jobDict, requiredSkills):
    blob = TextBlob(jobDescriptionDiv.text)
    for sentence in blob.sentences:
        if requiredSkills in sentence.words:
            print(sentence)
    if requiredSkills in blob.words:
        jobDict["required_skills"] = True

def waitForRefresh(driver, base):
    try:
        element = WebDriverWait(driver, 20).until(
        EC.staleness_of(base)
    )
        return
    except TimeoutException:
        print("baddd")
        raise TimeoutError

def main(userSearch):
    keyWord = userSearch["job_title"]
    location = userSearch["location"]
    driver = setupDriver()
    driver = search(driver, keyWord, location)
    jobResults = scrape(driver, userSearch)
    driver.quit()

if __name__ == "__main__":
    keyWord = sys.argv[1]
    location = sys.argv[2]
    driver = setupDriver()
    driver = search(driver, keyWord, location)
    scrape(driver, {'job_title': '', 'location': '', 'income': '', 'key_words': '', 'required_skills': 'python', 'experience': '', 'education': '', 'job_type': ''})
    driver.quit()
