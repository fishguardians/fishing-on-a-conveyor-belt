import csv
import os
import math

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
                    # sorting on basis of frequency of elements
                    result = [item for items, c in Counter(objects).most_common() for item in [items] * c]
                    idtag = result[0]
                if k == 'weight':
                    # get center of occurrences
                    if 'N.A' in objects:
                        objects.remove('N.A')
                    results = sorted(objects, key=lambda x: float(x))
                    weight = results[math.floor(len(results) / 2)]
                if k == 'length':
                    # get center of occurrences
                    if '0.0' in objects:
                        objects.remove('0.0')
                    results = sorted(objects, key=lambda x: float(x))
                    length = results[math.floor(len(results) / 2)]
                if k == 'breadth':
                    # get center of occurrences
                    if '0.0' in objects:
                        objects.remove('0.0')
                    results = sorted(objects, key=lambda x: float(x))
                    breadth = results[math.floor(len(results) / 2)]

        write_data.append([fish, frame, hypot, idtag, weight, length, breadth])

    print('Generating CSV file for video: ' + video_name)
    with open('output/' + video_name + '/fish_data.csv', 'w') as csvfile:

        writer = csv.writer(csvfile)
        writer.writerow(['fish', 'frame', 'hypotenuse', 'idtag', 'weight(kg)', 'length(cm)', 'breadth(cm)'])
        writer.writerows(write_data)

    return write_data

    # try:
    #     for (index, fish) in enumerate(fishes_data):
    #         for (fish_id, fish_data) in fish.items():
    #             minframe = min(fish[fish_id]['frame'])
    #             maxframe = max(fish[fish_id]['frame'])
    #             minhypot = min(fish[fish_id]['hypot'])
    #             indexofhypot = fish[fish_id]['hypot'].index(minhypot)

    #             for (indexid, idtag) in enumerate(idcontent):
    #                 if indexid == 0:
    #                     continue
    #                 idline = idtag.split(',')
    #                 if idline[2] >= minframe and idline[2] <= maxframe:
    #                     fish_data['id'].append(idline[3].strip())
    #                     break

    #             for (weightid, weight) in enumerate(weightcontent):
    #                 if weightid == 0:
    #                     continue
    #                 weightline = weight.split(',')
    #                 if weightline[2] >= minframe and weightline[2] <= maxframe:
    #                     fish_data['weight'].append(weightline[3].strip())
    #                     break

    #             for (dimensionid, dimension) in enumerate(dimensioncontent):
    #                 if dimensionid == 0:
    #                     continue
    #                 dimensionline = dimension.split(',')
    #                 if dimensionline[2] >= minframe and dimensionline[2] <= maxframe:
    #                     fish_data['length'].append(dimensionline[3].strip())
    #                     fish_data['breadth'].append(dimensionline[4].strip())
    #                     break

    #             print(fishes_data)

    #             with open('./output/'+video_name+'/fish_data.csv', 'a') as csvfile:
    #                 writer = csv.writer(csvfile)
    #                 for (index, id) in enumerate(fish_data['id']):
    #                     writer.writerow([fish_id, fish_data['frame'][index], fish_data['hypot'][index], id, fish_data['weight'][index], fish_data['length'][index], fish_data['breadth'][index]])
    # except:
    #     errwriter.writerow(['Serious', 'No or Corrupted Data' , 'Cannot Generate Final CSV', 'Please see if /output/' + video_name + ' has more than 1 row of data'])
    #     return False
