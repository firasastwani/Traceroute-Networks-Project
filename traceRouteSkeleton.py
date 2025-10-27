import re #if you want to use regular expression to parse the data
import sys

def main(dump_filename):
    with open(dump_filename, 'r') as infile:
        for line in infile:
            #parse the file line by line and
            #collect necessary information

            if 'proto TCP' in line: 
                tokens = line.split(' ')
                try:
                    id = tokens.index('id')
                    print('time stamp: ', tokens[0])
                    print('id:', tokens[id + 1])
                except: 
                    continue


    #calcuate elapsed time and output the result
    #with open('output.txt', 'w') as outfile:
        #output TTL, router IP address, and 3 elapsed times in msec for each TTL
        


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
    else:
        filename = 'sampletcpdump.txt'

    main(filename)
