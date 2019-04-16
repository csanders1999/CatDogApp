from header import *
from harvest import *

twitter_api = oauth_login()
screen_name = 'caitsands'
user_tweets = harvest_user_timeline(twitter_api, screen_name)

cat_names = ["cat", "kitten", "kitty"]
dog_names = ["dog", "doggy", "pupper", "doggo", "puppy"]

final_cat_scores = []
final_dog_scores = []

for tweet in user_tweets:
     if any(name in tweet.lower() for name in cat_names):
        # get sentiment analsyis for that tweet and add to final_cat_scores
         final_cat_scores.append(1)
     if any(name in tweet.lower() for name in dog_names):
        # get sentiment analsyis for that tweet and add to final_dog_scores
        final_dog_scores.append(1)

print(''.join(str(e) for e in final_cat_scores))
print(''.join(str(e) for e in final_dog_scores))
