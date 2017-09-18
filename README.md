

# Sentiment Analysis of Financial News in Predicting the Movements of Stock Prices.

The current status of this project is to use Natural Language Processing to predict the trends of stock markets. This project starts from fetching the ticker symbols and financial news from NASDAQ and Reuters, then we convert the words in each sentence by applying the GloVe representations, proposed by Jeffrey Pennington et al . The last but not least, we adpot the convolutional neural network proposed by Yoon Kim to build the forecasting models to predict the movements of stock prices. 



## Data Fetching and Cleaning

We start from the data fetching process.

### Ticker Symbol Fetching

In this section, we scrape the data from NASDAQ, which contains the information of ticker, company name, lastSale, Market Capital, IPO year, sector and industry. Then these information is stored in the file "./input/tickerList.csv". The python codes are wrapped in the following file

```
ticker_sracpy.py
```

### News Fetching

The next step is to fetch the stock news. This process is done by creating the link to Reuters. For all the companies recorded in the "tickerList.csv" file, we fetch the news corresponding to each ticker symbol up to N days. If there is no news in the current date, we just skip it. It then creates a another .csv file to record the news title and news contents as well as the class given by Reuters. At present, there are only two classes: "top story" and "normal". Basically, we only focus on the top news in building the prediction models. The retrieval of the news can be done in the following .py file

Say what the step will be

```
fetch_news.py
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
