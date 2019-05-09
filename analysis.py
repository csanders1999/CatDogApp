# Based on:
# https://www.sohamkamani.com/blog/2015/08/21/python-nodejs-comm/

import sys, json
from user_SA import *

#Read data from stdin
def read_in():
    lines = sys.stdin.readlines()
    # Since our input would only be having one line, parse our JSON data from that
    return json.loads(lines[0])

def main():
    # get data from read_in()
    lines = json.loads(sys.argv[1])

    # Perform the user_analysis function on the provided username
    cat_info, dog_info, personality = user_analysis(lines['username'])

    # Open and read aggregate data for dog/cat people
    with open('./research/research_data.csv', mode='r') as infile:
        reader = csv.reader(infile)
        cat_dog_personality = { rows[0]: (rows[1], rows[2]) for rows in reader }

    # Assign data from aggregate csv and user_analysis() function to an object
    # that will be sent to the front end
    lines['cat_sa_score'] = cat_info[0]
    lines['cat_num'] = cat_info[1]
    lines['cat_img_num'] = cat_info[2]
    lines['dog_sa_score'] = dog_info[0]
    lines['dog_num'] = dog_info[1]
    lines['dog_img_num'] = dog_info[2]
    lines['personality'] = personality
    lines['cat_dog_personality'] = cat_dog_personality

    # Return the data object to the output stream
    print(''.join(['***', json.dumps(lines), '***']))

# Start process
if __name__ == '__main__':
    main()