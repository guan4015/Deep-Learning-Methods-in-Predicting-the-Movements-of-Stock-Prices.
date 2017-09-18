
import datetime
import sys
import urllib2
import re
import os
import time
import urllib
import urllib2
import pandas_datareader.data as web
import random
import json
from math import log

# output file name: input/stockPrices_raw.json
# json structure: crawl daily price data from yahoo finance
#          ticker
#         /  |   \
#     open close adjust ...
#       /    |     \
#    dates dates  dates ...

def calc_finished_ticker():
    # This one generates the list of tickers in the recorded news file
    os.system("awk -F',' '{print $1}' ./input/news_stocks.csv | sort | uniq > ./input/finished.reuters")

def get_stock_Prices(startdate = datetime.datetime(2016,7,1),enddate=datetime.date.today()):
    '''
    This function is used to get ticker symbols from the ticker symbol file.
    It returns a json file which contains the prices of the tickers from start date to end date.
    :return:
    '''
    # Specify the path of input file and output file
    fin = open('./input/finished.reuters')
    output = './input/stockPrices_raw.json'

    # exit if the output already existed
    if os.path.isfile(output):
        sys.exit("Prices data already existed!")


    # Initialize the priceSet
    priceSet = {}
    priceSet['^GSPC'] = repeatDownload('^GSPC',startdate,enddate) # download price history S&P 500

    for num, line in enumerate(fin):
        ticker = line.strip()
        print(num, ticker)
        priceSet[ticker] = repeatDownload(ticker,startdate,enddate)  # record the price
        #if num > 10: break # for testing purpose

    with open(output, 'w') as outfile:
        json.dump(priceSet, outfile, indent=4)
#
#
def repeatDownload(ticker,startdate,enddate):
    repeat_times = 1  # repeat download for N times
    for _ in range(repeat_times):
        try:
            time.sleep(random.uniform(0, 0.5))
            priceStr = PRICE(ticker,startdate,enddate)
            if len(priceStr) > 0:     # skip loop if data is not empty
                break
        except:
            if _ == 0: print ticker, "Http error!"
    return priceStr

#
def PRICE(ticker,startdate,enddate):
    #start = datetime.datetime(2016, 9, 5)
    #end = datetime.datetime(2017, 9, 5)
    # Construct url
    #url = https://query1.finance.yahoo.com/v7/finance/download/%5EGSPC?period1=1473048000&period2=1504584000&interval=1d&events=history&crumb=3mH28u4nQ71
    #url1 = "http://chart.finance.yahoo.com/table.csv?s=" + ticker
    #url2 = "&a=" + start_m + "&b=" + start_d + "&c=" + start_y
    #url3 = "&d=" + end_m + "&e=" + end_d + "&f=" + end_y + "&g=d&ignore=.csv"

    # parse url and link the target file, read the file with split \n.
    #response = urllib2.urlopen(url1 + url2 + url3)
    #csv = response.read().split('\n')
    ticker_data = web.DataReader(ticker, "yahoo", startdate, enddate)
    ticker_csv = ticker_data.to_csv("./input/stockdata/{}.csv".format(ticker), mode="w", header=True)
    ticker_document = open("./input/stockdata/{}.csv".format(ticker))

    # get historical price
    ticker_price = {}
    index = ['open', 'high', 'low', 'close', 'adjClose', 'volume']
    for num, line in enumerate(ticker_document):
        line = line.strip().split(',')
        if len(line) < 7 or num == 0: continue
        date = line[0]
        # check if the date type matched with the standard type
        if not re.search('\d{4}(?P<sep>[-/])\d{2}(?P=sep)\d{2}', date): continue
        # open, high, low, close, volume, adjClose : 1,2,3,4,5,6

        for index_num, typeName in enumerate(index):
            try:
                ticker_price[typeName][date] = round(float(line[index_num + 1]),2)
            except:
                ticker_price[typeName] = {}
    return ticker_price


if __name__ == "__main__":
    #calc_finished_ticker()
    startdate = datetime.datetime(2016,9,5)
    enddate = datetime.datetime(2017,9,5)
    get_stock_Prices(startdate= startdate,enddate=enddate)