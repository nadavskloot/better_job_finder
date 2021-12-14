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
import re
import sys
import requests
import pprint
from textblob import TextBlob
from word2number import w2n


def setupDriver():
    chrome_options = Options()
    chrome_options.add_experimental_option(
        "detach", True)  # So window doesn't close
    chrome_options.add_argument("--disable-single-click-autofill")
    chrome_options.add_argument("--ignore-autocomplete-on-autofill")
    driverPath = downloadDriver()
    s = Service(driverPath)
    # add your path to chromedriver, mine is "/Users/nadavskloot/Documents/GitHub/comp446/better_job_finder/chromedriver"
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.get("https://www.indeed.com")
    return driver


def search(driver, kewWord, location):
    jobInput = driver.find_elements(By.ID, "text-input-what")[0]
    jobLocation = driver.find_elements(By.ID, "text-input-where")[0]
    jobInput.clear()
    jobInput.send_keys(kewWord)
    jobLocation.send_keys(Keys.TAB)
    while (jobLocation.get_attribute('value') != ""):
        jobLocation.send_keys(Keys.BACK_SPACE)
    jobLocation.send_keys(location)
    base = driver.find_element(By.TAG_NAME, "html")
    jobInput.send_keys(Keys.RETURN)  # search

    waitForRefresh(driver, base)
    return driver


def scrape(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    jobsDiv = soup.find_all("div", id=re.compile(
        "mosaic-provider-jobcards"))[0]
    jobLinks = jobsDiv.find_all("a", href=True, recursive=False)
    print(len(jobLinks))

    indeedJobs = []
    for job in jobLinks:
        base_url = "https://www.indeed.com" + job['href']
        base = driver.find_element(By.TAG_NAME, "html")
        driver.get(base_url)

        waitForRefresh(driver, base)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        jobTitle = soup.find(
            "h1", attrs={'class': re.compile("jobsearch-JobInfoHeader-title")})
        jobEmployerDiv = soup.find(
            "div", attrs={'class': re.compile("jobsearch-InlineCompanyRating")})
        jobEmployer = jobEmployerDiv.find(["a", "div"])
        jobLocation = jobEmployerDiv.next_sibling
        jobDescriptionDiv = soup.find(
            "div", attrs={"class": re.compile("jobsearch-JobComponent-description")})

        detailsSection = soup.find("div", id="jobDetailsSection")
        if detailsSection:
            salary = detailsSection.find("span", string=re.compile("$"))
            jobType = detailsSection.find(
                "div", string="Job Type").next_sibling
        qualificationsSection = soup.find("div", id="qualificationsSection")

        descriptionSection = soup.find("div", id="jobDescriptionText")

        jobDict = {
            "title": jobTitle.text.strip(),
            "employer": jobEmployer.text.strip(),
            "location": jobLocation.text.strip(),
            'income': None,
            'required_skills': None,
            'experience': None,
            'education': [],
            'job_type': None,
            'score': 0,
            "link": base_url
        }

        # print(jobTitle.string)
        # print(jobEmployer.string)
        # print(jobLocation.string)
        if detailsSection and salary:
            print(salary.string)
            jobDict["income"] = salary.string
        if jobType and detailsSection:
            print(jobType.string)
            jobDict["job_type"] = jobType.string
        # print(jobDescriptionDiv.text)
        # print(descriptionSection.text)
        if qualificationsSection:
            print(qualificationsSection.text)
        print()

        findEducation(jobDescriptionDiv, jobDict)

        pp = pprint.PrettyPrinter()
        pp.pprint(jobDict)
        print()
        indeedJobs.append(jobDict)

    return indeedJobs


def findEducation(jobDescriptionDiv, jobDict):
    blob = TextBlob(str(jobDescriptionDiv.text))
    # print(blob)
    educationRegex = {"BS": [r"[Bb]achelor", r"\bBS ", r"\bB.S. ", r"\bBA ", r"\bB.A. " r"College Diploma "],
                      "MS": [r"[Mm]aster", r"\bMS ", r"\bM.S. "],
                      "PhD": [r"PhD", r"\b[Dd]octorate "]}
    for sentence in blob.sentences:
        for educationLevel in educationRegex.keys():
            for regex in educationRegex[educationLevel]:
                match = re.search(regex, str(sentence))
                if match:
                    # print(str(sentence))
                    print(match.group())
                    print(educationLevel)
                    if educationLevel not in jobDict["education"]:
                        jobDict["education"].append(educationLevel)


def score(jobsDict, searchDict):
    return


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
    jobDict = scrape(driver)
    searchDict = {}
    driver.quit()
    # score(jobsDict, searchDict)
