#input : model, test set
#output : predictions?
import numpy as np
import pandas as pd
import json
import argparse
import os
import statistics
import math
import pickle
from ast import literal_eval

df = pd.DataFrame()
transcripts=[]
position=[]
five_mers = []
last = []

def make_preds(model, json_data) :
    data = [json.loads(line) for line in open(json_data, 'r')]
    for sublist in data:
        transcript_name = list(sublist)  # sublist is a dictionary then list it to get the keys of this dictionary
        transcripts.append(transcript_name[0])  # use a new list to store the name

        sublist_2nd = sublist.values()  # sublist_2nd is a dictionary_values object
        temp = list(sublist_2nd)  # put these dictionary in a list like sublist in test
        second_layer = list(temp[0])  # temp[0] is a dictionary like sublist, listing this dictionary would get the key itself of this dict
        position.append(second_layer[0])  # append this key to position

        sublist_3rd = temp[0].values()
        temp = list(sublist_3rd)
        third_layer = list(temp[0])
        five_mers.append(third_layer[0])

        sublist_4th = temp[0].values()
        temp = list(sublist_4th)
        fourth_layer = list(temp[0])
        last.append(fourth_layer)

    df['Transcript_id'] = transcripts
    df['Position'] = position
    df['5-mers'] = five_mers
    df['Reads'] = last
    data = df
    
    print("End of Data Parsing")
    ##### End of Data Parsing #####

    ##### Start of Feature Engineering #####

    #data['Reads'] = data['Reads'].apply(literal_eval)
    read_lengths = []
    for i in range(len(data)):
        read_lengths.append(len(data['Reads'][i]))
    data['Read Lengths'] = read_lengths

    data = data[data['Read Lengths'] > 1] #Remove rows with reads < 20, since 20 was the minimum in the training set
    data = data.reset_index(drop = True)
    data = data.head(500)

    dwell_left_final = []
    dwell_mid_final = []
    dwell_right_final = []
    mean_left_final = []
    mean_mid_final = []
    mean_right_final = []
    sd_left_final = []
    sd_mid_final = []
    sd_right_final = []

    for i in range(len(data)):
        dwell_left = []
        dwell_mid = []
        dwell_right = []
        mean_left = []
        mean_mid = []
        mean_right = []
        sd_left = []
        sd_mid = []
        sd_right = []
        for read in data['Reads'][i]:
            dwell_left.append(read[0])
            sd_left.append(read[1])
            mean_left.append(read[2])
            
            dwell_mid.append(read[3])
            sd_mid.append(read[4])
            mean_mid.append(read[5])
            
            dwell_right.append(read[6])
            sd_right.append(read[7])
            mean_right.append(read[8])
        
        dwell_left_final.append(dwell_left)
        dwell_mid_final.append(dwell_mid)
        dwell_right_final.append(dwell_right)
        
        sd_left_final.append(sd_left)
        sd_mid_final.append(sd_mid)
        sd_right_final.append(sd_right)
        
        mean_left_final.append(mean_left)
        mean_mid_final.append(mean_mid)
        mean_right_final.append(mean_right)

    data['Signal Dwell Time -1'] = dwell_left_final
    data['Signal Dwell Time 0'] = dwell_mid_final
    data['Signal Dwell Time +1'] = dwell_right_final

    data['Means -1'] = mean_left_final
    data['Means'] = mean_mid_final
    data['Means +1'] = mean_right_final

    data['SD -1'] = sd_left_final
    data['SD 0'] = sd_mid_final
    data['SD +1'] = sd_right_final

    first = []
    second = []
    fifth = []
    for i in range(len(data)):
        five_mer = data['5-mers'][i]
        
        #for D, A = 1, G = 2, U = 3
        
        if five_mer[1] == 'A' : 
            first.append(1)
        elif five_mer[1] == 'G' :
            first.append(2)
        else :
            first.append(3)
        
        #for R, A = 1, G = 2
        
        if five_mer[2] == 'A' :
            second.append(1)
        else :
            second.append(2)
        
        #for H, A = 1, C = 2, T = 3
        
        if five_mer[5] == 'A':
            fifth.append(1)
        elif five_mer[5] == 'C':
            fifth.append(2)
        else :
            fifth.append(3)
    
    data['1-mer'] = first
    data['2-mer'] = second
    data['5-mer'] = fifth

    ## Aggregating the reads
    # Taking Mean
    mean_of_left_means = []
    mean_of_right_means = []
    mean_of_mid_means = []
    mean_of_left_dwell= []
    mean_of_mid_dwell= []
    mean_of_right_dwell= []
    sd_left_final = []
    sd_mid_final = []
    sd_right_final = []

    for i in range(len(data)):
        sd_left = 0
        sd_mid = 0
        sd_right = 0
        read_length = data['Read Lengths'][i]
        for j in range(read_length):
            #sum of squares of each of the 3 positions first
            sd_left += ((data['SD -1'][i][j])**2)
            sd_mid += ((data['SD 0'][i][j])**2)
            sd_right += ((data['SD +1'][i][j])**2)
        #then append the square root/reads to the list
        sd_left_final.append((math.sqrt(sd_left))/read_length)
        sd_mid_final.append((math.sqrt(sd_mid))/read_length) 
        sd_right_final.append((math.sqrt(sd_right))/read_length) 

    for i in range(len(data)):
        mean_of_left_means.append(statistics.mean(data['Means -1'][i]))
        mean_of_mid_means.append(statistics.mean(data['Means'][i]))
        mean_of_right_means.append(statistics.mean(data['Means +1'][i]))
        mean_of_left_dwell.append(statistics.mean(data['Signal Dwell Time -1'][i]))
        mean_of_mid_dwell.append(statistics.mean(data['Signal Dwell Time 0'][i]))
        mean_of_right_dwell.append(statistics.mean(data['Signal Dwell Time +1'][i]))

    data['Mean of -1 Means'] = mean_of_left_means
    data['Mean of 0 Means'] = mean_of_mid_means
    data['Mean of +1 Means'] = mean_of_right_means
    data['Mean of -1 SD'] = sd_left_final
    data['Mean of 0 SD'] = sd_mid_final
    data['Mean of +1 SD'] = sd_right_final
    data['Mean of -1 Dwell'] = mean_of_left_dwell
    data['Mean of 0 Dwell'] = mean_of_mid_dwell
    data['Mean of +1 Dwell'] = mean_of_right_dwell

    # Median
    median_of_left_means = []
    median_of_right_means = []
    median_of_mid_means = []
    median_of_left_dwell= []
    median_of_mid_dwell= []
    median_of_right_dwell= []

    for i in range(len(data)):
        median_of_left_means.append(statistics.median(data['Means -1'][i]))
        median_of_mid_means.append(statistics.median(data['Means'][i]))
        median_of_right_means.append(statistics.median(data['Means +1'][i]))
        median_of_left_dwell.append(statistics.median(data['Signal Dwell Time -1'][i]))
        median_of_mid_dwell.append(statistics.median(data['Signal Dwell Time 0'][i]))
        median_of_right_dwell.append(statistics.median(data['Signal Dwell Time +1'][i]))
    
    data['Median of -1 Means'] = median_of_left_means
    data['Median of 0 Means'] = median_of_mid_means
    data['Median of +1 Means'] = median_of_right_means
    data['Median of -1 Dwell'] = median_of_left_dwell
    data['Median of 0 Dwell'] = median_of_mid_dwell
    data['Median of +1 Dwell'] = median_of_right_dwell

    # Minimum
    min_of_left_means = []
    min_of_right_means = []
    min_of_mid_means = []
    min_of_left_sd = []
    min_of_mid_sd = []
    min_of_right_sd = []
    min_of_left_dwell= []
    min_of_mid_dwell= []
    min_of_right_dwell= []

    for i in range(len(data)):
        min_of_left_means.append(min(data['Means -1'][i]))
        min_of_mid_means.append(min(data['Means'][i]))
        min_of_right_means.append(min(data['Means +1'][i]))
        min_of_left_sd.append(min(data['SD -1'][i]))
        min_of_mid_sd.append(min(data['SD 0'][i]))
        min_of_right_sd.append(min(data['SD +1'][i]))
        min_of_left_dwell.append(min(data['Signal Dwell Time -1'][i]))
        min_of_mid_dwell.append(min(data['Signal Dwell Time 0'][i]))
        min_of_right_dwell.append(min(data['Signal Dwell Time +1'][i]))
    
    data['Min of -1 Means'] = min_of_left_means
    data['Min of 0 Means'] = min_of_mid_means
    data['Min of +1 Means'] = min_of_right_means
    data['Min of -1 SD'] = min_of_left_sd
    data['Min of 0 SD'] = min_of_mid_sd
    data['Min of +1 SD'] = min_of_right_sd
    data['Min of -1 Dwell'] = min_of_left_dwell
    data['Min of 0 Dwell'] = min_of_mid_dwell
    data['Min of +1 Dwell'] = min_of_right_dwell

    # Maximum
    max_of_left_means = []
    max_of_right_means = []
    max_of_mid_means = []
    max_of_left_sd = []
    max_of_mid_sd = []
    max_of_right_sd = []
    max_of_left_dwell= []
    max_of_mid_dwell= []
    max_of_right_dwell= []

    for i in range(len(data)):
        max_of_left_means.append(max(data['Means -1'][i]))
        max_of_mid_means.append(max(data['Means'][i]))
        max_of_right_means.append(max(data['Means +1'][i]))
        max_of_left_sd.append(max(data['SD -1'][i]))
        max_of_mid_sd.append(max(data['SD 0'][i]))
        max_of_right_sd.append(max(data['SD +1'][i]))
        max_of_left_dwell.append(max(data['Signal Dwell Time -1'][i]))
        max_of_mid_dwell.append(max(data['Signal Dwell Time 0'][i]))
        max_of_right_dwell.append(max(data['Signal Dwell Time +1'][i]))
    
    data['Max of -1 Means'] = max_of_left_means
    data['Max of 0 Means'] = max_of_mid_means
    data['Max of +1 Means'] = max_of_right_means
    data['Max of -1 SD'] = max_of_left_sd
    data['Max of 0 SD'] = max_of_mid_sd
    data['Max of +1 SD'] = max_of_right_sd
    data['Max of -1 Dwell'] = max_of_left_dwell
    data['Max of 0 Dwell'] = max_of_mid_dwell
    data['Max of +1 Dwell'] = max_of_right_dwell

    # Variance
    var_of_left_means = []
    var_of_right_means = []
    var_of_mid_means = []
    var_of_left_sd = []
    var_of_mid_sd = []
    var_of_right_sd = []
    var_of_left_dwell= []
    var_of_mid_dwell= []
    var_of_right_dwell= []

    for i in range(len(data)):
        var_of_left_means.append(statistics.variance(data['Means -1'][i]))
        var_of_mid_means.append(statistics.variance(data['Means'][i]))
        var_of_right_means.append(statistics.variance(data['Means +1'][i]))
        var_of_left_sd.append(statistics.variance(data['SD -1'][i]))
        var_of_mid_sd.append(statistics.variance(data['SD 0'][i]))
        var_of_right_sd.append(statistics.variance(data['SD +1'][i]))
        var_of_left_dwell.append(statistics.variance(data['Signal Dwell Time -1'][i]))
        var_of_mid_dwell.append(statistics.variance(data['Signal Dwell Time 0'][i]))
        var_of_right_dwell.append(statistics.variance(data['Signal Dwell Time +1'][i]))
    
    data['Var of -1 Means'] = var_of_left_means
    data['Var of 0 Means'] = var_of_mid_means
    data['Var of +1 Means'] = var_of_right_means
    data['Var of -1 SD'] = var_of_left_sd
    data['Var of 0 SD'] = var_of_mid_sd
    data['Var of +1 SD'] = var_of_right_sd
    data['Var of -1 Dwell'] = var_of_left_dwell
    data['Var of 0 Dwell'] = var_of_mid_dwell
    data['Var of +1 Dwell'] = var_of_right_dwell

    print("End of Feature Engineering")
    #set aside transcript id and position for final csv, then drop all the non feature engineered columns for prediction
    final_transcripts = data['Transcript_id']
    final_positions = data['Position']
    data = data.drop(columns = ['Transcript_id','Position','5-mers','Reads','Means','Signal Dwell Time -1','Signal Dwell Time 0','Signal Dwell Time +1','Means -1','Means +1','SD -1','SD 0','SD +1'])

    loaded_model = pickle.load(open(model, 'rb'))
    test_preds = loaded_model.predict_proba(data)[:, 1]
    
    #combine transcript id, position and scores
    output = pd.DataFrame()
    output['transcript_id'] = final_transcripts
    output['transcript_position'] = final_positions
    output['score'] = test_preds
    output.to_csv('predictions.csv', index = False)


def parse_arguments():
    parser = argparse.ArgumentParser(description='To make predictions on test dataset')
    parser.add_argument('-ipath','--input', type = str, help = 'paths for 1) model 2) test set', nargs = 2)
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

    make_preds(args.input[0], args.input[1])

if __name__ == "__main__":
    main()
