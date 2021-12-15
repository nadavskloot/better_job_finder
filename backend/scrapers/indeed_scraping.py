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
    # driverPath = '/Users/nadavskloot/Documents/GitHub/comp446/better_job_finder/backend/scrapers/chromedrivers/chromedriver'
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


def scrape(driver, userSearch):
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
        jobType = None
        if detailsSection:
            salary = detailsSection.find("span", string=re.compile("$"))
            jobTypeSection = detailsSection.find(
                "div", string="Job Type")
            if jobTypeSection:
                jobType=jobTypeSection.next_sibling
        qualificationsSection = soup.find("div", id="qualificationsSection")

        descriptionSection = soup.find("div", id="jobDescriptionText")

        jobDict = {
            "job_title": jobTitle.text.strip(),
            "employer": jobEmployer.text.strip(),
            "location": jobLocation.text.strip(),
            'salary': None,
            'required_skills': [],
            'years_experience': None,
            'education_level': [],
            'employment_type': None,
            'score': 0,
            "job_post_link": base_url
        }

        # print(jobTitle.string)
        # print(jobEmployer.string)
        # print(jobLocation.string)
        if detailsSection and salary:
            print(salary.string)
            # jobDict["salary"] = salary.string
            sentenceToSalary(salary.string, jobDict)
        if jobType and detailsSection:
            print(jobType.string)
            jobDict["employment_type"] = jobType.string
        # print(jobDescriptionDiv.text)
        # print(descriptionSection.text)
        if qualificationsSection:
            print(qualificationsSection.text)
        print()

        findEducation(jobDescriptionDiv, jobDict)
        findExperience(jobDescriptionDiv, jobDict)
        if userSearch["required_skills"].strip() != "":
            search_skills(jobDescriptionDiv, jobDict, userSearch)

        score(jobDict, userSearch)

        pp = pprint.PrettyPrinter()
        pp.pprint(jobDict)
        print()
        indeedJobs.append(jobDict)

    return indeedJobs


def findEducation(jobDescriptionDiv, jobDict): 
    """"Finds the level of education from the job description"""
    blob = TextBlob(str(jobDescriptionDiv.text))
    # print(blob)
    educationRegex = {"Bachelors": [r"[Bb]achelor", r"\bBS ", r"\bB.S. ", r"\bBA ", r"\bB.A. " r"College Diploma "],
                      "Masters": [r"\b[Mm]aster", r"\bMS ", r"\bM.S. "],
                      "P.H.D": [r"PhD", r"P.H.D.", r"\b[Dd]octorate "]}
    for sentence in blob.sentences:
        for educationLevel in educationRegex.keys():
            for regex in educationRegex[educationLevel]:
                match = re.search(regex, str(sentence))
                if match:
                    # print(str(sentence))
                    # print(match.group())
                    # print(educationLevel)
                    if educationLevel not in jobDict["education_level"]:
                        jobDict["education_level"].append(educationLevel)


def findExperience(jobDescriptionDiv, jobDict):
    """"Finds the level of experience from the job description"""
    # yearsExperienceTag = jobDescriptionDiv.find(
    #     text=[re.compile(r"\b\d+\b(.)*((year)|(years))(.)*experience")])
    children = jobDescriptionDiv.findChildren()
    # for tag in jobDescriptionDiv:
    #     print(tag)
    #     print()
    experienceRegex = [r"\b\d+\b(.)*((year)|(years))(.)*experience",
                       r"(one |two |three |four |five |six |seven |eight |nine |ten |eleven |twelve |thirteen |fourteen |fifteen )(.)*[(year)|(years)](.)*experience"]
    for child in children:
        for child2 in child:
            # print(child2.text)
            blob = TextBlob(str(child2.text))
            for sentence in blob.sentences:
                for regex in experienceRegex:
                    match = re.search(regex, str(sentence))
                    if match:
                        # print(match)
                        sentenceToExperience(match.group(), jobDict)
                        # print()
                    # match2 = re.search(r"years", str(sentence))
                    # if match2:
                    #     print("match2: ", sentence)


def sentenceToExperience(sentence, jobDict):
    """Converts the sentence containing the level of experience to a singular number 
    that represents the minimum accepted years of experience"""
    matches = re.findall(
        "(one |two |three |four |five |six |seven |eight |nine |ten |eleven |twelve |thirteen |fourteen |fifteen )", sentence)
    if matches:
        for match in matches:
            num = w2n.word_to_num(match)

            sentence = sentence.replace(match, str(num))
    matches = re.findall(r"\d+", sentence)
    if matches:
        # print(matches)
        # print(int(min(matches)))
        if jobDict["years_experience"]:
            jobDict["years_experience"] = max(
                jobDict["years_experience"], int(min(matches)))
        else:
            jobDict["years_experience"] = int(min(matches))

def sentenceToSalary(sentence, jobDict):
    matches = re.findall(r"\d*,\d*", sentence)
    if matches:
        for i in range(len(matches)):
            matches[i] = matches[i].replace(",", "")
            print(matches[i])
            matches[i] = int(matches[i])
        print(matches)
        jobDict["salary"] = max(matches)

# required Skills need to be comma seperated!!
def search_skills(jobDescriptionDiv, jobDict, userSearch):
    """Searches through the job description for the user's skills"""
    skills = userSearch["required_skills"].split(",")
    print(skills)
    string = str(jobDescriptionDiv.text)
    for skill in skills:
        match = re.search(re.escape(skill.strip().lower()), string.lower())
        if match:
            print(match.group())
            jobDict["required_skills"].append(str(match.group()).strip())


def score(jobDict, userSearch):
    """Scores a job result based on how well it matches the user's specifications"""
    if userSearch["education"] in jobDict["education_level"]:
        jobDict["score"] += 1
        print("education!")
    if jobDict["employment_type"] == userSearch["job_type"]:
        jobDict["score"] += 1
        print("Job Type!")
    if userSearch["experience"] and jobDict["years_experience"]:
        if jobDict["years_experience"] <= int(userSearch["experience"]):
            jobDict["score"] += 1
            print("experience!")
    if len(jobDict["required_skills"]) > 0:
        jobDict["score"] += (len(jobDict["required_skills"]) /
                             len(userSearch["required_skills"].split(",")))
        print("skills!")
    if jobDict["salary"] and userSearch["income"]:
        if jobDict["salary"] >= int(userSearch["income"]):
            jobDict["score"] += 1
            print("salary!")



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
    indeedJobs = scrape(driver, userSearch)
    driver.quit()
    return indeedJobs

if __name__ == "__main__":
    keyWord = sys.argv[1]
    location = sys.argv[2]
    driver = setupDriver()
    driver = search(driver, keyWord, location)
    userSearch = {'job_title': '', 'location': '', 'income': '', 'key_words': '',
                    'required_skills': 'python', 'experience': '', 'education': '', 'job_type': ''}
    jobDict = scrape(driver, userSearch)
    searchDict = {}
    driver.quit()
    # score(jobsDict, searchDict)
