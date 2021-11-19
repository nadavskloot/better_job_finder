from bs4 import BeautifulSoup
import requests

base_url = "https://www.indeed.com/jobs?q=software%20engineer&l=Saint%20Paul%2C%20MN&vjk=d22e26283d8484f6"
r = requests.get(base_url)
soup = BeautifulSoup(r.content, 'html.parser')

# Get all company names:
tags = soup.find_all('h2')
# Collect info from the span tags
collect_info = []
for tag in tags:
#     print(tag.attrs)
    if "class" in tag.attrs.keys():
        print(tag.attrs["class"])
        if "jobTitle" in tag.attrs["class"]:
            info = tag.text
            collect_info.append(info)

print(collect_info)