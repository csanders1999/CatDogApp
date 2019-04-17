# Based on:
# https://www.sohamkamani.com/blog/2015/08/21/python-nodejs-comm/

import sys, json

#Read data from stdin
def read_in():
    lines = sys.stdin.readlines()
    #Since our input would only be having one line, parse our JSON data from that
    return json.loads(lines[0])

def main():
    #get our data as an array from read_in()
    lines = json.loads(sys.argv[1])
    lines['py'] = True

    #return the name to the output stream
    print(json.dumps(lines))

#start process
if __name__ == '__main__':
    main()