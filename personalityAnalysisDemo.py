from header import *

###############################################################################
###############################################################################
##                                                                           ##
##                             API Key Log-Ins                               ##
##                                                                           ##
###############################################################################
###############################################################################

# api keys for IBM's PersonalityInsightsV3
def ibm_login():
    return PersonalityInsightsV3(
        version=myVersion,
        iam_apikey=myIam_apikey,
        url=myUrl
    )

###############################################################################
###############################################################################
##                                                                           ##
##                         My Functions and Methods                          ##
##                                                                           ##
###############################################################################
###############################################################################

def reduce_status(s):
    # My code here
    return {
        'content': s['text'],
        'contenttype': 'text/plain',
        'created': time.mktime(time.strptime(s['created_at'],"%a %b %d %H:%M:%S +0000 %Y")),
        'id': str(s['id']),
        'language': s['lang']
    }

###############################################################################
###############################################################################
##                                                                           ##
##                         WHERE THE MAGIC HAPPENS                           ##
##                                                                           ##
###############################################################################
###############################################################################

if __name__ == "__main__":
    twitter_api = oauth_login()
    personality_insights = ibm_login()

    user_list = ['TysonOwens']
    dog_list = []
    cat_list = []

    research_dog = {
        'movie_romance' : 0,
        'movie_adventure' : 0,
        'movie_horror' : 0,
        'movie_musical' : 0,
        'movie_historical' : 0,
        'movie_scifi' : 0,
        'movie_war' : 0,
        'movie_drama' : 0,
        'movie_action' : 0,
        'movie_document' : 0
    }

    research_cat = research_dog.copy()

    # Classifying terms. Going to add more.
    cat_names = [" cat ", " kitten ", " kitty ", " meow ", " feline "]
    dog_names = [" dog ", " doggy ", " pupper ", " doggo ", \
                 " puppy ", " woof ", " borker ", " yapper ", \
                 " hound ", " golden retriever ", " siberian husky ",]

    MAXUSER = 1000

    ############### CLASSIIFY USERS AS CAT OR DOG PERSON #####################
    max_users = MAXUSER
    for user in user_list:
        if max_users <= 0:
            break
        print("Fetching more people...")
        if len(user_list) < MAXUSER:
            friends_ids, followers_ids = get_friends_followers_ids(twitter_api,
                                                                   screen_name=user,
                                                                   friends_limit=50,
                                                                   followers_limit=50)
            friends_ids = get_user_profile(twitter_api, user_ids=list(friends_ids))
            for userID in friends_ids:
                if friends_ids[userID]['screen_name'] not in user_list:
                    user_list.append(friends_ids[userID]['screen_name'])

        print('Attempting to classify ', user)
        user_tweets = harvest_user_timeline(twitter_api, screen_name=user, max_results=200)

        # Lists of sentiment scores per each tweet
        final_cat_scores = []
        final_dog_scores = []
        for tweet in user_tweets:
            tweet = tweet['text']
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

        if dog_sa_score > cat_sa_score:
            print(user, " is a dog person. (Dog: ", dog_sa_score, ", Cat: ", cat_sa_score, ")")
            dog_list.append(user)
        elif cat_sa_score > dog_sa_score:
            print(user, " is a cat person. (Dog: ", dog_sa_score, ", Cat: ", cat_sa_score, ")")
            cat_list.append(user)
        else:
            print(user, " could not be classified. (Dog: ", dog_sa_score, ", Cat: ", cat_sa_score, ")")
        max_users = max_users-1

    ################## TAKE AVERAGE SCORES FOR ALL DOG PEOPLE #################

    for user in dog_list:
        newTweets = []
        print('Fetching tweets of dog user: ', user)
        tweets = harvest_user_timeline(twitter_api, screen_name=user, max_results=200)
        for i in tweets:
            newTweets.append(reduce_status(i))
        tweets= {'contentItems': newTweets}

        with open('./profile.json', 'w') as fp:
            json.dump(tweets, fp, indent=2)

        with open(join(dirname(__file__), './profile.json')) as profile_json:
            profile = personality_insights.profile(
                profile_json.read(),
                'application/json',
                content_type='application/json',
                consumption_preferences=True,
                raw_scores=True
            ).get_result()

        research_dog['movie_romance'] += profile['consumption_preferences'][4]['consumption_preferences'][0]['score']
        research_dog['movie_adventure'] += profile['consumption_preferences'][4]['consumption_preferences'][1]['score']
        research_dog['movie_horror'] += profile['consumption_preferences'][4]['consumption_preferences'][2]['score']
        research_dog['movie_musical'] += profile['consumption_preferences'][4]['consumption_preferences'][3]['score']
        research_dog['movie_historical'] += profile['consumption_preferences'][4]['consumption_preferences'][4]['score']
        research_dog['movie_scifi'] += profile['consumption_preferences'][4]['consumption_preferences'][5]['score']
        research_dog['movie_war'] += profile['consumption_preferences'][4]['consumption_preferences'][6]['score']
        research_dog['movie_drama'] += profile['consumption_preferences'][4]['consumption_preferences'][7]['score']
        research_dog['movie_action'] += profile['consumption_preferences'][4]['consumption_preferences'][8]['score']
        research_dog['movie_document'] += profile['consumption_preferences'][4]['consumption_preferences'][9]['score']


    ################## TAKE AVERAGE SCORES FOR ALL CAT PEOPLE #################

    for user in cat_list:
        newTweets = []
        print('Fetching tweets of cat user: ', user)
        tweets = harvest_user_timeline(twitter_api, screen_name=user, max_results=200)
        for i in tweets:
            newTweets.append(reduce_status(i))
        tweets= {'contentItems': newTweets}

        with open('./profile.json', 'w') as fp:
            json.dump(tweets, fp, indent=2)

        with open(join(dirname(__file__), './profile.json')) as profile_json:
            profile = personality_insights.profile(
                profile_json.read(),
                'application/json',
                content_type='application/json',
                consumption_preferences=True,
                raw_scores=True
            ).get_result()

        research_cat['movie_romance'] += profile['consumption_preferences'][4]['consumption_preferences'][0]['score']
        research_cat['movie_adventure'] += profile['consumption_preferences'][4]['consumption_preferences'][1]['score']
        research_cat['movie_horror'] += profile['consumption_preferences'][4]['consumption_preferences'][2]['score']
        research_cat['movie_musical'] += profile['consumption_preferences'][4]['consumption_preferences'][3]['score']
        research_cat['movie_historical'] += profile['consumption_preferences'][4]['consumption_preferences'][4]['score']
        research_cat['movie_scifi'] += profile['consumption_preferences'][4]['consumption_preferences'][5]['score']
        research_cat['movie_war'] += profile['consumption_preferences'][4]['consumption_preferences'][6]['score']
        research_cat['movie_drama'] += profile['consumption_preferences'][4]['consumption_preferences'][7]['score']
        research_cat['movie_action'] += profile['consumption_preferences'][4]['consumption_preferences'][8]['score']
        research_cat['movie_document'] += profile['consumption_preferences'][4]['consumption_preferences'][9]['score']

    ############# PRINT AVERAGES FOR BOTH DOG AND CAT PEOPLE ##################

    for r in research_dog:
        research_dog[r] = research_dog[r]/len(dog_list)
    for r in research_cat:
        research_cat[r] = research_cat[r]/len(cat_list)
    print('\nAverages found for dog users:')
    for r in research_dog:
        print(r, ': ', research_dog[r])
    print('\nAverages found for cat users:')
    for r in research_cat:
        print(r, ': ', research_cat[r])
    os.remove('./profile.json')
