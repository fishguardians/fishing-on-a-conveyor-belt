#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''generate_csv.py: Module that retrieves the entire data output and parse into csv using mean, median and iqr calculations
    @Author: "Yip Hou Liang"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''
    
import csv
import math
import numpy as np

from collections import Counter

# open the file in the write mode
errorfile = open('errorlogs.txt', 'a', encoding='UTF8')
errwriter = csv.writer(errorfile)


def write_data_output(video_name):
    # combine the results of the weights, lengths and depths data into one csv file
    fish_id = 0
    fish_index = 0
    overall_data = []
    write_data = []
    fish_dict = {}
    try:
        f = open('output/' + video_name + '/images.txt', 'r')
        hypos_array = f.readlines()
        f.close()
        f = open('output/' + video_name + '/dimensions.txt', 'r')
        dimensions_array = f.readlines()
        f.close()
        f = open('output/' + video_name + '/ids.txt', 'r')
        ids_array = f.readlines()
        f.close()
        f = open('output/' + video_name + '/weights.txt', 'r')
        weights_array = f.readlines()
        f.close()
    except:
        print('Error: File not found')
        errwriter.writerow(['Serious', 'Files Not Found', 'Missing Output Data',
                            'Please check /output/' + video_name + ' folder for missing files'])
        return False

    for (index, lines) in enumerate(hypos_array):
        try:
            if index == 0:
                continue
            else:
                line = lines.split(',')
                if line == ['\n']:
                    continue

                fish_index += 1
                if line[1] in fish_dict.keys():
                    fish_dict[line[1]]['hypot'].append(line[3].strip())
                    fish_dict[line[1]]['frame'].append(line[2].strip())
                    fish_dict[line[1]]['index'] = fish_index
                else:
                    fish_dict = {
                        line[1]: {'hypot': [line[3].strip()], 'frame': [line[2].strip()], 'id': [], 'weight': [],
                                  'length': [], 'depth': [],'index': fish_index}}
                    if fish_id != line[1]:
                        fish_id = line[1]
                        overall_data.append(fish_dict)
        except:
            print('Error: Hypothenuse not recorded')
            errwriter.writerow(['Serious', 'Error with Recording Fish Center', 'Missing Output Data',
                                'Please check /output/' + video_name + ' folder for images.txt file'])
            return False

    for (index, lines) in enumerate(ids_array):
        try:
            if index == 0:
                continue
            else:
                line = lines.split(',')
                if line == ['\n']:
                    continue

                for items in overall_data:
                    if line[1] in items.keys():
                        items[line[1]]['id'].append(line[3].strip())
                    else:
                        continue
        except:
            print('Error: Ids not recorded')
            errwriter.writerow(['Serious', 'Error with Recording ID Tags', 'Missing Output Data',
                                'Please check /output/' + video_name + ' folder for ids.txt file'])
            return False
    
    for (index, lines) in enumerate(weights_array):
        try:
            if index == 0:
                continue
            else:
                line = lines.split(',')
                if line == ['\n']:
                    continue

                for items in overall_data:
                    if line[1] in items.keys():
                        if line[3].strip():
                            items[line[1]]['weight'].append(line[3].strip())
                    else:
                        continue
        except:
            print('Error: Weights not recorded')
            errwriter.writerow(['Serious', 'Error with Recording Weights', 'Missing Output Data',
                                'Please check /output/' + video_name + ' folder for weights.txt file'])
            return False
    
    for (index, lines) in enumerate(dimensions_array):
        try:
            if index == 0:
                continue
            else:
                line = lines.split(',')
                if line == ['\n']:
                    continue

                for items in overall_data:
                    if line[1] in items.keys():
                        items[line[1]]['length'].append(line[3].strip())
                        items[line[1]]['depth'].append(line[4].strip())
                    else:
                        continue
        except:
            print('Error: Weights not recorded')
            errwriter.writerow(['Serious', 'Error with Recording Weights', 'Missing Output Data',
                                'Please check /output/' + video_name + ' folder for dimensions.txt file'])
            return False
    
    
    for items in overall_data:
        fish = 0
        frame = 0
        hypot = 0
        idtag = ""
        weight = 0.0
        length = ""
        depth = ""
        indexofhypot = 0

        for key, value in items.items():
            fish = key
            for k, objects in value.items():
                if k == 'hypot':
                    hypot = min(objects)
                    indexofhypot = objects.index(hypot)
                if k == 'frame':
                    frame = objects[indexofhypot]
                if k == 'id':
                    objects = list(filter(None, objects))
                    if objects:
                        # sorting on basis of frequency of elements, mode
                        result = [item for items, c in Counter(objects).most_common() for item in [items] * c]
                        idtag = result[0]
                if k == 'weight':
                    # get median of occurrences
                    objects = list(map(lambda x: x.replace('N.A', '0.0'), objects))
                    results = sorted(objects, key=lambda x: float(x))
                    weight = results[math.floor(len(results) / 2)]
                if k == 'length':
                    # get median of occurrences
                    results = sorted(objects, key=lambda x: float(x))
                    length = results[math.floor(len(results) / 2)]
                if k == 'depth':
                    # get median of occurrences
                    results = sorted(objects, key=lambda x: float(x))
                    depth = results[math.floor(len(results) / 2)]
        print([fish, idtag, weight, length, depth])
        # add the calculated value into the data
        write_data.append([fish, idtag, weight, length, depth])
    # add iqr of the results
    write_data = check_iqr_data(write_data)

    print('Generating CSV file for video: ' + video_name)
    with open('results/' + video_name[:-4] + '.csv', 'w') as csvfile:

        writer = csv.writer(csvfile)
        writer.writerow(['fish', 'idtag', 'weight(kg)', 'length(cm)', 'depth(cm)','weight diff(iqr)', 'length diff(iqr)', 'depth diff(iqr)'])
        writer.writerows(write_data)

    return write_data

def check_iqr_data(array):
    # find the iqr of the weights, lengths and depths data from the output folder
    ids = []
    weights = []
    lengths = []
    depths = []
    for fish in array:
        if fish[1] not in ids:
            ids.append(fish[1])
            weights.append(float(fish[2]))
            lengths.append(float(fish[3]))
            depths.append(float(fish[4]))
    
    # get interquartile range (IQR)
    iqr_weight_q1 = np.percentile(weights, 25)
    iqr_weight_q3 = np.percentile(weights, 75)
    iqr_length_q1 = np.percentile(lengths, 25)
    iqr_length_q3 = np.percentile(lengths, 75)
    iqr_depth_q1 = np.percentile(depths, 25)
    iqr_depth_q3 = np.percentile(depths, 75)

    for fish in array:
        weight_iqr_error = " "
        length_iqr_error = " "
        depth_iqr_error = " "
        if float(fish[2]) < iqr_weight_q1:
            weight_iqr_error = str(round(float(fish[2]) - iqr_weight_q1,3))
        if float(fish[2]) > iqr_weight_q3:
            weight_iqr_error =  "+" + str(round(float(fish[2]) - iqr_weight_q3,3))

        if float(fish[3]) < iqr_length_q1:
            length_iqr_error =  str(round(float(fish[3]) - iqr_length_q1,3))
        if float(fish[3]) > iqr_length_q3:
            length_iqr_error =  "+" + str(round(float(fish[3]) - iqr_length_q3,3))
        
        if float(fish[4]) < iqr_depth_q1:
            depth_iqr_error =  str(round(float(fish[4]) - iqr_depth_q1,3))
        if float(fish[4]) > iqr_depth_q3:
            depth_iqr_error =  "+" + str(round(float(fish[4]) - iqr_depth_q3,3))
        fish.append(weight_iqr_error)
        fish.append(length_iqr_error)
        fish.append(depth_iqr_error)
        
    return array