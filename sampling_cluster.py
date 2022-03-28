import csv
import os
import matplotlib.pyplot as plt
import numpy as np
import json
import random
import shutil
import urllib.request
import time
import socket

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


def sample_from_list(data_list, start_number, end_number, cluster_number, sample_number):
    data_len = end_number - start_number
    step = data_len//cluster_number 
    result_list = []
    print('step = ', step)
    
    for i in range(start_number, end_number, step):
        if i + step > end_number:
            continue
        temp_list = []
        ### create temp list in step ###
        for j in range(i, i + step):
            # print('index = ', j)
            # print('len = ', len(data_list[j]))
            for id in data_list[j]:
                temp_list.append(id)
            
        element_len = len(temp_list)
        ### data check ###
        if element_len == 0 :
            print('cluster number ', i, 'has no photo')
            result_list.append([i, 'no photo'])
            continue
        if element_len <= sample_number:
            print(element_len)
            print('count number ', i, 'do not have enough data')
            result_list.append([i, 'do not have enough data'])
            continue
        
        ### random sampling ###
        random_number = [r for r in range(element_len)]
        random_list = random.sample(random_number, sample_number)
        result_list.append([i, [temp_list[r_id] for r_id in random_list]])
    
    return result_list


def request_retry(p_url, p_id, folder_name, timeout):
    # p_url = data[1]
    # p_id = data[0]
    socket.setdefaulttimeout(timeout) #設定連線愈時時間 
    download_count = 0
    try:
        urllib.request.urlretrieve(p_url,'{}{}.jpg'.format(folder_name +'\\',p_id))
        print(p_id+"已下載，並確認於資料庫")
        download_count += 1
    except socket.error:
        count = 1
        while count <= 5: 
            socket.setdefaulttimeout(15) #重新計時連線時間
            try:
                print('連線愈時，重新下載',p_id)
                urllib.request.urlretrieve(p_url,'{}\\{}.jpg'.format(folder_name,p_id))
                print(p_id+"已下載，並確認於資料庫")
                download_count += 1
                break
            except socket.error:
                count += 1
            if count > 5:
                print(p_id,'嘗試次數>5次，下載失敗')
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


max_count_num = 25000
f_list = [[] for i in range(max_count_num)]

folder_path = 'data'
file_list = os.listdir(folder_path)
file_list = [os.path.join(folder_path,i) for i in file_list]

for f_path in file_list:
    f_list = get_count_list(f_path, f_list)

# sample_data = sample_from_list(f_list, 5, 990, 7, 25)
# folder_list, c_list = get_pic(sample_data, 'picture\\2021_1120_142943_Images(2016 to 2020 and 2021 part1)\\')
# print(f_list, c_list)
for i in range(10,21):
    sample_data = sample_from_list(f_list, 5, 990, 7, 25)
    folder_list, c_list = get_pic(sample_data, 'picture\\2021_1120_142943_Images(2016 to 2020 and 2021 part1)\\')
    sample_folder_name = 'sample' + str(i)
    if not os.path.isdir(sample_folder_name):
            os.mkdir(sample_folder_name)
    
    for folder_name in folder_list:
        shutil.move(folder_name, sample_folder_name)
    for csv_name in c_list:
        shutil.move(csv_name, sample_folder_name)


