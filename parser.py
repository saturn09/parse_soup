import logging
from datetime import datetime, timedelta
from random import randint as rint

import pandas as pd
import requests
from bs4 import BeautifulSoup

class Parser:
    def __init__(self, url):
        self.url = url

    def connect(self):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
        request = requests.get(url=self.url, headers = headers)
        return request

    def fetch(self):
        data = self.connect()
        soup = BeautifulSoup(data.content, "html.parser")
        info = soup.find_all("div",{"class": "search-result-description__item search-result-description__item_primary"})
        return info

    def obtain(self):
        vacancies, salaries, companies = [], [], []
        info = self.fetch()
        for div in info:
            vacancies.append(self.get_vacancy(div))
            salaries.append(self.get_salary(div))
            companies.append(self.get_company(div))
        return companies, vacancies, salaries

    def get_salary(self, div):
        if "b-vacancy-list-salary" in div.contents[1].get("class"):
            return div.contents[1].text
        return "Salary is not provided by employer"

    def get_vacancy(self, div):
        return div.contents[0].text.replace(",", "")

    def get_company(self, div):
        i = 2
        while i < 6:
            if "search-result-item__company" in div.contents[i].get("class"):
                return div.contents[i].text.replace(",", "")
                i = 6
            else:
                i += 1
    def get_date(self):
        return datetime.now() + timedelta(seconds=rint(0,20))

    def write(self):
        companies, vacancies, salaries = self.obtain()
        df = pd.DataFrame({"Companies": companies, "Salaries": salaries, "Vacancies": vacancies,
                           "Date": [self.get_date() for i in range(len(vacancies))]})
        df.to_csv("python_vacancies.csv", sep="#", encoding="utf-8")

    def run(self):
        self.connect()
        self.fetch()
        self.obtain()
        self.write()

if __name__ == "__main__":
    url = "https://hh.kz/search/vacancy?text=python&enable_" \
          "snippets=true&currency_code=KZT&clusters=true&" \
          "area=159&from=cluster_area"
    parser = Parser(url)
    parser.run()








