# Based on:
# https://www.sohamkamani.com/blog/2015/08/21/python-nodejs-comm/

import sys, json
from user_SA import *

#Read data from stdin
def read_in():
    lines = sys.stdin.readlines()
    #Since our input would only be having one line, parse our JSON data from that
    return json.loads(lines[0])

def main():
    #get our data as an array from read_in()
    lines = json.loads(sys.argv[1])

    cat_info, dog_info = user_analysis(lines['username'])

    lines['cat_sa_score'] = cat_info[0]
    lines['cat_num'] = cat_info[1]
    lines['dog_sa_score'] = dog_info[0]
    lines['dog_num'] = dog_info[1]

    print(1111)

    #return the name to the output stream
    print(''.join(['***', json.dumps(lines), '***']))

#start process
if __name__ == '__main__':
    main()