import json
import re

from watson_developer_cloud import VisualRecognitionV3

visual_recognition = VisualRecognitionV3('2018-03-19', iam_apikey='MmKAR85BG57mM7tR5pw5T2g_U0z3t0uZLNECjnKACjN-')

myString = 'This is Beaux. He would like to box, but only if you go easy on him. Might hit you with a left hook or maybe a swift puppercut. 12/10 https://pbs.twimg.com/media/D4ZMVZSUYAAH6nv.jpg'
dog_images = 0
cat_images = 0
url_search = re.search("(?P<url>https?://[^\s]+)", myString)
if url_search is not None:
    url = url_search.group("url")
    classes_result = visual_recognition.classify(url=url).get_result()
    data = json.dumps(classes_result["images"][0]["classifiers"][0]["classes"], indent=2)
    list = json.loads(data)
    for dict in list:
        for key, value in dict.items():
            if value == 'dog':
                dog_images += 1
                break # won't account for both dog or cat (whichever is bigger)
            if value == 'cat':
                cat_images += 1
                break
print(dog_images)
print(cat_images)
