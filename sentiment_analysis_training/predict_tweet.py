#Importing the classifiers and testing them.
from nltk import classify
from nltk import NaiveBayesClassifier
from naive_bayes_model import bag_of_words
import pickle 

#Text you want to classify:
tweet = "i had such a great day with my dog"

#Load the naive bayes classifer
with open('naive_bayes_model.pickle', 'rb') as file:
    nb_classifier = pickle.load(file)

#Clean the tweets and classify.
custom_tweet_set = bag_of_words(tweet)
print("Naive bayes predicted as: " + nb_classifier.classify(custom_tweet_set)) 

#Import the random forrest classifier.
from sklearn.pipeline import Pipeline
with open('RandomForest.pickle', 'rb') as f:
    rf_classifier = pickle.load(f)

#Predict.
print("Random forrest predicted a polarity of: " + str(rf_classifier.predict([tweet])))