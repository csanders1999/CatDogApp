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

    user_list = ['TysonOwens', 'caitsands']
    dog_list = []
    cat_list = []

    research_dog = {
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

    research_cat = research_dog.copy()

    # Classifying terms. Going to add more.
    cat_names = ["cat", "kitten", "kitty", "meow", "feline", "cats"]
    dog_names = ["dog", "doggy", "pupper", "doggo", \
                 "puppy", "woof", "borker", "yapper", \
                 "hound", "retriever", "husky", "dogs"]

    MAXUSER = 4000

    ############### CLASSIIFY USERS AS CAT OR DOG PERSON #####################
    max_users = MAXUSER
    for user in user_list:
        if max_users <= 0:
            break
        if len(user_list) < MAXUSER:
            print("Fetching more people...   [", len(user_list), "/", MAXUSER, "]")
            friends_ids, followers_ids = get_friends_followers_ids(twitter_api,
                                                                   screen_name=user,
                                                                   friends_limit=50,
                                                                   followers_limit=50)
            followers_ids = get_user_profile(twitter_api, user_ids=list(followers_ids))
            for userID in followers_ids:
                if followers_ids[userID]['screen_name'] not in user_list:
                    user_list.append(followers_ids[userID]['screen_name'])

        print('Attempting to classify ', user)
        user_tweets = harvest_user_timeline(twitter_api, screen_name=user, max_results=400)

        # Lists of sentiment scores per each tweet
        final_cat_scores = []
        final_dog_scores = []
        for tweet in user_tweets:
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
                 blob = TextBlob(tweet)
                 final_cat_scores.append(blob.sentiment.polarity)
                 print(blob.sentiment.polarity)
            elif any(name in tweetSimple for name in dog_names):
                print("Dog: ",tweet)
                blob = TextBlob(tweet)
                final_dog_scores.append(blob.sentiment.polarity)
                print(blob.sentiment.polarity)

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
        tweets = harvest_user_timeline(twitter_api, screen_name=user, max_results=400)
        for i in tweets:
            newTweets.append(reduce_status(i))
        tweets= {'contentItems': newTweets}

        with open('./profile.json', 'w') as fp:
            json.dump(tweets, fp, indent=2)

        try:
            with open(join(dirname(__file__), './profile.json')) as profile_json:
                profile = personality_insights.profile(
                    profile_json.read(),
                    'application/json',
                    content_type='application/json',
                    consumption_preferences=True,
                    raw_scores=True
                ).get_result()

            research_dog['big5_openness'] += profile['personality'][0]['raw_score']
            research_dog['adventurousness'] += profile['personality'][0]['children'][0]['raw_score']
            research_dog['art_interest'] += profile['personality'][0]['children'][1]['raw_score']
            research_dog['emotionality'] += profile['personality'][0]['children'][2]['raw_score']
            research_dog['imagination'] += profile['personality'][0]['children'][3]['raw_score']
            research_dog['intellect'] += profile['personality'][0]['children'][4]['raw_score']
            research_dog['auth_challenge'] += profile['personality'][0]['children'][5]['raw_score']

            research_dog['big5_conscientiousness'] += profile['personality'][1]['raw_score']
            research_dog['achieve_strive'] += profile['personality'][1]['children'][0]['raw_score']
            research_dog['cautiousness'] += profile['personality'][1]['children'][1]['raw_score']
            research_dog['dutifulness'] += profile['personality'][1]['children'][2]['raw_score']
            research_dog['orderliness'] += profile['personality'][1]['children'][3]['raw_score']
            research_dog['self_discip'] += profile['personality'][1]['children'][4]['raw_score']
            research_dog['self_effic'] += profile['personality'][1]['children'][5]['raw_score']

            research_dog['big5_extraversion'] += profile['personality'][2]['raw_score']
            research_dog['act_level'] += profile['personality'][2]['children'][0]['raw_score']
            research_dog['assertiveness'] += profile['personality'][2]['children'][1]['raw_score']
            research_dog['cheerfulness'] += profile['personality'][2]['children'][2]['raw_score']
            research_dog['excite_seek'] += profile['personality'][2]['children'][3]['raw_score']
            research_dog['outgoing'] += profile['personality'][2]['children'][4]['raw_score']
            research_dog['gregariousness'] += profile['personality'][2]['children'][5]['raw_score']

            research_dog['big5_agreeableness'] += profile['personality'][3]['raw_score']
            research_dog['altruism'] += profile['personality'][3]['children'][0]['raw_score']
            research_dog['coop'] += profile['personality'][3]['children'][1]['raw_score']
            research_dog['modesty'] += profile['personality'][3]['children'][2]['raw_score']
            research_dog['uncompromising'] += profile['personality'][3]['children'][3]['raw_score']
            research_dog['sympathy'] += profile['personality'][3]['children'][4]['raw_score']
            research_dog['trust'] += profile['personality'][3]['children'][5]['raw_score']

            research_dog['big5_emotional_range'] += profile['personality'][4]['raw_score']
            research_dog['fiery'] += profile['personality'][4]['children'][0]['raw_score']
            research_dog['worry_prone'] += profile['personality'][4]['children'][0]['raw_score']
            research_dog['melancholy'] += profile['personality'][4]['children'][0]['raw_score']
            research_dog['immoderation'] += profile['personality'][4]['children'][0]['raw_score']
            research_dog['self_consc'] += profile['personality'][4]['children'][0]['raw_score']
            research_dog['stress_prone'] += profile['personality'][4]['children'][0]['raw_score']

            research_dog['clothing_qual'] += profile['consumption_preferences'][0]['consumption_preferences'][2]['score']
            research_dog['clothing_style'] += profile['consumption_preferences'][0]['consumption_preferences'][3]['score']
            research_dog['clothing_comf'] += profile['consumption_preferences'][0]['consumption_preferences'][4]['score']
            research_dog['clothing_brand'] += profile['consumption_preferences'][0]['consumption_preferences'][5]['score']
            research_dog['clothing_ads'] += profile['consumption_preferences'][0]['consumption_preferences'][7]['score']
            research_dog['clothing_socmed'] += profile['consumption_preferences'][0]['consumption_preferences'][8]['score']
            research_dog['clothing_fam'] += profile['consumption_preferences'][0]['consumption_preferences'][9]['score']
            research_dog['clothing_spur'] += profile['consumption_preferences'][0]['consumption_preferences'][10]['score']

            research_dog['health_eat'] += profile['consumption_preferences'][1]['consumption_preferences'][0]['score']
            research_dog['health_gym'] += profile['consumption_preferences'][1]['consumption_preferences'][1]['score']
            research_dog['health_outdoor'] += profile['consumption_preferences'][1]['consumption_preferences'][2]['score']

            research_dog['enviro_care'] += profile['consumption_preferences'][2]['consumption_preferences'][0]['score']

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
        except:
            print("ERROR: ", user, " could not have sentiment analyzed (may be due to language)")

    ################## TAKE AVERAGE SCORES FOR ALL CAT PEOPLE #################

    for user in cat_list:
        newTweets = []
        print('Fetching tweets of cat user: ', user)
        tweets = harvest_user_timeline(twitter_api, screen_name=user, max_results=400)
        for i in tweets:
            newTweets.append(reduce_status(i))
        tweets= {'contentItems': newTweets}

        with open('./profile.json', 'w') as fp:
            json.dump(tweets, fp, indent=2)

        try:
            with open(join(dirname(__file__), './profile.json')) as profile_json:
                profile = personality_insights.profile(
                    profile_json.read(),
                    'application/json',
                    content_type='application/json',
                    consumption_preferences=True,
                    raw_scores=True
                ).get_result()

            research_cat['big5_openness'] += profile['personality'][0]['raw_score']
            research_cat['adventurousness'] += profile['personality'][0]['children'][0]['raw_score']
            research_cat['art_interest'] += profile['personality'][0]['children'][1]['raw_score']
            research_cat['emotionality'] += profile['personality'][0]['children'][2]['raw_score']
            research_cat['imagination'] += profile['personality'][0]['children'][3]['raw_score']
            research_cat['intellect'] += profile['personality'][0]['children'][4]['raw_score']
            research_cat['auth_challenge'] += profile['personality'][0]['children'][5]['raw_score']

            research_cat['big5_conscientiousness'] += profile['personality'][1]['raw_score']
            research_cat['achieve_strive'] += profile['personality'][1]['children'][0]['raw_score']
            research_cat['cautiousness'] += profile['personality'][1]['children'][1]['raw_score']
            research_cat['dutifulness'] += profile['personality'][1]['children'][2]['raw_score']
            research_cat['orderliness'] += profile['personality'][1]['children'][3]['raw_score']
            research_cat['self_discip'] += profile['personality'][1]['children'][4]['raw_score']
            research_cat['self_effic'] += profile['personality'][1]['children'][5]['raw_score']

            research_cat['big5_extraversion'] += profile['personality'][2]['raw_score']
            research_cat['act_level'] += profile['personality'][2]['children'][0]['raw_score']
            research_cat['assertiveness'] += profile['personality'][2]['children'][1]['raw_score']
            research_cat['cheerfulness'] += profile['personality'][2]['children'][2]['raw_score']
            research_cat['excite_seek'] += profile['personality'][2]['children'][3]['raw_score']
            research_cat['outgoing'] += profile['personality'][2]['children'][4]['raw_score']
            research_cat['gregariousness'] += profile['personality'][2]['children'][5]['raw_score']

            research_cat['big5_agreeableness'] += profile['personality'][3]['raw_score']
            research_cat['altruism'] += profile['personality'][3]['children'][0]['raw_score']
            research_cat['coop'] += profile['personality'][3]['children'][1]['raw_score']
            research_cat['modesty'] += profile['personality'][3]['children'][2]['raw_score']
            research_cat['uncompromising'] += profile['personality'][3]['children'][3]['raw_score']
            research_cat['sympathy'] += profile['personality'][3]['children'][4]['raw_score']
            research_cat['trust'] += profile['personality'][3]['children'][5]['raw_score']

            research_cat['big5_emotional_range'] += profile['personality'][4]['raw_score']
            research_cat['fiery'] += profile['personality'][4]['children'][0]['raw_score']
            research_cat['worry_prone'] += profile['personality'][4]['children'][0]['raw_score']
            research_cat['melancholy'] += profile['personality'][4]['children'][0]['raw_score']
            research_cat['immoderation'] += profile['personality'][4]['children'][0]['raw_score']
            research_cat['self_consc'] += profile['personality'][4]['children'][0]['raw_score']
            research_cat['stress_prone'] += profile['personality'][4]['children'][0]['raw_score']

            research_cat['clothing_qual'] += profile['consumption_preferences'][0]['consumption_preferences'][2]['score']
            research_cat['clothing_style'] += profile['consumption_preferences'][0]['consumption_preferences'][3]['score']
            research_cat['clothing_comf'] += profile['consumption_preferences'][0]['consumption_preferences'][4]['score']
            research_cat['clothing_brand'] += profile['consumption_preferences'][0]['consumption_preferences'][5]['score']
            research_cat['clothing_ads'] += profile['consumption_preferences'][0]['consumption_preferences'][7]['score']
            research_cat['clothing_socmed'] += profile['consumption_preferences'][0]['consumption_preferences'][8]['score']
            research_cat['clothing_fam'] += profile['consumption_preferences'][0]['consumption_preferences'][9]['score']
            research_cat['clothing_spur'] += profile['consumption_preferences'][0]['consumption_preferences'][10]['score']

            research_cat['health_eat'] += profile['consumption_preferences'][1]['consumption_preferences'][0]['score']
            research_cat['health_gym'] += profile['consumption_preferences'][1]['consumption_preferences'][1]['score']
            research_cat['health_outdoor'] += profile['consumption_preferences'][1]['consumption_preferences'][2]['score']

            research_cat['enviro_care'] += profile['consumption_preferences'][2]['consumption_preferences'][0]['score']

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
        except:
            print("ERROR: ", user, " could not have sentiment analyzed (may be due to language)")

    ############# PRINT AVERAGES FOR BOTH DOG AND CAT PEOPLE ##################
    try:
        for r in research_dog:
            research_dog[r] = research_dog[r]/len(dog_list)
        for r in research_cat:
            research_cat[r] = research_cat[r]/len(cat_list)
    except:
        print('Either dog or cat list is empty')

    # create csv file with all data
    with open('./research/research_data.csv', mode='w') as employee_file:
        data_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(['Attribute', 'Dog', 'Cat'])
        for r in research_dog:
            data_writer.writerow([r, research_dog[r], research_cat[r]])

    # create a graph for big5
    plt.rcParams.update({'font.size': 8})
    N = 5
    dogAvgs = (research_dog['big5_openness'],research_dog['big5_extraversion'],research_dog['big5_agreeableness'],research_dog['big5_emotional_range'],research_dog['big5_conscientiousness'])
    catAvgs = (research_cat['big5_openness'],research_cat['big5_extraversion'],research_cat['big5_agreeableness'],research_cat['big5_emotional_range'],research_cat['big5_conscientiousness'])
    ind = np.arange(N)
    width = 0.20
    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects1 = ax.bar(ind, dogAvgs, width, color='royalblue')
    rects2 = ax.bar(ind+width, catAvgs, width, color='y')
    ax.set_title('Big5 on Cats vs Dogs')
    ax.set_xticks(ind+width/2)
    ax.set_xticklabels(('Openness', 'Extravesion', 'Agreeableness', 'Emotional\nRange', 'Conscientiousness'))
    ax.legend((rects1[0], rects2[0]), ('Dog', 'Cat'))
    ax.autoscale_view()
    plt.savefig('./research/big5_graph.png')

    # create a graph for big5_openness
    N = 6
    dogAvgs = (research_dog['adventurousness'],research_dog['art_interest'],research_dog['emotionality'],research_dog['imagination'],research_dog['intellect'],research_dog['auth_challenge'])
    catAvgs = (research_cat['adventurousness'],research_cat['art_interest'],research_cat['emotionality'],research_cat['imagination'],research_cat['intellect'],research_cat['auth_challenge'])
    ind = np.arange(N)
    width = 0.20
    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects1 = ax.bar(ind, dogAvgs, width, color='royalblue')
    rects2 = ax.bar(ind+width, catAvgs, width, color='y')
    ax.set_title('Openness on Cats vs Dogs')
    ax.set_xticks(ind+width/2)
    ax.set_xticklabels(('Adventurousness', 'Artistic\nInterest', 'Emotionality', 'imagination', 'Intellect','Authority \nChallenging'))
    ax.legend((rects1[0], rects2[0]), ('Dog', 'Cat'))
    ax.autoscale_view()
    plt.savefig('./research/big5_openness_graph.png')

    # create a graph for big5_conscientiousness
    N = 6
    dogAvgs = (research_dog['achieve_strive'],research_dog['cautiousness'],research_dog['dutifulness'],research_dog['orderliness'],research_dog['self_discip'],research_dog['self_effic'])
    catAvgs = (research_cat['achieve_strive'],research_cat['cautiousness'],research_cat['dutifulness'],research_cat['orderliness'],research_cat['self_discip'],research_cat['self_effic'])
    ind = np.arange(N)
    width = 0.20
    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects1 = ax.bar(ind, dogAvgs, width, color='royalblue')
    rects2 = ax.bar(ind+width, catAvgs, width, color='y')
    ax.set_title('Conscientiousness on Cats vs Dogs')
    ax.set_xticks(ind+width/2)
    ax.set_xticklabels(('Achievement\nStriving', 'Cautiousness', 'Dutifulness', 'Orderliness', 'Self-\nDiscipline','Self-\nEfficacy'))
    ax.legend((rects1[0], rects2[0]), ('Dog', 'Cat'))
    ax.autoscale_view()
    plt.savefig('./research/big5_conscientiousness_graph.png')

    # create a graph for big5_extraversion
    N = 6
    dogAvgs = (research_dog['act_level'],research_dog['assertiveness'],research_dog['cheerfulness'],research_dog['excite_seek'],research_dog['outgoing'],research_dog['gregariousness'])
    catAvgs = (research_cat['act_level'],research_cat['assertiveness'],research_cat['cheerfulness'],research_cat['excite_seek'],research_cat['outgoing'],research_cat['gregariousness'])
    ind = np.arange(N)
    width = 0.20
    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects1 = ax.bar(ind, dogAvgs, width, color='royalblue')
    rects2 = ax.bar(ind+width, catAvgs, width, color='y')
    ax.set_title('Extravesion on Cats vs Dogs')
    ax.set_xticks(ind+width/2)
    ax.set_xticklabels(('Activity\nLevel', 'Assertiveness', 'Cheerfulness', 'Excitement\nSeeking', 'Outgoing','Gregariousness'))
    ax.legend((rects1[0], rects2[0]), ('Dog', 'Cat'))
    ax.autoscale_view()
    plt.savefig('./research/big5_extraversion_graph.png')

    # create a graph for big5_agreeableness
    N = 6
    dogAvgs = (research_dog['altruism'],research_dog['coop'],research_dog['modesty'],research_dog['uncompromising'],research_dog['sympathy'],research_dog['trust'])
    catAvgs = (research_cat['altruism'],research_cat['coop'],research_cat['modesty'],research_cat['uncompromising'],research_cat['sympathy'],research_cat['trust'])
    ind = np.arange(N)
    width = 0.20
    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects1 = ax.bar(ind, dogAvgs, width, color='royalblue')
    rects2 = ax.bar(ind+width, catAvgs, width, color='y')
    ax.set_title('Agreeableness on Cats vs Dogs')
    ax.set_xticks(ind+width/2)
    ax.set_xticklabels(('Altruism', 'Co-operation', 'Modesty', 'Uncompromising', 'Sympathy','Trust'))
    ax.legend((rects1[0], rects2[0]), ('Dog', 'Cat'))
    ax.autoscale_view()
    plt.savefig('./research/big5_agreeableness_graph.png')

    # create a graph for big5_emotional_range
    N = 6
    dogAvgs = (research_dog['fiery'],research_dog['worry_prone'],research_dog['melancholy'],research_dog['immoderation'],research_dog['self_consc'],research_dog['stress_prone'])
    catAvgs = (research_cat['fiery'],research_cat['worry_prone'],research_cat['melancholy'],research_cat['immoderation'],research_cat['self_consc'],research_cat['stress_prone'])
    ind = np.arange(N)
    width = 0.20
    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects1 = ax.bar(ind, dogAvgs, width, color='royalblue')
    rects2 = ax.bar(ind+width, catAvgs, width, color='y')
    ax.set_title('Emotional Range on Cats vs Dogs')
    ax.set_xticks(ind+width/2)
    ax.set_xticklabels(('Fiery', 'Worry\nProne', 'Melancholy', 'Immoderation', 'Self-\nConsciousness','Stress\nProne'))
    ax.legend((rects1[0], rects2[0]), ('Dog', 'Cat'))
    ax.autoscale_view()
    plt.savefig('./research/big5_emotional_range_graph.png')

    # create a graph for health
    N = 3
    dogAvgs = (research_dog['health_eat'],research_dog['health_gym'],research_dog['health_outdoor'])
    catAvgs = (research_cat['health_eat'],research_cat['health_gym'],research_cat['health_outdoor'])
    ind = np.arange(N)
    width = 0.20
    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects1 = ax.bar(ind, dogAvgs, width, color='royalblue')
    rects2 = ax.bar(ind+width, catAvgs, width, color='y')
    ax.set_title('Health on Cats vs Dogs')
    ax.set_xticks(ind+width/2)
    ax.set_xticklabels(('Eat Out', 'Gym\nMember', 'Like Outdoor\nActivities'))
    ax.legend((rects1[0], rects2[0]), ('Dog', 'Cat'))
    ax.autoscale_view()
    plt.savefig('./research/big5_health_graph.png')

    # create a graph for big5_shopping
    plt.rcParams.update({'font.size': 6})
    N = 8
    dogAvgs = (research_dog['clothing_ads'],research_dog['clothing_fam'],research_dog['clothing_comf'],research_dog['clothing_qual'],research_dog['clothing_spur'],research_dog['clothing_brand'],research_dog['clothing_style'],research_dog['clothing_socmed'])
    catAvgs = (research_cat['clothing_ads'],research_cat['clothing_fam'],research_cat['clothing_comf'],research_cat['clothing_qual'],research_cat['clothing_spur'],research_cat['clothing_brand'],research_dog['clothing_style'],research_dog['clothing_socmed'])
    ind = np.arange(N)
    width = 0.20
    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects1 = ax.bar(ind, dogAvgs, width, color='royalblue')
    rects2 = ax.bar(ind+width, catAvgs, width, color='y')
    ax.set_title('Shopping on Cats vs Dogs')
    ax.set_xticks(ind+width/2)
    ax.set_xticklabels(('Influenced\nby Online Ads', 'Influenced\nby Family', 'Prefer Comfy\nClothing', 'Prefer Qual.\nClothing', 'Likely to\nSpur Shop','Influenced\nby Brand','Prefer Stylish\nClothing','Influenced\nby Soc. Med.'))
    ax.legend((rects1[0], rects2[0]), ('Dog', 'Cat'))
    ax.autoscale_view()
    plt.savefig('./research/big5_shopping_graph.png')

    # print averages for both dogs and cats
    print('\nAverages found for dog users:')
    for r in research_dog:
        print(r, ': ', research_dog[r])
    print('\nAverages found for cat users:')
    for r in research_cat:
        print(r, ': ', research_cat[r])
    os.remove('./profile.json')
