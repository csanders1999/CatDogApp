#A lot of the code below is taken from this blog post: https://blog.chapagain.com.np/python-nltk-twitter-sentiment-analysis-natural-language-processing-nlp/
# I made some modifications so it suits our needs.
##I will put the authors name (chapagain) on code I got from the above source.

#Import the data set from the nltk module.
from nltk.corpus import twitter_samples 
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
import string 
import re
from nltk.corpus import stopwords 
from nltk.tokenize import TweetTokenizer
import pickle

stopwords_english = stopwords.words('english') #(chapagain)

#Divide the data set into positive and negative tweets. (chapagain)
positive_tweets = twitter_samples.strings('positive_tweets.json')
negative_tweets = twitter_samples.strings('negative_tweets.json')


#Check if item is emoji.
from emoji import UNICODE_EMOJI
def is_emoji(string):
    return string in UNICODE_EMOJI

#From chapagain source.
#Cleans the tweet of unneccesary items.
def clean_tweets(tweet):
    # remove stock market tickers like $GE (chapagain)
    tweet = re.sub(r'\$\w*', '', tweet)

    # remove old style retweet text "RT" (chapagain)
    tweet = re.sub(r'^RT[\s]+', '', tweet)
 
    # remove hyperlinks (chapagain)
    tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)
    
    # remove hashtags (chapagain)
    # only removing the hash # sign from the word
    tweet = re.sub(r'#', '', tweet)

    #tokenize the tweets (chapagain)
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
    tokens = tokenizer.tokenize(tweet)

    result = []
    for word in tokens:
        if (word not in stopwords_english and word not in string.punctuation and not is_emoji(word)):
            result.append(stemmer.stem(word))
    
    return result


# feature extractor function (chapagain)
def bag_of_words(tweet):
    words = clean_tweets(tweet)
    words_dictionary = dict([word, True] for word in words)    
    return words_dictionary

# positive tweets feature set (chapagain)
pos_tweets_set = []
for tweet in positive_tweets:
    pos_tweets_set.append((bag_of_words(tweet), 'pos'))    
 
# negative tweets feature set (chapagain)
neg_tweets_set = []
for tweet in negative_tweets:
    neg_tweets_set.append((bag_of_words(tweet), 'neg'))


# radomize pos_reviews_set and neg_reviews_set (chapagain)
# doing so will output different accuracy result everytime we run the program
from random import shuffle 
shuffle(pos_tweets_set)
shuffle(neg_tweets_set)
 
test_set = pos_tweets_set[:2500] + neg_tweets_set[:2500]
train_set = pos_tweets_set[2500:] + neg_tweets_set[2500:]

#Train the model using a naivebayes classifier (chapagain)
from nltk import classify
from nltk import NaiveBayesClassifier
 
classifier = NaiveBayesClassifier.train(train_set)


#Save the classifier for later use.
with open("naive_bayes_model.pickle", "wb") as file:
    pickle.dump(classifier, file)