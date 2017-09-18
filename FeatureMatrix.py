#!/usr/bin/python
import json
import os
import en
import nltk
import numpy as np
import util
from nltk.corpus import stopwords


# Use pretrained word vector to generate our target features
# required input data:
# ./input/glove.xB.xd.txt
# ./input/stopWords
# ./input/stockReturns.json
# ./input/news_reuters.csv
# ./input/featureMatrix

# output file name:
# input/featureMatrix_train
# input/featureMatrix_test


def wordVec(glove_file):
    wordDict = {}
    with open(glove_file) as f:
        print("Loading word vector ...")
        for line in f:
            line = line.strip().split(' ')
            key, values = line[0], map(float, line[1:])
            wordDict[key] = values
    return wordDict, len(values) # return word vector and word vector dimension


def gen_FeatureMatrix(news_file, price_file, output, wordDict, dim_wordVec, term_type, mtype, preserve = 0, sentense_len=20, stopWords_file=None):
    with open(price_file) as file:
        print("Loading price info ...")
        priceDt = json.load(file)[term_type]
    cnt = 0
    testDates = util.dateGenerator(50)
    os.system('rm ' + output + mtype)

    stopWords = set()
    stopWords = set(stopwords.words('english'))

    # with open(stopWords_file) as file:
    #     for word in file:
    #         stopWords.add(word.strip())

    with open(news_file) as f:
        for line in f:
            line = line.strip().split(',')
            if len(line) != 5: continue
            '''
            newsType: [topStory, normal]
            '''
            ticker, day, headline, body, newsType = line
            if newsType != 'topStory': continue # skip normal news
            if ticker not in priceDt: continue   # skip if no corresponding company found
            if day not in priceDt[ticker]: continue # skip if no corresponding date found

            # if cnt > 20: continue


            if mtype == "test" and day not in testDates: continue
            if mtype == "train" and day in testDates: continue

            cnt += 1
            if cnt % 100 == 0: print("%sing samples %d" % (mtype, cnt))

            # 2.1 tokenize sentense, check if the word belongs to the top words, unify the format of words
            #headline = headline.encode('utf-8')
            #body = body.encode('utf-8')

            tokens = nltk.word_tokenize(headline)   # + nltk.word_tokenize(body)
            tokens = map(util.unify_word, tokens)

            # build feature and label
            feature = np.zeros([dim_wordVec,0])
            featureNone = True

            for t in tokens:
                # if t in stopWords: continue
                if t not in wordDict: continue
                featureNone = False
                feature = np.hstack((feature, np.matrix(wordDict[t]).T))
            if featureNone: continue # feature is empty, continue

            #feature = util.padding(feature, sentense_len)
            feature = util.feature_preprocess(sentencesVec=feature,preserve=preserve)

            # mean = np.mean(feature, axis=1)
            # min = np.min(feature, axis=1)
            # max = np.max(feature, axis=1)
            # per25 = np.percentile(feature, 25, axis=1)
            # per75 = np.percentile(feature, 75, axis=1)
            # std = np.std(feature, axis=1)

            #stat = np.matrix(np.hstack((mean,min,max,per25,per75,std)))

            label = round(priceDt[ticker][day], 6)

            with open(output + mtype, 'a+') as file:
                np.savetxt(file, np.hstack((feature, np.matrix(label))), fmt='%.5f')

def main():
    glove_file = "./input/glove.6B.100d.txt"
    news_file = "./input/news_stocks.csv"
    #stopWords_file = "./input/stopWords"
    price_file = "./input/stockReturns.json"
    output = './input/featureMatrix_'
    #sentense_len = 20
    term_type = 'short'
    wordDict, dim_wordVec = wordVec(glove_file)
    gen_FeatureMatrix(news_file, price_file, output, wordDict, dim_wordVec, term_type, mtype = 'train')
    gen_FeatureMatrix(news_file, price_file, output, wordDict, dim_wordVec, term_type, mtype = 'test')


if __name__ == "__main__":
    main()