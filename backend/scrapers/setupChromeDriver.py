import os
import zipfile
import xmltodict
import platform
import requests


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
        if os.popen(f'{driver_folder}/chromedriver'.replace(' ', '\\ ')+' -v').read().split(' ')[1].split('.')[0:2] == chromeVersion.split('.')[0:2]:
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
