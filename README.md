

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

### Stock Prices Download

For each ticker that contains news up to N days before, we record their ticker symbols and create a list. Next, we acquire the stock prices data associated with each ticker up to N days before. Then these information will be stored in a json file, which behaves similar to a NoSQL. The execuation of the following file will produces the stock prices files.

```
fetch_stock_data.py
```
For the reason that the direct download of stock prices data suffer a url issue. We utilize the pandas datareader to achieve this task. 

End with an example of getting some data out of the system or using it for a little demo

## Words Representations and Feature Matrices

In this section, we explain how to convert words into features/proper representations and obtain the feature matrix.

### Word Representations

In this project, we adopted the models proposed by Jeffrey Pennington et al to obtain the word representations. More specifically, we used the pre-trained word vectors "glove6B100d.txt" to acquire the representations. If you prefer to use your own corpus, you are encouraged to refer to the following codes.

```
WordEmbedding.py
```

### Feature Matrices Generation

Once we have words representations on hand, then it is time to generate feature matrices. In this part, we traverse each word in one sentence and convert them into a matrx. Then these matrices will be horizontally stacked to form a series of tensors, which will be the input of the models.

```
FeatureMatrix.py
```

## Model Deployment

In this part, we apply the structure proposed by [Yoon Kim](http://www.people.fas.harvard.edu/~yoonkim/data/sent-cnn.pdf). The model has only two layers, the convolutional layer which consist of 64 2$\times$100 filters. The current model is built upon Keras under the TensorFlow backend. The TensorFlow version will be posted later.

'''
CnnModel.py
'''



## Contributing

Please contact me [CONTRIBUTING.md](xg720@nyu.edu) for and the process for submitting pull requests to me.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/guan4015/Deep-Learning-Methods-in-Predicting-the-Movements-of-Stock-Prices). 

## Authors

* **Xiao Guan**  

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments


