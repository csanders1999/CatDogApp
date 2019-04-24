from header import *
visual_recognition = VisualRecognitionV3(myVersion, iam_apikey=myIam_apikey)

myTweet = 'This is Beaux. He would like to box, but only if you go easy on him. Might hit you with a left hook or maybe a swift puppercut. 12/10 https://pbs.twimg.com/media/D4ZMVZSUYAAH6nv.jpg'

dog_images = 0
cat_images = 0

url_search = re.search("(?P<url>https?://[^\s]+)", myTweet) # Looks for image url in tweet

if url_search is not None: # If no image, doesn't do anything
    url = url_search.group("url") # grabs URL
    classes_result = visual_recognition.classify(url=url).get_result() # classifies image

    # Gets json data
    classify_data = json.dumps(classes_result["images"][0]["classifiers"][0]["classes"], indent=2)

    # Going through every dictionary in list of json date
    for dict in json.loads(classify_data):
        for key, value in dict.items():
            if value == 'dog':
                dog_images += 1
                break # won't account for both dog or cat (whichever is bigger)
            if value == 'cat':
                cat_images += 1
                break

print(dog_images)
print(cat_images)
