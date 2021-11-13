from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import requests
import re


chrome_options = Options()
chrome_options.add_experimental_option("detach", True) # So window doesn't close
driver = webdriver.Chrome("/Users/nadavskloot/Documents/GitHub/comp446/better_job_finder/chromedriver", chrome_options=chrome_options) # add your path to chromedriver, mine is "/Users/nadavskloot/Documents/GitHub/comp446/better_job_finder/chromedriver"
driver.get("https://www.linkedin.com/jobs")
#cookie for username: rroczbikpplzvhotou@mrvpt.com, pass: hebedebe
cookie = {'name': "li_at",'value':"AQEDATiE-woDvY3iAAABfRYyfewAAAF9Oj8B7E4AySbBRJeEri4Uig-2B1hlS4dhO7btpUwcnJljINARdtGB6IUdmWiWhDxpSWc0P9rhH5wlCx_2ugoDz0lvQumpl-gOuHVp-7uBGeYDhEkwXVi9ETBn"}
driver.add_cookie(cookie)


jobInput = driver.find_elements(By.NAME, "keywords")[0]
jobLocation = driver.find_elements(By.NAME, "location")[0]
# str(jobInput.is_displayed())
jobInput.clear()
jobInput.send_keys("hello")
jobLocation.clear()
jobLocation.send_keys("hello")

jobInput.send_keys(Keys.RETURN)



page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

jobTitles = soup.find_all("a", attrs={'class': re.compile("job-card-list__title")})

jobs = []
for a in jobTitles:
    jobs.append({"title":a.text.strip()})

print(jobs)