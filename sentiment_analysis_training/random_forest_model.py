#Some code pulled from the following resource:
#https://towardsdatascience.com/multi-class-text-classification-with-sklearn-and-nltk-in-python-a-software-engineering-use-case-779d4a28ba5
#I will put the authors name (Nasir Safdari) on code I got from the above source.
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, chi2
import pickle


#Name input file.
#Please get the training set from https://docs.google.com/file/d/0B04GJPshIjmPRnZManQwWEdTZjg/edit. If you don't want to train, and only test,
#import the classifier as shown in predict_tweet.py
#I used the 1600000 processed data set.
input_file = "training_set.csv"

#Import csv. The dataset is already cleaned. 
df = pd.read_csv(input_file, encoding="ISO-8859-1", names = ["Polarity", "ID", "Date", "idk", "User", "Tweet"])
df = df[["Tweet", "Polarity"]]

#Get X and Y sets.
X = df["Tweet"]
Y = df["Polarity"]

#Split into training and testing data.
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, train_size=.1)


vectorizer = TfidfVectorizer(min_df= 3, stop_words="english", sublinear_tf=True) #Nasir Safdari

pipeline = Pipeline([('vect', vectorizer), #Nasir Safdari
                     ('chi',  SelectKBest(chi2, k=1000)),
                     ('clf', RandomForestClassifier())])

# fitting our model and save it in a pickle for later use.
# #Nasir Safdari
model = pipeline.fit(X_train, y_train)
with open('RandomForest.pickle', 'wb') as f:
    pickle.dump(model, f)