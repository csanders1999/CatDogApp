from textblob import TextBlob
from header import *
from harvest import *
from personalityAnalysisDemo import *

twitter_api = oauth_login()
personality_insights = ibm_login()
visual_recognition = VisualRecognitionV3(myVersion2, iam_apikey=myIam_apikey2)

def user_analysis(screen_name):
    user_tweets = harvest_user_timeline(twitter_api, screen_name)

    dog_images = 0
    cat_images = 0

    research_user = {
        'big5_openness' : 0,
        'adventurousness' : 0,
        'art_interest' : 0,
        'emotionality' : 0,
        'imagination' : 0,
        'intellect' : 0,
        'auth_challenge' : 0,

        'big5_conscientiousness' : 0,
        'achieve_strive' : 0,
        'cautiousness' : 0,
        'dutifulness' : 0,
        'orderliness' : 0,
        'self_discip' : 0,
        'self_effic' : 0,

        'big5_extraversion' : 0,
        'act_level' : 0,
        'assertiveness' : 0,
        'cheerfulness' : 0,
        'excite_seek' : 0,
        'outgoing' : 0,
        'gregariousness' : 0,

        'big5_agreeableness' : 0,
        'altruism' : 0,
        'coop' : 0,
        'modesty' : 0,
        'uncompromising' : 0,
        'sympathy' : 0,
        'trust' : 0,

        'big5_emotional_range' : 0,
        'fiery' : 0,
        'worry_prone' : 0,
        'melancholy' : 0,
        'immoderation' : 0,
        'self_consc' : 0,
        'stress_prone' : 0,

        'clothing_qual' : 0,
        'clothing_style' : 0,
        'clothing_comf' : 0,
        'clothing_brand' : 0,
        'clothing_ads' : 0,
        'clothing_socmed' : 0,
        'clothing_fam' : 0,
        'clothing_spur' : 0,

        'health_eat' : 0,
        'health_gym' : 0,
        'health_outdoor' : 0,

        'enviro_care' : 0,

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

    # Classifying terms. Going to add more.
    cat_names = ["cat", "kitten", "kitty", "meow", "feline", "cats"]
    dog_names = ["dog", "doggy", "pupper ", "doggo", \
                 "puppy", "woof", "borker", "yapper", \
                 "hound", "retriever", "husky", "dogs"]

    # Lists of sentiment scores per each tweet
    final_cat_scores = []
    final_dog_scores = []
    num_cat_tweets = 0
    num_dog_tweets = 0

    for tweet in user_tweets:
        #print(tweet)
        tweetOG = tweet
        tweet = tweet['text']
        tweetSimple = tweet.lower()
        PERMITTED_CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ _-"
        tweetSimple = "".join(c for c in tweetSimple if c in PERMITTED_CHARS)
        tweetSimple = tweetSimple.split()
        if any(name in tweetSimple for name in cat_names) and \
           any(name in tweetSimple for name in dog_names):
            # Need to add way to parse sentance if contains both cat
            # and dog classifiers (i.e. "I hate cats but I love dogs")
            # should add a negative sentiment score to final_cat_scores
            # and positive to final_dog_scores
            break
        elif any(name in tweetSimple for name in cat_names):
             print("Cat: ",tweet)
             num_cat_tweets += 1
             blob = TextBlob(tweet)
             final_cat_scores.append(blob.sentiment.polarity)
             print(blob.sentiment.polarity)
        elif any(name in tweetSimple for name in dog_names):
            print("Dog: ",tweet)
            num_dog_tweets += 1
            blob = TextBlob(tweet)
            final_dog_scores.append(blob.sentiment.polarity)
            print(blob.sentiment.polarity)

        try:
            #print(tweetOG)
            mediaList = tweetOG['entities']['media']
            #print(mediaList)
            mediaURLs = []
            for dict in mediaList:
                mediaURLs.append(dict['media_url'])
            for url in mediaURLs:
                # print(url)
                # url = url.group("url") # grabs URL
                print("Found URL, attempting to classify possible image...", url)
                try:
                    classes_result = visual_recognition.classify(url=url).get_result() # classifies image

                    # Gets json data
                    classify_data = json.dumps(classes_result["images"][0]["classifiers"][0]["classes"], indent=2)

                    # Going through every dictionary in list of json date
                    for dict in json.loads(classify_data):
                        for key, value in dict.items():
                            # print(key, " ", value)
                            if value == 'dog':
                                dog_images += 1
                                print("URL was a DOG image")
                                break # won't account for both dog or cat (whichever is bigger)
                            if value == 'cat':
                                cat_images += 1
                                print("URL was a CAT image")
                                break # won't account for both dog or cat (whichever is bigger)
                except Exception as ex:
                    # print("Not a valid image URL")
                    print(ex)
        except:
            pass

    # Sum of sentiment scores for all tweets containing cat or dog classifiers
    cat_sa_score = sum(final_cat_scores)
    dog_sa_score = sum(final_dog_scores)

    # Testing
    # print("Final dog score: ", dog_sa_score)
    # print("Final cat score: ", cat_sa_score)

    newTweets = []
    # tweets = harvest_user_timeline(twitter_api, screen_name=screen_name, max_results=400)
    for i in user_tweets:
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

    research_user['big5_openness'] += profile['personality'][0]['raw_score']
    research_user['adventurousness'] += profile['personality'][0]['children'][0]['raw_score']
    research_user['art_interest'] += profile['personality'][0]['children'][1]['raw_score']
    research_user['emotionality'] += profile['personality'][0]['children'][2]['raw_score']
    research_user['imagination'] += profile['personality'][0]['children'][3]['raw_score']
    research_user['intellect'] += profile['personality'][0]['children'][4]['raw_score']
    research_user['auth_challenge'] += profile['personality'][0]['children'][5]['raw_score']

    research_user['big5_conscientiousness'] += profile['personality'][1]['raw_score']
    research_user['achieve_strive'] += profile['personality'][1]['children'][0]['raw_score']
    research_user['cautiousness'] += profile['personality'][1]['children'][1]['raw_score']
    research_user['dutifulness'] += profile['personality'][1]['children'][2]['raw_score']
    research_user['orderliness'] += profile['personality'][1]['children'][3]['raw_score']
    research_user['self_discip'] += profile['personality'][1]['children'][4]['raw_score']
    research_user['self_effic'] += profile['personality'][1]['children'][5]['raw_score']

    research_user['big5_extraversion'] += profile['personality'][2]['raw_score']
    research_user['act_level'] += profile['personality'][2]['children'][0]['raw_score']
    research_user['assertiveness'] += profile['personality'][2]['children'][1]['raw_score']
    research_user['cheerfulness'] += profile['personality'][2]['children'][2]['raw_score']
    research_user['excite_seek'] += profile['personality'][2]['children'][3]['raw_score']
    research_user['outgoing'] += profile['personality'][2]['children'][4]['raw_score']
    research_user['gregariousness'] += profile['personality'][2]['children'][5]['raw_score']

    research_user['big5_agreeableness'] += profile['personality'][3]['raw_score']
    research_user['altruism'] += profile['personality'][3]['children'][0]['raw_score']
    research_user['coop'] += profile['personality'][3]['children'][1]['raw_score']
    research_user['modesty'] += profile['personality'][3]['children'][2]['raw_score']
    research_user['uncompromising'] += profile['personality'][3]['children'][3]['raw_score']
    research_user['sympathy'] += profile['personality'][3]['children'][4]['raw_score']
    research_user['trust'] += profile['personality'][3]['children'][5]['raw_score']

    research_user['big5_emotional_range'] += profile['personality'][4]['raw_score']
    research_user['fiery'] += profile['personality'][4]['children'][0]['raw_score']
    research_user['worry_prone'] += profile['personality'][4]['children'][0]['raw_score']
    research_user['melancholy'] += profile['personality'][4]['children'][0]['raw_score']
    research_user['immoderation'] += profile['personality'][4]['children'][0]['raw_score']
    research_user['self_consc'] += profile['personality'][4]['children'][0]['raw_score']
    research_user['stress_prone'] += profile['personality'][4]['children'][0]['raw_score']

    research_user['clothing_qual'] += profile['consumption_preferences'][0]['consumption_preferences'][2]['score']
    research_user['clothing_style'] += profile['consumption_preferences'][0]['consumption_preferences'][3]['score']
    research_user['clothing_comf'] += profile['consumption_preferences'][0]['consumption_preferences'][4]['score']
    research_user['clothing_brand'] += profile['consumption_preferences'][0]['consumption_preferences'][5]['score']
    research_user['clothing_ads'] += profile['consumption_preferences'][0]['consumption_preferences'][7]['score']
    research_user['clothing_socmed'] += profile['consumption_preferences'][0]['consumption_preferences'][8]['score']
    research_user['clothing_fam'] += profile['consumption_preferences'][0]['consumption_preferences'][9]['score']
    research_user['clothing_spur'] += profile['consumption_preferences'][0]['consumption_preferences'][10]['score']

    research_user['health_eat'] += profile['consumption_preferences'][1]['consumption_preferences'][0]['score']
    research_user['health_gym'] += profile['consumption_preferences'][1]['consumption_preferences'][1]['score']
    research_user['health_outdoor'] += profile['consumption_preferences'][1]['consumption_preferences'][2]['score']

    research_user['enviro_care'] += profile['consumption_preferences'][2]['consumption_preferences'][0]['score']

    research_user['movie_romance'] += profile['consumption_preferences'][4]['consumption_preferences'][0]['score']
    research_user['movie_adventure'] += profile['consumption_preferences'][4]['consumption_preferences'][1]['score']
    research_user['movie_horror'] += profile['consumption_preferences'][4]['consumption_preferences'][2]['score']
    research_user['movie_musical'] += profile['consumption_preferences'][4]['consumption_preferences'][3]['score']
    research_user['movie_historical'] += profile['consumption_preferences'][4]['consumption_preferences'][4]['score']
    research_user['movie_scifi'] += profile['consumption_preferences'][4]['consumption_preferences'][5]['score']
    research_user['movie_war'] += profile['consumption_preferences'][4]['consumption_preferences'][6]['score']
    research_user['movie_drama'] += profile['consumption_preferences'][4]['consumption_preferences'][7]['score']
    research_user['movie_action'] += profile['consumption_preferences'][4]['consumption_preferences'][8]['score']
    research_user['movie_document'] += profile['consumption_preferences'][4]['consumption_preferences'][9]['score']

    return ((cat_sa_score, num_cat_tweets, cat_images), (dog_sa_score, num_dog_tweets, dog_images), research_user)
