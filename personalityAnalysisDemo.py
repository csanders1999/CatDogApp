from ibm_watson import PersonalityInsightsV3
from os.path import join, dirname
import json
import time
import twitter
import sys

# api keys for IBM's PersonalityInsightsV3
def ibm_login():
    return PersonalityInsightsV3(
        version='2017-10-13',
        iam_apikey='-ACg3nD4EcO5CZ99ttHjKIrs-DBI6NZycDcc5xYaUAFY',
        url='https://gateway.watsonplatform.net/personality-insights/api'
    )

# this function utilizes our keys to return a twitter_api item user later in all twitter system calls
def oauth_login():

    CONSUMER_KEY = 'mCnEXeDRkMrIcWVuaVINLoTqW'
    CONSUMER_SECRET = 'BrK8OlrVBQlCJ1UJcfBQ6hyCcwpIi5QFLjyT1941Jymu32ass9'
    OAUTH_TOKEN = '428623376-v54l4C89jqSz7V4p5Grf8cwxtA0RH6Sqw1qIvz9T'
    OAUTH_TOKEN_SECRET = 'UsfHEy3bVXbueTduNn3sE9KfYxWDy94PXKShJcB3dcV80'

    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)

    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api

def get_user_profile(twitter_api, screen_names=None, user_ids=None):

    # Must have either screen_name or user_id (logical xor)
    assert (screen_names != None) != (user_ids != None),     "Must have screen_names or user_ids, but not both"

    items_to_info = {}

    items = screen_names or user_ids

    while len(items) > 0:

        # Process 100 items at a time per the API specifications for /users/lookup.
        # See http://bit.ly/2Gcjfzr for details.

        items_str = ','.join([str(item) for item in items[:100]])
        items = items[100:]

        if screen_names:
            response = make_twitter_request(twitter_api.users.lookup,
                                            screen_name=items_str)
        else: # user_ids
            response = make_twitter_request(twitter_api.users.lookup,
                                            user_id=items_str)

        for user_info in response:
            if screen_names:
                items_to_info[user_info['screen_name']] = user_info
            else: # user_ids
                items_to_info[user_info['id']] = user_info

    return items_to_info

def harvest_user_timeline(twitter_api, screen_name=None, user_id=None, max_results=1000):

    assert (screen_name != None) != (user_id != None),     "Must have screen_name or user_id, but not both"

    kw = {  # Keyword args for the Twitter API call
        'count': 200,
        'trim_user': 'true',
        'include_rts' : 'true',
        'since_id' : 1
        }

    if screen_name:
        kw['screen_name'] = screen_name
    else:
        kw['user_id'] = user_id

    max_pages = 16
    results = []

    tweets = make_twitter_request(twitter_api.statuses.user_timeline, **kw)

    if tweets is None: # 401 (Not Authorized) - Need to bail out on loop entry
        tweets = []

    results += tweets

    print('Fetched {0} tweets'.format(len(tweets)), file=sys.stderr)

    page_num = 1

    # Many Twitter accounts have fewer than 200 tweets so you don't want to enter
    # the loop and waste a precious request if max_results = 200.

    # Note: Analogous optimizations could be applied inside the loop to try and
    # save requests. e.g. Don't make a third request if you have 287 tweets out of
    # a possible 400 tweets after your second request. Twitter does do some
    # post-filtering on censored and deleted tweets out of batches of 'count', though,
    # so you can't strictly check for the number of results being 200. You might get
    # back 198, for example, and still have many more tweets to go. If you have the
    # total number of tweets for an account (by GET /users/lookup/), then you could
    # simply use this value as a guide.

    if max_results == kw['count']:
        page_num = max_pages # Prevent loop entry

    while page_num < max_pages and len(tweets) > 0 and len(results) < max_results:

        # Necessary for traversing the timeline in Twitter's v1.1 API:
        # get the next query's max-id parameter to pass in.
        # See https://dev.twitter.com/docs/working-with-timelines.
        kw['max_id'] = min([ tweet['id'] for tweet in tweets]) - 1

        tweets = make_twitter_request(twitter_api.statuses.user_timeline, **kw)
        results += tweets

        print('Fetched {0} tweets'.format(len(tweets)),file=sys.stderr)

        page_num += 1

    print('Done fetching tweets', file=sys.stderr)

    return results[:max_results]

def make_twitter_request(twitter_api_func, max_errors=10, *args, **kw):

    # A nested helper function that handles common HTTPErrors. Return an updated
    # value for wait_period if the problem is a 500 level error. Block until the
    # rate limit is reset if it's a rate limiting issue (429 error). Returns None
    # for 401 and 404 errors, which requires special handling by the caller.
    def handle_twitter_http_error(e, wait_period=2, sleep_when_rate_limited=True):

        if wait_period > 3600: # Seconds
            print('Too many retries. Quitting.', file=sys.stderr)
            raise e

        # See https://developer.twitter.com/en/docs/basics/response-codes
        # for common codes

        if e.e.code == 401:
            print('Encountered 401 Error (Not Authorized)', file=sys.stderr)
            return None
        elif e.e.code == 404:
            print('Encountered 404 Error (Not Found)', file=sys.stderr)
            return None
        elif e.e.code == 429:
            print('Encountered 429 Error (Rate Limit Exceeded)', file=sys.stderr)
            if sleep_when_rate_limited:
                print("Retrying in 15 minutes...ZzZ...", file=sys.stderr)
                sys.stderr.flush()
                time.sleep(60*15 + 5)
                print('...ZzZ...Awake now and trying again.', file=sys.stderr)
                return 2
            else:
                raise e # Caller must handle the rate limiting issue
        elif e.e.code in (500, 502, 503, 504):
            print('Encountered {0} Error. Retrying in {1} seconds'                  .format(e.e.code, wait_period), file=sys.stderr)
            time.sleep(wait_period)
            wait_period *= 1.5
            return wait_period
        else:
            raise e

    # End of nested helper function

    wait_period = 2
    error_count = 0

    while True:
        try:
            return twitter_api_func(*args, **kw)
        except twitter.api.TwitterHTTPError as e:
            error_count = 0
            wait_period = handle_twitter_http_error(e, wait_period)
            if wait_period is None:
                return
        except URLError as e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 1.5
            print("URLError encountered. Continuing.", file=sys.stderr)
            if error_count > max_errors:
                print("Too many consecutive errors...bailing out.", file=sys.stderr)
                raise
        except BadStatusLine as e:
            error_count += 1
            time.sleep(wait_period)
            wait_period *= 1.5
            print("BadStatusLine encountered. Continuing.", file=sys.stderr)
            if error_count > max_errors:
                print("Too many consecutive errors...bailing out.", file=sys.stderr)
                raise

def convert_status_to_pi_content_item(s):
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

    newTweets = []
    tweets = harvest_user_timeline(twitter_api, screen_name="tysonowens", max_results=200)
    for i in tweets:
        newTweets.append(convert_status_to_pi_content_item(i))
    tweets= {'contentItems': newTweets}

    with open('./profile2.json', 'w') as fp:
        json.dump(tweets, fp, indent=2)

    with open(join(dirname(__file__), './profile2.json')) as profile_json:
        profile = personality_insights.profile(
            profile_json.read(),
            'application/json',
            content_type='application/json',
            consumption_preferences=True,
            raw_scores=True
        ).get_result()
    print(json.dumps(profile, indent=2))
