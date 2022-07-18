import csv
import os
import math
import numpy as np

from collections import Counter

# open the file in the write mode
errorfile = open('errorlogs.txt', 'a', encoding='UTF8')
errwriter = csv.writer(errorfile)


def write_data_output(video_name):
    fish_id = 0
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

                if line[1] in fish_dict.keys():
                    fish_dict[line[1]]['hypot'].append(line[3].strip())
                    fish_dict[line[1]]['frame'].append(line[2].strip())
                else:
                    fish_dict = {
                        line[1]: {'hypot': [line[3].strip()], 'frame': [line[2].strip()], 'id': [], 'weight': [],
                                  'length': [], 'breadth': []}}
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
                        if len(line[3].strip()) > 6 and len(line[3].strip()) < 10:
                            items[line[1]]['id'].append(line[3].strip())
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
                        items[line[1]]['weight'].append(line[3].strip())
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
                        items[line[1]]['breadth'].append(line[4].strip())
        except:
            print('Error: Weights not recorded')
            errwriter.writerow(['Serious', 'Error with Recording Weights', 'Missing Output Data',
                                'Please check /output/' + video_name + ' folder for dimensions.txt file'])
            return False

    for items in overall_data:
        fish = 0
        frame = 0
        hypot = 0
        idtag = 0
        weight = 0.0
        length = ""
        breadth = ""
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
                    # sorting on basis of frequency of elements, mode
                    result = [item for items, c in Counter(objects).most_common() for item in [items] * c]
                    idtag = result[0]
                if k == 'weight':
                    # get median of occurrences
                    if 'N.A' in objects:
                        objects.remove('N.A')
                    results = sorted(objects, key=lambda x: float(x))
                    weight = results[math.floor(len(results) / 2)]
                if k == 'length':
                    # get median of occurrences
                    if '0.0' in objects:
                        objects.remove('0.0')
                    results = sorted(objects, key=lambda x: float(x))
                    length = results[math.floor(len(results) / 2)]
                if k == 'breadth':
                    # get median of occurrences
                    if '0.0' in objects:
                        objects.remove('0.0')
                    results = sorted(objects, key=lambda x: float(x))
                    breadth = results[math.floor(len(results) / 2)]

        write_data.append([fish, idtag, weight, length, breadth])

    write_data = check_iqr_data(write_data)

    print('Generating CSV file for video: ' + video_name)
    with open('results/' + video_name + '_fish_data.csv', 'w') as csvfile:

        writer = csv.writer(csvfile)
        writer.writerow(['fish', 'idtag', 'weight(kg)', 'length(cm)', 'depth(cm)','iqr error'])
        writer.writerows(write_data)

    return write_data

def check_iqr_data(array):
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

    iqr_error = ""
    for fish in array:
        if float(fish[2]) < iqr_weight_q1:
            iqr_error += fish[2] + " kg < q1: " + str(round(iqr_weight_q1,3)) + "kg. "
        if float(fish[2]) > iqr_weight_q3:
            iqr_error += fish[2] + " kg > q3: " + str(round(iqr_weight_q3,3)) + "kg. "
        if float(fish[3]) < iqr_length_q1:
            iqr_error += fish[3] + " cm < q1: " + str(round(iqr_length_q1,3)) + "cm. "
        if float(fish[3]) > iqr_length_q3:
            iqr_error += fish[3] + " cm > q3: " + str(round(iqr_length_q3,3)) + "cm. "
        if float(fish[4]) < iqr_depth_q1:
            iqr_error += fish[4] + " cm < q1: " + str(round(iqr_depth_q1,3)) + "cm. "
        if float(fish[4]) > iqr_depth_q3:
            iqr_error += fish[4] + " cm > q3: " + str(round(iqr_depth_q3,3)) + "cm. "
        fish.append(iqr_error)
        iqr_error = ""
    return array