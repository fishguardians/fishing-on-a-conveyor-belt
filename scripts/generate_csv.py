#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''camera.py: Video capture module that takes the images of the fish
    @Author: "Muhammad Abdurraheem and Yip Hou Liang"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''
# import if necessary (built-in, third-party, path, own modules)
import csv
import os

# open the file in the write mode
errorfile = open('./errorlogs.txt', 'a', encoding='UTF8')
errwriter = csv.writer(errorfile)

def WriteDataOutput(_video_names):
    index, fish_id = 0, 0
    fishes_data = []
    for video_name in _video_names:
        try:
            print('Generating CSV file for video: ' + video_name)
            with open('./output/'+video_name+'/fish_data.csv', 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['fish_id', 'frame', 'hypotenuse', 'id', 'weight', 'length', 'breadth'])

            hypof = open('./output/'+video_name+'/images.txt','r')
            hypocontent = hypof.readlines()
            hypof.close()
            dimensionf = open('./output/'+video_name+'/dimensions.txt','r')
            dimensioncontent = dimensionf.readlines()
            dimensionf.close()
            idsf = open('./output/'+video_name+'/ids.txt','r')
            idcontent = idsf.readlines()
            idsf.close()
            weightsf = open('./output/'+video_name+'/weights.txt','r')
            weightcontent = weightsf.readlines()
            weightsf.close()
        except:
            print('Error: File not found')
            errwriter.writerow(['Serious', 'Files Not Found' , 'Missing Output Data', 'Please check /output/' + video_name + ' folder for missing files'])
            return
        
        fish_data = []
        for (index, lines) in enumerate(hypocontent):
            if index == 0:
                continue
            line = lines.split(',')

            if line[1] != fish_id:
                if(len(fish_data) > 0):
                    fishes_data.append(fish_data)
                fish_id = line[1]
                fish_data = {fish_id: {'frame':[line[2].strip()],'hypot':[line[3].strip()], 'id': [], 'weight': [], 'length':[], 'breadth':[]}}
            else:
                fish_data[line[1]]['frame'].append(line[2].strip())
                fish_data[line[1]]['hypot'].append(line[3].strip())
        fishes_data.append(fish_data)

        try:
            for (index, fish) in enumerate(fishes_data):
                for (fish_id, fish_data) in fish.items():
                    minframe = min(fish[fish_id]['frame'])
                    maxframe = max(fish[fish_id]['frame'])
                    minhypot = min(fish[fish_id]['hypot'])
                    indexofhypot = fish[fish_id]['hypot'].index(minhypot)

                    for (indexid, idtag) in enumerate(idcontent):
                        if indexid == 0:
                            continue
                        idline = idtag.split(',')
                        if idline[2] >= minframe and idline[2] <= maxframe:
                            fish_data['id'].append(idline[3].strip())
                            break

                    for (weightid, weight) in enumerate(weightcontent):
                        if weightid == 0:
                            continue
                        weightline = weight.split(',')
                        if weightline[2] >= minframe and weightline[2] <= maxframe:
                            fish_data['weight'].append(weightline[3].strip())
                            break

                    for (dimensionid, dimension) in enumerate(dimensioncontent):
                        if dimensionid == 0:
                            continue
                        dimensionline = dimension.split(',')
                        if dimensionline[2] >= minframe and dimensionline[2] <= maxframe:
                            fish_data['length'].append(dimensionline[3].strip())
                            fish_data['breadth'].append(dimensionline[4].strip())
                            break

                    print(fishes_data)
                    
                    with open('./output/'+video_name+'/fish_data.csv', 'a') as csvfile:
                        writer = csv.writer(csvfile)
                        for (index, id) in enumerate(fish_data['id']):
                            writer.writerow([fish_id, fish_data['frame'][index], fish_data['hypot'][index], id, fish_data['weight'][index], fish_data['length'][index], fish_data['breadth'][index]])
        except:
            errwriter.writerow(['Serious', 'No or Corrupted Data' , 'Cannot Generate Final CSV', 'Please see if /output/' + video_name + ' has more than 1 row of data'])