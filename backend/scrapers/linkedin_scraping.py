from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service

from bs4 import BeautifulSoup
import platform
import requests
import re
import sys
import random
import pprint
import time
import os
import zipfile
import xmltodict
from textblob import TextBlob
from word2number import w2n


def setupDriver():
    chrome_options = Options()
    chrome_options.add_experimental_option(
        "detach", True)  # So window doesn't close
    # chrome_options.add_argument("--headless") # So window never opens
    driverPath = downloadDriver()
    print('*************************** driverpath:', driverPath)
    s = Service(driverPath)
    # add your path to chromedriver, mine is "/Users/nadavskloot/Documents/GitHub/comp446/better_job_finder/chromedriver"
    driver = webdriver.Chrome(service=s, options=chrome_options)
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
    sleepTime = random.randint(4, 10)
    time.sleep(sleepTime)
    jobInput.send_keys(Keys.RETURN)  # search
    waitForRefresh(driver, base)
    return driver


def downloadDriver():
    dirname = os.path.dirname(__file__)
    driver_folder = os.path.join(dirname, 'chromedrivers')
    os.makedirs(driver_folder, exist_ok=True)

    osname = platform.system()
    if osname == 'Darwin':
        chromeVersion = os.popen(
            '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version').read().strip('Google Chrome ').strip()
    elif osname == 'Windows':
        chromeVersion = os.popen(
            'C:\Program Files\Google\Chrome\Application\chrome.exe --version').read().strip('Google Chrome ').strip()
    elif osname == 'Linux':
        chromeVersion = os.popen(
            '/usr/bin/google-chrome --version').read().strip('Google Chrome ').strip()

    if os.path.exists(driver_folder+'/chromedriver'):
        if os.popen(f'{driver_folder}/chromedriver -v').read().split(' ')[1].split('.')[0:2] == chromeVersion.split('.')[0:2]:
            print('*************************************', 'keeping driver')
            return driver_folder+'/chromedriver'
        else:
            print('*************************************', 'replacing driver')
            os.remove(driver_folder+'/chromedriver')
    else:
        print('*************************************', 'creating driver')

    r = requests.get(
        'https://chromedriver.storage.googleapis.com/?delimiter=/&prefix=')
    json = xmltodict.parse(r.content)
    downloadVersion = ''
    for i in json['ListBucketResult']['CommonPrefixes']:
        if i['Prefix'].split('.')[0:2] == chromeVersion.split('.')[0:2]:
            downloadVersion = i['Prefix'][:-1]
            break

    if osname == 'Darwin':
        if platform.processor() == 'arm' and int(chromeVersion.split('.')[0]) > 88:
            downloadLink = f'https://chromedriver.storage.googleapis.com/{downloadVersion}/chromedriver_mac64_m1.zip'
        else:
            downloadLink = f'https://chromedriver.storage.googleapis.com/{downloadVersion}/chromedriver_mac64.zip'
    elif osname == 'Windows':
        downloadLink = f'https://chromedriver.storage.googleapis.com/{downloadVersion}/chromedriver_win32.zip'
    elif osname == 'Linux':
        downloadLink = f'https://chromedriver.storage.googleapis.com/{downloadVersion}/chromedriver_linux64.zip'
    r_down = requests.get(downloadLink, allow_redirects=True)
    # https://stackoverflow.com/questions/49787327/selenium-on-mac-message-chromedriver-executable-may-have-wrong-permissions
    # https://stackoverflow.com/questions/36745577/how-do-you-create-in-python-a-file-with-permissions-other-users-can-write
    zip_location = f'{driver_folder}/{osname}-{downloadVersion}-driver.zip'
    open(os.open(zip_location,
                 os.O_CREAT | os.O_WRONLY, 0o755), 'wb').write(r_down.content)
    with zipfile.ZipFile(zip_location, 'r') as zip_ref:
        zip_ref.extractall(driver_folder)
    os.chmod(driver_folder+'/chromedriver', 0o755)
    os.remove(zip_location)
    return driver_folder+'/chromedriver'


def scrape(driver, userSearch):
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    jobsUl = soup.find(
        "ul", attrs={"class": re.compile("jobs-search__results-list")})
    if not jobsUl:
        print("NO UL")
        print(soup)
    jobLinks = jobsUl.find_all("a", href=True, attrs={
                               "class": re.compile("base-card__full-link")})
    print(len(jobLinks))

    linkedinJobs = []
    for job in jobLinks:
        print(job['href'])

        sleepTime = random.randint(4, 10)
        time.sleep(sleepTime)

        base_url = job['href']
        r = requests.get(base_url)
        soup = BeautifulSoup(r.content, 'html.parser')

        jobHeader = soup.find(
            "section", attrs={"class": re.compile("top-card-layout")})
        if not jobHeader:
            driver.get(base_url)
            print(soup)
        jobTitle = jobHeader.find(
            "h1", attrs={"class": re.compile("topcard__title")})
        jobEmployer = jobHeader.find(
            "a", attrs={"class": re.compile("topcard__org-name-link")})
        jobLocation = jobHeader.find(
            "span", attrs={"class": "topcard__flavor"}).findNextSibling()

        jobDict = {
            "title": jobTitle.string.strip(),
            "employer": jobEmployer.text.strip(),
            "location": jobLocation.text.strip(),
            'income': None,
            'required_skills': [],
            'experience': None,
            'education': [],
            'job_type': None,
            'score': 0,
            "link": base_url
        }

        jobInfoUl = soup.find(
            "ul", attrs={"class": re.compile("description__job-criteria-list")})
        if jobInfoUl:
            jobType = jobInfoUl.find("h3", text=re.compile(
                "Employment type")).findNextSibling()
            print(jobType.text.strip())
            jobDict["job_type"] = jobType.text.strip()

        jobDescriptionDiv = soup.find(
            "div", attrs={"class": re.compile("show-more-less-htm")})

        print(jobTitle.string)
        print(jobEmployer.text.strip())
        print(jobLocation.text.strip())

        # search_description(jobDescriptionDiv, jobDict) # educationLevel and years exeriance
        findEducation(jobDescriptionDiv, jobDict)
        findExperience(jobDescriptionDiv, jobDict)
        # requiredSkills = userSearch["required_skills"]
        search_skills(jobDescriptionDiv, jobDict, userSearch)

        score(jobDict, userSearch)

        pp = pprint.PrettyPrinter()
        pp.pprint(jobDict)
        print()
        linkedinJobs.append(jobDict)
        # print(str(jobDescriptionDiv.text))
    return linkedinJobs


def findEducation(jobDescriptionDiv, jobDict):
    blob = TextBlob(str(jobDescriptionDiv.text))
    # print(blob)
    educationRegex = {"BS": [r"[Bb]achelor", r"\bBS ", r"\bB.S. ", r"\bBA ", r"\bB.A. " r"College Diploma "],
                      "MS": [r"\b[Mm]aster", r"\bMS ", r"\bM.S. "],
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


def findExperience(jobDescriptionDiv, jobDict):
    yearsExperienceTag = jobDescriptionDiv.find(
        text=[re.compile(r"\b\d+\b(.)*((year)|(years))(.)*experience")])
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
                        print(match)
                        sentenceToExperience(match.group(), jobDict)
                        print()
                    match2 = re.search(r"years", str(sentence))
                    if match2:
                        print("match2: ", sentence)


def sentenceToExperience(sentence, jobDict):
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
        if jobDict["experience"]:
            jobDict["experience"] = max(
                jobDict["experience"], int(min(matches)))
        else:
            jobDict["experience"] = int(min(matches))


# def scoreEducation(jobDict, userSearch):
#     userEducation = userSearch["education"].strip()
#     if userEducation:
#         educationRegex = {"BS": [r"\b[Bb]achelor", r"\bBS", r"\bB.S.", r"\bCollege Diploma"],
#                        "MS": [r"\b[Mm]asters", r"\bMS", r"\bM.S."],
#                        "PhD": [ r"\bPhD", r"\b[Dd]octorate"]}
#         for educationLevel in educationRegex.keys():
#             for regex in educationRegex[educationLevel]:
#                 match = re.search(regex, userEducation)
#                 if match:


def search_description(jobDescriptionDiv, jobDict):

    yearsExperienceSentence = jobDescriptionDiv.find(
        text=re.compile("year(.)*experience"))
    if yearsExperienceSentence:
        yearsExperience = [int(s) for s in re.findall(
            r'\b\d+\b', str(yearsExperienceSentence))]
        if len(yearsExperience) > 0:
            jobDict["experience"] = yearsExperience[0]
            print(yearsExperience)
        print(yearsExperienceSentence)
    educationLevelSentence = jobDescriptionDiv.find(text=[re.compile(
        "Bachelor"), re.compile("Master"), re.compile("BS "), re.compile(" MS ")])
    jobDict["education"] = str(educationLevelSentence).strip()
    print(educationLevelSentence)

    blob = TextBlob(jobDescriptionDiv.text)
    for sentence in blob.sentences:
        if re.match("Bachelor", str(sentence)) or re.match("BS ", str(sentence)):
            print(sentence)


# required Skills need to be a list and lowercase!!!!
def search_skills(jobDescriptionDiv, jobDict, userSearch):
    # blob = TextBlob(jobDescriptionDiv.text)
    # for sentence in blob.sentences:
    #     if requiredSkills in sentence.words:
    #         print(sentence)
    # if requiredSkills in blob.words:
    #     jobDict["required_skills"] = True
    skills = userSearch["required_skills"]
    string = str(jobDescriptionDiv.text)
    for skill in skills:
        match = re.search(re.escape(skill), string.lower())
        if match:
            print(match.group())
            jobDict["required_skills"].append(str(match.group()).strip())


def score(jobDict, userSearch):
    if userSearch["education"] in jobDict["education"]:
        jobDict["score"] += 1
        print("education!")
    if jobDict["job_type"] == userSearch["job_type"]:
        jobDict["score"] += 1
        print("Job Type!")
    if userSearch["experience"] and jobDict["experience"]:
        if jobDict["experience"] <= int(userSearch["experience"]):
            jobDict["score"] += 1
            print("experience!")
    if len(jobDict["required_skills"]) < 0:
        jobDict["score"] += (len(jobDict["required_skills"]) /
                             len(userSearch["required_skills"]))
    if jobDict["income"] and userSearch["income"]:
        if jobDict["income"] >= int(userSearch["income"]):
            jobDict["score"] += 1
            print("income!")


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
    linkedinJobs = scrape(driver, userSearch)
    driver.quit()
    return linkedinJobs


if __name__ == "__main__":
    keyWord = sys.argv[1]
    location = sys.argv[2]
    driver = setupDriver()
    driver = search(driver, keyWord, location)
    scrape(driver, {'job_title': '', 'location': '', 'income': '', 'key_words': '',
                    'required_skills': ['python'], 'experience': '', 'education': '', 'job_type': ''})
    driver.quit()
