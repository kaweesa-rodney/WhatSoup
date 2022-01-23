from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import sys
import pyautogui
import datetime
import re
from time import *
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
st=time()
def eta(seconds):
    sec=seconds-st
    return "ETA: "+str(datetime.timedelta(seconds=sec))
def valid_date(datestring):
        try:
                mat=re.match('(\d{2})[/.-](\d{2})[/.-](\d{4})$', datestring)
                if mat is not None:
                        datetime.datetime(*(map(int, mat.groups()[-1::-1])))
                        return True
        except ValueError:
                pass
        return False
def scroll():
    for i in range(8):
        pyautogui.press('down')
        sleep(1)
def findmsg(name):
    sleep(2);partial=0
    try:
        driver.find_element_by_class_name('_1ays2').click()
    except:
        return None
    sleep(2)
    for i in range(40):
        sleep(1)
        pyautogui.press('up')
    msg=[name];prev='Unknown';
    sleep(8)
    htmlcode=(driver.page_source).encode('utf-8')
    soup = BeautifulSoup(htmlcode,features="html.parser")
    cnt=0
    for tag in soup.find_all('span'):
        classid=tag.get('class')
        if classid==['_F7Vk', 'selectable-text', 'invisible-space', 'copyable-text']:
            msg.append([tag.text.translate(non_bmp_map).replace('\n', '')])
        if classid==['_3fnHB']:
            try:
                if msg[-1][-1] in [1,2]:
                    msg[-1].append(tag.text)
            except:
                par
                tial=1
        if classid in [['EopGb', '_3HIqo'],['EopGb']]:
            try:
                msg[-1].append(len(classid))
            except:
                partial=1
        if classid == ['_F7Vk']:
            try:
                if tag.text in ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY', 'TODAY', 'YESTERDAY'] or valid_date(tag.text):
                    msg[-1].append(tag.text)
            except:
                if tag.text in ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY', 'TODAY', 'YESTERDAY'] or valid_date(tag.text):
                    prev=tag.text
                partial=1
    for i in msg:
        if len(i)>4:
            i=i[:4]
    
    for i in msg[1:]:
        if len(i)==3:
            i.append(prev)
        else:
            prev=i[-1]
    chats.append(msg)
driver = webdriver.Chrome("./chromedriver_win32/chromedriver.exe")
driver.get("https://web.whatsapp.com/")
sleep(20)
chats=[]
print("Chrome has been automated",eta(time()))

'''elem = driver.find_elements_by_class_name('_3j8Pd')
print(elem)
elem[1].click()
sleep(10)
print("Web Whatsapp Authetication success",eta(time()))'''

mycon=set()
while(True):
    scroll()
    contacts = driver.find_elements_by_css_selector('._3NWy8 span')
    newcon=set([j.text for j in contacts])
    if len(newcon|mycon)==len(mycon):
        break
    else:
        mycon=newcon|mycon
contact=sorted(list(mycon),key=str.casefold)
rotate=dict()
print(len(contact),"contacts has been retrieved",eta(time()))