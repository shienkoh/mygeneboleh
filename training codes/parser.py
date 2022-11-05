import numpy as np
import pandas as pd
import json
import argparse
import os

df = pd.DataFrame()
transcripts=[]
position=[]
five_mers = []
last = []
middle_means = []


def parse_data(json_data, output):
    #data = [json.loads(line) for line in open('/Users/shien/Downloads/DSA4262/project2/data.json', 'r')]
    data = [json.loads(line) for line in open(json_data, 'r')]
    for sublist in data:
        transcript_name = list(sublist)  # sublist is a dictionary then list it to get the keys of this dictionary
        transcripts.append(transcript_name[0])  # use a new list to store the name

        sublist_2nd = sublist.values()  # sublist_2nd is a dictionary_values object
        temp = list(sublist_2nd)  # put these dictionary in a list like sublist in test
        second_layer = list(temp[
                                0])  # temp[0] is a dictionary like sublist, listing this dictionary would get the key itself of this dict
        position.append(second_layer[0])  # append this key to position

        sublist_3rd = temp[0].values()
        temp = list(sublist_3rd)
        third_layer = list(temp[0])
        five_mers.append(third_layer[0])

        sublist_4th = temp[0].values()
        temp = list(sublist_4th)
        fourth_layer = list(temp[0])
        last.append(fourth_layer)

    df['Transcript'] = transcripts
    df['Position'] = position
    df['5-mers'] = five_mers
    df['Reads'] = last

    head_tail = os.path.split(json_data)
    #test = df.head()
    df.to_csv(output + '/' + head_tail[1][:-5] + '.csv')

    #return df

def parse_arguments():
    parser = argparse.ArgumentParser(description='To parse the raw json dataset')
    #parser.add_argument('-ipath', '--input', type=argparse.FileType('r'), help='JSON input file')
    parser.add_argument('-ipath','--input', type = str, help = 'path to input json file')
    #parser.add_argument('-opath' '--output', type=dir_path, help = '')
    parser.add_argument('-opath','--output', type = str, help = 'path to output parsed data')

    return parser.parse_args()

def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

def main():
    args = parse_arguments()
    #if args.input is not None:
    #    data = [json.loads(args.input) for line in open('/Users/shien/Downloads/DSA4262/project2/data.json', 'r')]

    parse_data(args.input, args.output)

if __name__ == "__main__":
    main()
