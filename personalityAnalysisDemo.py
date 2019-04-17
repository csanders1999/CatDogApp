from ibm_watson import PersonalityInsightsV3
from os.path import join, dirname
import json
import time
import twitter
import sys
from credentials import *
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
##                         Where the Magic Happens                           ##
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

if __name__ == "__main__":
    twitter_api = oauth_login()
    personality_insights = ibm_login()

    user_list = ['tysonowens','caitsands','Joe_Comeau3',]

    research = {
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

    for user in user_list:
        newTweets = []
        print('Fetching tweets of ', user)
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

        research['movie_romance'] += profile['consumption_preferences'][4]['consumption_preferences'][0]['score']
        research['movie_adventure'] += profile['consumption_preferences'][4]['consumption_preferences'][1]['score']
        research['movie_horror'] += profile['consumption_preferences'][4]['consumption_preferences'][2]['score']
        research['movie_musical'] += profile['consumption_preferences'][4]['consumption_preferences'][3]['score']
        research['movie_historical'] += profile['consumption_preferences'][4]['consumption_preferences'][4]['score']
        research['movie_scifi'] += profile['consumption_preferences'][4]['consumption_preferences'][5]['score']
        research['movie_war'] += profile['consumption_preferences'][4]['consumption_preferences'][6]['score']
        research['movie_drama'] += profile['consumption_preferences'][4]['consumption_preferences'][7]['score']
        research['movie_action'] += profile['consumption_preferences'][4]['consumption_preferences'][8]['score']
        research['movie_document'] += profile['consumption_preferences'][4]['consumption_preferences'][9]['score']

    for r in research:
        research[r] = research[r]/len(user_list)
    print('\nAverages found:')
    for r in research:
        print(r, ': ', research[r])
