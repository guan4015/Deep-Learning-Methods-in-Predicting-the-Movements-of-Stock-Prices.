'''
This file scrape all the ticker symbol from Nasdaq
'''

# Import necessary libraries

import urllib2
import csv
import sys
import numpy as np



def getTickers(percent):
    '''

    :param percent: This parameter indicates what is the percentage of the companies used to do further sentiment analysis
    with respect to the sizes of the companies. For instance, the top "percent" percent of companies will be reserved for computing.
    :return:
    '''
    file = open('./input/tickerList.csv', 'w') # open the file
    writer = csv.writer(file,delimiter = ";")  # create a writer object Note that this is really tricky. But why using ";" instead of
    # "," is a mystery.
    capStat, output = np.array([]), []   # create a empty array

    for exchange in ["NASDAQ", "NYSE", "AMEX"]:
        # begin fetching the data from nasdaq
        # define url
        url = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange="
        repeat_times = 10  # repeat downloading in case of http error
        # Try downloading the data
        for _ in range(repeat_times):
            try:
                print "Download tickers from " + exchange
                response = urllib2.urlopen(url + exchange + '&render=download')
                content = response.read().split('\n')

                for num, line in enumerate(content):
                    line = line.strip().strip('"').split('","')
                    if num == 0 or len(line) != 9: continue # filter unmatched format
                    ticker, name, lastSale, MarketCap, IPOyear, sector, \
                    industry = line[0: 4] + line[5: 8]
                    # Market cap statistics
                    capStat = np.append(capStat, float(MarketCap))
                    dataentity = [ticker, name.replace(',', '').replace('.', ''), exchange, MarketCap]
                    #if dataentity[0] == "BCO":
                        #print(dataentity)
                    output.append(dataentity)
                break
            except:
                continue

    for data in output:
        marketCap = float(data[3])
        if marketCap < np.percentile(capStat, 100 - percent): continue
        writer.writerow(data)


def main(toppercentile = 5):
    '''

    :param toppercentile: This parameter indicates the top (toppercentile) companies reserved for further analysis
    :return:
    '''
    s = getTickers(int(toppercentile))    # keep the top N% market-cap companies


if __name__ == "__main__":
    main()