from textblob import TextBlob
from header import *
from harvest import *

twitter_api = oauth_login()

# Add Twitter user you want tweets from here
screen_name = ''
user_tweets = harvest_user_timeline(twitter_api, screen_name)

# Classifying terms. Going to add more.
cat_names = [" cat ", " kitten ", " kitty ", " meow ", " feline "]
dog_names = [" dog ", " doggy ", " pupper ", " doggo ", \
             " puppy ", " woof ", " borker ", " yapper ", \
             " hound ", " golden retriever ", " siberian husky ",]

# Lists of sentiment scores per each tweet
final_cat_scores = []
final_dog_scores = []

for tweet in user_tweets:
    if any(name in tweet.lower() for name in cat_names) and \
       any(name in tweet.lower() for name in dog_names):
        # Need to add way to parse sentance if contains both cat
        # and dog classifiers (i.e. "I hate cats but I love dogs")
        # should add a negative sentiment score to final_cat_scores
        # and positive to final_dog_scores
        break
    elif any(name in tweet.lower() for name in cat_names):
         # print("Cat: ",tweet)
         blob = TextBlob(tweet)
         final_cat_scores.append(blob.sentiment.polarity)
    elif any(name in tweet.lower() for name in dog_names):
        # print("Dog: ",tweet)
        blob = TextBlob(tweet)
        final_dog_scores.append(blob.sentiment.polarity)

# Sum of sentiment scores for all tweets containing cat or dog classifiers
cat_sa_score = sum(final_cat_scores)
dog_sa_score = sum(final_dog_scores)

print("Final dog score: ", dog_sa_score)
print("Final cat score: ", cat_sa_score)
