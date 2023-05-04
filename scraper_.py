import numpy as np
import pandas as pd
import csv
# import requests
from bs4 import BeautifulSoup
# import bs4
import time
import undetected_chromedriver as uc
from selenium import webdriver
import openpyxl



def read_keywords(hindi=False):
    workbook = openpyxl.load_workbook('keywords.xlsx')
    sheet = workbook.active
    if hindi:
        column_values = [cell.value for cell in sheet['A'][1:]]
    else:
        column_values = [cell.value for cell in sheet['B'][1:]]
    string_list = [str(value) for value in column_values if value]
    return string_list

# undetected_chromedriver works properly in name==main
if __name__ == "__main__":
    driver = uc.Chrome()
    options = webdriver.ChromeOptions()
    # time.sleep(3)
    keywords=read_keywords()
    comments_list = []

    for keyword in keywords:
    # keyword= 'Bhen ke laude'
        url=f'https://www.reddit.com/search/?q={keyword}&source=recent&type=comment'                                                                     #<---------Enter Keyword Here
        driver.get(url)
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
        # with open('comment_reddit.csv', mode='w', newline='') as csv_file:
            #fieldnames = ['Title','Comments']
            # fieldnames = ['Comments']
            # writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            # writer.writeheader()
        if results:
            try:
                comment_container = results.find_all("div", class_="_3tw__eCCe7j-epNCKGXUKk")
            except:
                break

            for comment in comment_container:
                try:

                    #title_element = comment.find("a", class_="wM6scouPXXsFDSZmZPHRo DjcdNGtVXPcxG0yiFXIoZ _23wugcdiaj44hdfugIAlnX ")
                    comment_element = comment.find("p", class_="_1qeIAgB0cPwnLhDF9XSiJM")
                    #print("\n",title_element.text.strip())
                    if comment_element and len(comment_element)>0:
                        print("\n",comment_element.text.strip())
                        dic={'comment':comment_element,'url':url,'keyword':keyword}
                        comments_list.append(comment_element)
                    #writer.writerow({'Title': title_element})
                    # writer.writerow({'Comments': comment_element})
                except:
                    break

    driver.close()
    data1=pd.DataFrame(comments_list)
    data1.to_csv('data_for_keywords.csv')