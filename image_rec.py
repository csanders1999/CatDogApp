from header import *
visual_recognition = VisualRecognitionV3(myVersion, iam_apikey=myIam_apikey)

myTweet = 'This is Beaux. He would like to box, but only if you go easy on him. Might hit you with a left hook or maybe a swift puppercut. 12/10 https://www.google.com https://pbs.twimg.com/media/D4ZMVZSUYAAH6nv.jpg https://images.pexels.com/photos/20787/pexels-photo.jpg?cs=srgb&dl=adorable-animal-cat-20787.jpg&fm=jpg'

dog_images = 0
cat_images = 0

# url_search = re.search("(?P<url>https?://[^\s]+)", myTweet) # Looks for image url in tweet
for url in re.findall("(?P<url>https?://[^\s]+)", myTweet):
    # print(url)
    # url = url.group("url") # grabs URL
    print("Found URL, attempting to classify possible image...")
    try:
        classes_result = visual_recognition.classify(url=url).get_result() # classifies image

        # Gets json data
        classify_data = json.dumps(classes_result["images"][0]["classifiers"][0]["classes"], indent=2)

        # Going through every dictionary in list of json date
        for dict in json.loads(classify_data):
            for key, value in dict.items():
                if value == 'dog':
                    dog_images += 1
                    print("URL was a DOG image")
                    break # won't account for both dog or cat (whichever is bigger)
                if value == 'cat':
                    cat_images += 1
                    print("URL was a CAT image")
                    break # won't account for both dog or cat (whichever is bigger)
    except:
        print("Not a valid image URL")


print(dog_images)
print(cat_images)
