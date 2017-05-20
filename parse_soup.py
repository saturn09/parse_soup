"""
Program for scrapping info from
https://hh.kz/search/vacancy?text=python&only_with_salary=false&area=159&enable_snippets=true
&clusters=true&salary=
"""

import requests
from bs4 import BeautifulSoup
import logging
import pandas as pd
import datetime

# send request to take all content from page
url = "https://hh.kz/search/vacancy?text=python&only_with_salary=false/" \
      "&area=159&enable_snippets=true&clusters=true&salary="


logging.basicConfig(filename="example.log", filemode="w", level=logging.INFO)
# headers for granting access to the website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"
}
f_obj = open("hhkz.txt", "w")

request = requests.get(url, headers = headers)

soup = BeautifulSoup(request.content, "html.parser")

# write all divs with class "search-result-description__item search-result-description__item_primary" to "data" variable
data = soup.find_all("div", {"class": "search-result-description__item search-result-description__item_primary"})

# parse & print info

vacancies, companies, salaries = [], [], []

def parser():
    logging.info("Parsing div tags")
    for div in data:
        logging.info("Appending to vacancies")
        vacancies.append(div.contents[0].text)
        logging.info("Appended: {0}".format(div.contents[0].text))
        is_vacancy(div)
        is_company_name(div)
    logging.info("Parsing finished")


def is_company_name(div):
    i = 2
    while i < 6:
        if "search-result-item__company" in div.contents[i].get("class"):
            logging.info("Appending to companies")
            companies.append(div.contents[i].text)
            logging.info("Appended: {0}".format(div.contents[i].text))
            i = 6
        else:
            i += 1


def is_vacancy(div):
    if "b-vacancy-list-salary" in div.contents[1].get("class"):
        logging.info("Appending to salaries")
        salaries.append(div.contents[1].text)
        logging.info("Appended: {0}".format(div.contents[1].text))

parser()

dataframe = pd.DataFrame({"Vacancies": vacancies,  "Companies": companies})
dataframe.to_csv("example.csv")



