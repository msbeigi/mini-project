import numpy as np
import pandas as pd
import csv
# import requests
from bs4 import BeautifulSoup
# import bs4
import time
import undetected_chromedriver as uc
from selenium import webdriver


# undetected_chromedriver works properly in name==main
if __name__ == "__main__": 
    driver = uc.Chrome()
    options = webdriver.ChromeOptions() 
    time.sleep(3)
    driver.get('https://www.reddit.com/search/?q=Kamini&type=comment')
    time.sleep(10)
    while True:
        last_height = driver.execute_script("return document.body.scrollHeight")
        print('Last hieght:', last_height)
        time.sleep(1)
        for i in range(5):
            driver.execute_script("window.scrollTo(0, window.scrollY + 1500)")
            time.sleep(2) # Scroll to get maximum entries
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
    soup=BeautifulSoup(driver.page_source)
    results = soup.find(class_="_1BJGsKulUQfhJyO19XsBph")
    with open('comment_reddit.csv', mode='w', newline='') as csv_file:
        #fieldnames = ['Title','Comments']
        fieldnames = ['Comments']
        # writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        # writer.writeheader()

        comment_container = results.find_all("div", class_="_3tw__eCCe7j-epNCKGXUKk")
        comments_list = []
        for comment in comment_container:
            #title_element = comment.find("a", class_="wM6scouPXXsFDSZmZPHRo DjcdNGtVXPcxG0yiFXIoZ _23wugcdiaj44hdfugIAlnX ")
            comment_element = comment.find("p", class_="_1qeIAgB0cPwnLhDF9XSiJM")
            #print("\n",title_element.text.strip())
            print("\n",comment_element.text.strip())
            comments_list.append(comment_element)
            #writer.writerow({'Title': title_element})
            # writer.writerow({'Comments': comment_element})
        driver.close()
        data1=pd.DataFrame(comments_list,columns =['Comments'])
        data1.to_csv('Kamini.csv')
