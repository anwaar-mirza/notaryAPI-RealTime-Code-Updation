from smtplib import SMTP
from email.message import EmailMessage
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options
opt = Options()
opt.add_argument('--headless')
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=opt)
def task_starting_email(total_num):
    smtp = SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login('anwaarmirza65@gmail.com', 'wicf zgki zvzc nton')
    receiver = ['anwaar@metaviz.pro', 'zainalijamil89@gmail.com']
    sender = 'anwaarmirza65@gmail.com'
    subject = 'API Scraping Start'
    body = f'''
    Hi dear,

    I wanted to inform you that the scheduled web scraping task has been successfully initiated on Blue Ocean.

    Total number of listings found are {total_num}. Which having either snapdocs or zigsig or both URLs in their profiles. 

    You will receive an email once the signing scores for all {total_num} listings are updated in BD database.  
    '''
    mail = EmailMessage()
    mail['From'] = sender
    mail['To'] = ", ".join(receiver)
    mail['Subject'] = subject
    mail.set_content(body)
    smtp.send_message(mail)
    smtp.close()
    print("Mail send successfully")

def task_middle_message(number):
    smtp = SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login('anwaarmirza65@gmail.com', 'wicf zgki zvzc nton')
    receiver = ['anwaar@metaviz.pro', 'zainalijamil89@gmail.com']
    sender = 'anwaarmirza65@gmail.com'
    subject = 'How many listings scraped?'
    body = f'''
        Hi dear,

        I wanted to inform you that the {number} listings in scheduled task has been successfully scraped that initiated on Blue Ocean.

        Best Regards,

        Muhammad Anwaar
        '''
    mail = EmailMessage()
    mail['From'] = sender
    for r in receiver:
        mail['To'] = r
        mail['Subject'] = subject
        mail.set_content(body)
        smtp.send_message(mail)
    smtp.close()

def task_closed():
    smtp = SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login('anwaarmirza65@gmail.com', 'wicf zgki zvzc nton')
    receiver = ['anwaar@metaviz.pro', 'zainalijamil89@gmail.com']
    sender = 'anwaarmirza65@gmail.com'
    subject = 'API Scraping Finish'
    body = '''
        Hi dear,

        I wanted to inform you that the scheduled web scraping task has been successfully completed on Blue Ocean.

        Best Regards,

        Muhammad Anwaar
        '''
    mail = EmailMessage()
    mail['From'] = sender
    for r in receiver:
        mail['To'] = r
        mail['Subject'] = subject
        mail.set_content(body)
        smtp.send_message(mail)
    smtp.close()

def api_not_working():
    smtp = SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login('anwaarmirza65@gmail.com', 'wicf zgki zvzc nton')
    receiver = ['anwaar@metaviz.pro', 'zainalijamil89@gmail.com']
    sender = 'anwaarmirza65@gmail.com'
    subject = 'API Not Working'
    body = '''
            Hi dear,

            I wanted to inform you that the API of notary not working.....

            Best Regards,

            Muhammad Anwaar
            '''
    mail = EmailMessage()
    mail['From'] = sender
    for r in receiver:
        mail['To'] = r
        mail['Subject'] = subject
        mail.set_content(body)
        smtp.send_message(mail)
    smtp.close()

def get_snapdoc(url1):
    try:
        driver.get(url1)
        sign1 = driver.find_element(By.XPATH, '//div[@class="info-row" and span[text() = "Snapdocs Signings Completed:"]]/span[2]').text
        driver.implicitly_wait(5)
        return sign1
    except:
        return 0

def get_zigzig(url2):
    try:
        driver.get(url2)
        sign2 = driver.find_element(By.XPATH, '//div[@class="col-xs-5 signingsMobileDiv" and p[contains(text(), "LifeTime Signings")]]/h3').text
        driver.implicitly_wait(5)
        return sign2
    except:
        return 0


response = requests.get('https://www.notarystars.com/api/widget/json/get/notary-stars-apis?api_type=users&limit=500')

if response.status_code == 200:
    data = json.loads(response.content)
    data1 = data['data']
    data2 = data1['data']
    task_starting_email(data1['total'])
    for i, d in enumerate(data2):
        if (i+1) % 100 == 0:
            task_middle_message(i+1)
            print(str(i+1)+": "+str(d))
            print(d['user_id'])
            if d['snapdocs_profile_link'] != "None":
                res1 = get_snapdoc(d['snapdocs_profile_link'])
                print(d['snapdocs_profile_link'])
                print(res1)
            else:
                print("Snapdoc not found")
                res1 = 0

            if d['zig_sig_profile_link'] != "None":
                res2 = get_zigzig(d['zig_sig_profile_link'])
                print(d['zig_sig_profile_link'])
                print(res2)
            else:
                res2 = 0
                print("Zig Zig not found")

        else:
            print(str(i + 1) + ": " + str(d))
            print(d['user_id'])
            if d['snapdocs_profile_link'] != "None":
                res1 = get_snapdoc(d['snapdocs_profile_link'])
                print(d['snapdocs_profile_link'])
                print(res1)
            else:
                print("Snapdoc not found")
                res1 = 0

            if d['zig_sig_profile_link'] != "None":
                res2 = get_zigzig(d['zig_sig_profile_link'])
                print(d['zig_sig_profile_link'])
                print(res2)
            else:
                res2 = 0
                print("Zig Zig not found")

        url_to_post = f"https://www.notarystars.com/api/widget/json/get/notary-stars-apis?api_type=update_user&user_id={d['user_id']}&snapdocs_signings={res1}&zigsig_signings={res2}"
        data = {}
        rep2 = requests.post(url_to_post, json=data)
        print(rep2.json())
        print("*************************************************")

else:
    api_not_working()

task_closed()
