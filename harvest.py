
#To harvest tweets from a user to a list, type: user_tweets = harvest_user_timeline(twitter_api, user_id) or use screen_name
#To harvest tweets from all users for personality analysis to a dictionary,-
#-type: cat_tweets = get_cat_results(twitter_api) for cats and-
#-dog_tweets = get_dog_results(twitter_api) for dogs

#Sample test code:

#from header import *
#from harvest import *

#twitter_api = oauth_login()
#cat_tweets = get_cat_results(twitter_api)
#print(json.dumps(cat_tweets, indent=1))
#user_tweets = harvest_user_timeline(twitter_api, "caitsands")
#print(json.dumps(user_tweets, indent=1))


from header import *
from collections import defaultdict


#Example 21
def harvest_user_timeline(twitter_api, screen_name=None, user_id=None, max_results=1000):

    assert (screen_name != None) != (user_id != None), \
    "Must have screen_name or user_id, but not both"

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

    results = results[:max_results]

    list_of_tweets = []

    for result in results:
        list_of_tweets.append(result["text"])

    return list_of_tweets









def twitter_search(twitter_api, q, max_results=200, **kw):

    # See https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets
    # and https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators
    # for details on advanced search criteria that may be useful for
    # keyword arguments

    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets
    search_results = twitter_api.search.tweets(q=q, count=100, **kw)

    statuses = search_results['statuses']

    # Iterate through batches of results by following the cursor until we
    # reach the desired number of results, keeping in mind that OAuth users
    # can "only" make 180 search queries per 15-minute interval. See
    # https://developer.twitter.com/en/docs/basics/rate-limits
    # for details. A reasonable number of results is ~1000, although
    # that number of results may not exist for all queries.

    # Enforce a reasonable limit
    max_results = min(1000, max_results)

    for _ in range(10): # 10*100 = 1000
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError as e: # No more results when next_results doesn't exist
            break

        # Create a dictionary from next_results, which has the following form:
        # ?max_id=313519052523986943&q=NCAA&include_entities=1
        kwargs = dict([ kv.split('=')
                        for kv in next_results[1:].split("&") ])

        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']

        if len(statuses) > max_results:
            break

    user_to_tweet = {}

    for status in statuses:
        user_to_tweet[status["id_str"]] = status["text"]


    return user_to_tweet

def get_dog_results(twitter_api):
        return twitter_search(twitter_api, " dog ", max_results=10)

def get_cat_results(twitter_api):
        return twitter_search(twitter_api, " cat ", max_results=10)




def get_user_profile_image(twitter_api, screen_name=None, user_id=None):

    # Must have either screen_name or user_id (logical xor)
    assert (screen_name != None) != (user_id != None), \
    "Must have screen_names or user_ids, but not both"

    items_to_info = {}

    item = screen_name or user_id

    if screen_name:
        response = make_twitter_request(twitter_api.users.lookup,
                                        screen_name=item)
    else: # user_id
        response = make_twitter_request(twitter_api.users.lookup,
                                        user_id=item)

    for user_info in response:
        if screen_name:
            items_to_info[user_info['screen_name']] = user_info
        else: # user_id
            items_to_info[user_info['id']] = user_info

    url = items_to_info[list(items_to_info.keys())[0]]["profile_image_url"]

    return url
