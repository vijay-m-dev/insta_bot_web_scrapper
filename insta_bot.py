from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from secrets import usr,pw
from bs4 import BeautifulSoup

#login
def login():
    username=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name='username']")))
    username.send_keys(usr)
    password=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input[name='password']")))
    password.send_keys(pw)
    login=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[type='submit']"))).click()
    not_now1=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(text(),'Not Now')]"))).click()
    not_now2=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(text(),'Not Now')]"))).click()
    user=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[5]/span"))).click()
    profile=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div[2]/div[2]/a[1]"))).click()
    time.sleep(3)

def get_logged_in_user_details():
    content=driver.page_source.encode("utf-8").strip()
    insta_soup=BeautifulSoup(content,"lxml")
    name=insta_soup.find("h2",class_="_7UhW9").text
    posts=insta_soup.find_all("span",class_="g47SY")
    detail=[]
    detail.append(name)
    for i in posts:
        numeric_type=convert_str_to_numbers(i.text)
        detail.append(numeric_type)
    return detail

def get_users_details():
    users_details=[]
    content=driver.page_source.encode("utf-8").strip()
    insta_soup=BeautifulSoup(content,"lxml")
    links=insta_soup.find_all("a",class_="FPmhX")
    for link in links:
        user=link.get('href')
        driver.get("https://www.instagram.com"+user)
        time.sleep(3)
        content=driver.page_source.encode("utf-8").strip()
        insta_soup=BeautifulSoup(content,"lxml")
        name=insta_soup.find("h2",class_="_7UhW9").text
        posts=insta_soup.find_all("span",class_="g47SY")
        each_user=[]
        each_user.append(name)
        for i in posts:
            numeric_type=convert_str_to_numbers(i.text)
            each_user.append(numeric_type)
        users_details.append(each_user)
    return users_details

def scrolling_users_list(n):
    fbody=driver.find_element_by_xpath("//div[@class='isgrP']")
    scroll=0
    while(scroll<n):
        driver.execute_script('arguments[0].scrollTop=arguments[0].scrollTop+arguments[0].offsetHeight;',fbody)
        time.sleep(1)
        scroll+=1

def clicking_follow_and_scrolling(n,nth_li):
    following=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/section/main/div/header/section/ul/li["+nth_li+"]/a"))).click()
    time.sleep(5)
    scrolling_users_list(n)

def convert_str_to_numbers(n):
    numeric_type=n.replace(',','')
    if 'k' in numeric_type and '.' in numeric_type:
        numeric_type=numeric_type.replace('.','')
        numeric_type=numeric_type.replace('k','00')
    elif 'm' in numeric_type and '.' in numeric_type:
        numeric_type=numeric_type.replace('.','')
        numeric_type=numeric_type.replace('m','00000')
    elif 'k' in numeric_type and '.' not in numeric_type:
        numeric_type=numeric_type.replace('k','000')
    elif 'm' in numeric_type and '.' not in numeric_type:
        numeric_type=numeric_type.replace('m','000000')
    numeric_type=int(numeric_type)
    return numeric_type



driver=webdriver.Chrome("D:/chromedriver.exe")
driver.get("https://www.instagram.com/")
login()
detail=get_logged_in_user_details()
print(detail)


clicking_follow_and_scrolling(detail[2],"2")
followers=get_users_details()
print(followers)

driver.get("https://www.instagram.com/"+detail[0])
clicking_follow_and_scrolling(detail[3],"3")
following=get_users_details()
print(following)

