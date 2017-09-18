

# This document defines several useful tools in generating feature matrix
import json
import os
import en
import datetime
import nltk
import numpy as np



def dateGenerator(numdays):  # generate N days until now, eg [20151231, 20151230]
    base = datetime.datetime(2017,9,5)
    date_list = [base - datetime.timedelta(days=x) for x in range(0, numdays)]
    for i in range(len(date_list)): date_list[i] = date_list[i].strftime("%Y%m%d")
    return set(date_list)



def unify_word(word):  # went -> go, apples -> apple, BIG -> big
    try:
        word = en.verb.present(word)  # unify tense
    except:
        pass
    try:
        word = en.noun.singular(word)  # unify noun
    except:
        pass
    return word.lower()



def padding(sentencesVec, keepNum):
    shape = sentencesVec.shape[0]
    ownLen = sentencesVec.shape[1]
    if ownLen < keepNum:
        return np.hstack((np.zeros([shape, keepNum - ownLen]), sentencesVec)).flatten()
    else:
        return sentencesVec[:, -keepNum:].flatten()


def feature_preprocess(sentencesVec, preserve):
    '''
    
    :param sentencesVec: 
    :param preserve: 
    :return: 
    '''
    shape = sentencesVec.shape[0]  # word representation dimension
    sentencelength = sentencesVec.shape[1]  # sentence length

    # calculate statistics
    mean = np.mean(sentencesVec,axis=1)
    min = np.min(sentencesVec,axis=1)
    max = np.max(sentencesVec,axis=1)
    per25 = np.matrix(np.percentile(sentencesVec,25,axis=1).reshape(shape,1))
    per75 = np.matrix(np.percentile(sentencesVec,75,axis=1).reshape(shape,1))
    std = np.std(sentencesVec,axis=1)

    if preserve == 0:
        stat = np.hstack((mean,min,per25,per75,max,std))
        #print(stat.shape)
        return stat.flatten("F")
    else:
        stat = np.hstack((mean,min,per25,per75,max,std))
        if preserve > sentencelength:
            print("The length of the sentence length is not enough long")
            result = np.hstack((stat,sentencesVec[:,:sentencelength]))
            result = np.hstack((np.zeros([shape, preserve - sentencelength])), result)
            return result.flatten("F")
        else:
            result = np.hstack((stat,sentencesVec[:,:sentencelength])).flatten("F")
            return result


