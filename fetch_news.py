
# Import Necessary Library
import re   # regular expression
import urllib2
import csv
import os
import sys
import time
import datetime

import numpy as np
from bs4 import BeautifulSoup


def dateGenerator(numdays=20):  # generate N days until now
    base = datetime.datetime.today()
    date_list = [base - datetime.timedelta(days=x) for x in range(0, numdays)]
    for i in range(len(date_list)): date_list[i] = date_list[i].strftime("%Y%m%d")
    return date_list

def parser(soup, ticker, timestamp):
    content = soup.find_all("div", {'class': ['topStory', 'feature']})
    if len(content) == 0: return 0
    fout = open('./input/news_stocks.csv', 'a+')
    for i in range(len(content)):
        title = content[i].h2.get_text().replace(",", " ").replace(":","").replace("'","").replace(";","").replace("\n", " ")
        body = content[i].p.get_text().replace(",", " ").replace(":","").replace("'","").replace(";","").replace("\n", " ")

        if i == 0 and len(soup.find_all("div", class_="topStory")) > 0:
            news_type = 'topStory'
        else:
            news_type = 'normal'

        print(ticker, timestamp, title, news_type)
        fout.write(','.join([ticker, timestamp, title, body, news_type]).encode('utf-8') + '\n')
    fout.close()
    return 1

def content_scrape(ticker, name, line, exchange, dateList,repeat_times=2):
    '''

    :param ticker:
    :param name:
    :param line:
    :param exchange:
    :param dateList:
    :return:
    '''

    if exchange == "NASDAQ":
        url1 = "http://www.reuters.com/finance/stocks/company-news/{}.O?".format(ticker)
    else:
        url1 = "http://www.reuters.com/finance/stocks/company-news/{}?".format(ticker)

    for _ in range(repeat_times):  # repeat in case of http failure
        try:
            time.sleep(np.random.poisson(0.2))
            # This is the attempt
            response = urllib2.urlopen(url1)
            data = response.read()
            soup = BeautifulSoup(data, "lxml")
            content = soup.find_all("div", {'class': ['topStory', 'feature']})
            #print(soup.find_all("div", {'class': ['topStory', 'feature']}))
            has_Content = len(content)
            break
        except:
            continue

    if has_Content > 0:
        missing_days = 0
        print(ticker)

        for timestamp in dateList:
            new_time = timestamp[4:] + timestamp[:4]  # change 20151231 to 12312015 to satisfy reuters format
            hasNews = 0
            for _ in range(repeat_times):
                try:
                    time.sleep(np.random.poisson(0.2))
                    url2 = url1 + "date=" + new_time
                    print(url2)
                    response = urllib2.urlopen(url2)
                    data = response.read()
                    soup = BeautifulSoup(data, "lxml")
                    hasNews = parser(soup, ticker, timestamp)
                    if hasNews == 0: break  # stop looping if the content is empty (no error)
                except:  # repeat if http error appears
                    continue
            if hasNews:
                missing_days = 0  # if get news, reset missing_days as 0
            else:
                missing_days += 1
            if missing_days > has_Content * 4 + 20:  # 2 NEWS: wait 30 days and stop, 10 news, wait 70 days
                break  # no news in X consecutive days, stop crawling
            if missing_days > 0 and missing_days % 20 == 0:  # print the process
                print(ticker, "has no news for ", missing_days, " days")
    else:
        print(ticker, "has no single news")


if __name__ == "__main__":
    fin = open('./input/tickerList.csv')

    filterList = set()  # define an empty set

    try:  # this is used when we restart a task
        fList = open('./input/finished.reuters')
        for l in fList:
            filterList.add(l.strip())
    except:
        pass

    lookbackwindow = 300

    dateList = dateGenerator(numdays=lookbackwindow)  # look back on the past X days

    for num, line in enumerate(fin):
        # Test
        if num >= 100:break
        line = line.strip().split(';')
        ticker, name, exchange, MarketCap = line
        if ticker in filterList: continue
        content_scrape(ticker, name, line, exchange, dateList,repeat_times=1)
