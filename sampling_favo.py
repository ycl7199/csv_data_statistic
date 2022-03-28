import csv
from itertools import count
import os
import matplotlib.pyplot as plt
import numpy as np
import json
import random
import shutil
import urllib.request
import time
import socket
import zipfile

def get_count_list(file_path, output_list):
    
    with open(file_path, 'r', encoding= 'utf-8-sig') as data:
        csv_reader = csv.reader(data)
        next(csv_reader)
        for row in csv_reader:
            try:
                favo_count = int(row[-1])
                views_count = int(row[3])
            except:
                continue
            imgurl=row[-5]
            if imgurl=="":
                imgurl=row[-4]
                if imgurl=="":
                    imgurl=row[-3]
                    if imgurl=="":
                        imgurl=row[-2]
            p_id = row[0]
            output_list[favo_count].append([p_id, imgurl, favo_count, views_count])
            

    return output_list

def request_retry(p_url, p_id, folder_name, timeout, zip_file):
    # p_url = data[1]
    # p_id = data[0]
    socket.setdefaulttimeout(timeout) #設定連線愈時時間 
    download_count = 0
    try:
        urllib.request.urlretrieve(p_url,'{}{}.jpg'.format(folder_name +'\\',p_id))
        zip_file.write(os.path.join(folder_name +'\\',p_id))
        print(p_id+"download completed")
        download_count += 1
    except socket.error:
        count = 1
        while count <= 5: 
            socket.setdefaulttimeout(15) #重新計時連線時間
            try:
                print('request timeout, retry the process',p_id)
                urllib.request.urlretrieve(p_url,'{}\\{}.jpg'.format(folder_name,p_id))
                zip_file.write(os.path.join(folder_name +'\\',p_id))
                print(p_id+"download completed")
                download_count += 1
                break
            except socket.error:
                count += 1
            if count > 5:
                print(p_id,'retry failed')
                break
            time.sleep(2)

def get_pic(id_list, source_img_path):
    folder_list = []
    csv_list = []
    for cluster in id_list:
        folder_name = 'cluster_' + str(cluster[0])
        folder_list.append(folder_name)
        csv_file_name = folder_name + '.csv'
        csv_list.append(csv_file_name)
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        with open(csv_file_name, 'w', encoding= 'utf-8-sig', newline= '') as data:
            csv_writer = csv.writer(data)
            csv_writer.writerow(['id', 'views', 'favorites', 'url'])
            for i,p in enumerate(cluster[1]):
                p_id = p[0]
                p_views = p[3]
                p_favo = p[2]
                p_url = p[1]
                img_path = os.path.join(source_img_path, p_id+'.jpg')
                try:
                    target_path = folder_name + '\\' + p_id + '.jpg'
                    shutil.copyfile(img_path, target_path)
                    print(img_path, 'data founded')
                except:
                    try:
                        print(img_path, 'file not founded, try to get picture from flickr server')
                        urllib.request.urlretrieve(p_url,'{}{}.jpg'.format(folder_name +'\\',p[0]))
                        time.sleep(1)
                    except:
                        try:
                            request_retry(p_url, p_id , folder_name = folder_name, timeout = 15)
                        except:
                            print(p_id, 'url not found')
                            pass
                csv_writer.writerow([p_id, p_views, p_favo, p_url])
                # if i >= 10:
                #     break
    return folder_list, csv_list

def sample_by_favo(data_list, favo_range_start, favo_range_end):
    sample_list = []
    # for pic_attri in data_list:
    #     if int(pic_attri[2]) >= favo_range_start and int(pic_attri[2]) <= favo_range_end:
    #         sample_list.append(pic_attri)
    for cluster in data_list[favo_range_start:favo_range_end]:
        for p_data in cluster:
            sample_list.append(p_data)

    
    return sample_list

def pic_extract(id_list, source_img_path, pic_number_per_foler, csv_name):
    csv_name = csv_name
    folder_name = 'extract_by_favorite__1'
    count_temp = 0
    
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    zf = zipfile.ZipFile('{}.zip'.format(folder_name), 'w', zipfile.ZIP_DEFLATED) # create new zip file to store file

    with open(csv_name, 'w', encoding= 'utf-8-sig', newline= '') as data:
        csv_writer = csv.writer(data)
        csv_writer.writerow(['id', 'views', 'favorites', 'url'])
        for i, pic_attri in enumerate(id_list):
            if i - count_temp >= pic_number_per_foler:
                folder_name = folder_name.split('__')[0] + '__' +str((int(folder_name.split('__')[-1]) + 1))
                os.mkdir(folder_name)
                zf = zipfile.ZipFile('{}.zip'.format(folder_name), 'w', zipfile.ZIP_DEFLATED) # create new zip file to store file
                count_temp = i
            ### picture attributes to save as csv
            p_id = pic_attri[0]
            p_views = pic_attri[3]
            p_favo = pic_attri[2]
            p_url = pic_attri[1]
            ###
            img_path = os.path.join(source_img_path, p_id+'.jpg')
            try:
                target_path = folder_name + '\\' + p_id + '.jpg'
                shutil.copyfile(img_path, target_path) # move file to target folder
                zf.write(os.path.join(img_path)) # add file to target zip file
                print(img_path, 'data founded')
            except:
                try:
                    print(img_path, 'file not founded, try to get picture from flickr server')
                    urllib.request.urlretrieve(p_url,'{}{}.jpg'.format(folder_name +'\\',p_id))
                    zf.write(os.path.join(folder_name +'\\',p_id))
                    time.sleep(1)
                except:
                    try:
                        request_retry(p_url, p_id , folder_name = folder_name, timeout = 15)
                        zf.write(os.path.join(folder_name +'\\',p_id))
                    except:
                        print(p_id, 'url not found')
                        pass
            csv_writer.writerow([p_id, p_views, p_favo, p_url])
            if i > 500:
                break
    return

max_count_num = 25000
f_list = [[] for i in range(max_count_num)]

folder_path = 'data'
img_src_folder = 'picture\\2021_1120_142943_Images(2016 to 2020 and 2021 part1)\\'
file_list = os.listdir(folder_path)
file_list = [os.path.join(folder_path,i) for i in file_list]
for f_path in file_list:
    f_list = get_count_list(f_path, f_list)

sample_list = sample_by_favo(f_list, 1000, 25000)
pic_extract(sample_list, img_src_folder, 200, 'extract_by_favo_test.csv')
        
