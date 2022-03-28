import csv
import os
import numpy as np
import json
import random
import shutil
import urllib.request
import time
import socket


def cal_sample_size(np, p = 0.5, b = 0.03, c = 1.96):
    ns = (np*p*(1-p)) / (((np-1)*(b/c)**2)+(p*(1-p)))
    return ns


def get_count_list(file_path, output_list):
    
    with open(file_path, 'r', encoding= 'utf-8-sig') as data:
        csv_reader = csv.reader(data)
        next(csv_reader)
        for row in csv_reader:
            try:
                favo_count = int(row[-1])
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
            views_count = row[3]
            favo_count = row[-1]            
            output_list.append([p_id, views_count, favo_count, imgurl])

    return output_list


def save_list(data_list, csv_file_name):
    with open(csv_file_name, 'w', encoding= 'utf-8-sig', newline= '') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['id', 'views', 'favorites', 'url'])
        for row in data_list:
            csv_writer.writerow(row)

def request_retry(data, folder_name, timeout):
    p_url = data[3]
    p_id = data[0]
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

def sample_from_list(data_list, sample_size, source_img_path, output_folder_name):
    random_list = random.sample(data_list, sample_size)
    if not os.path.isdir(output_folder_name):
        os.mkdir(output_folder_name)
    save_list(random_list, 'random_sample.csv')
    for p in random_list:
        p_id = p[0]
        img_path = img_path = os.path.join(source_img_path, p_id+'.jpg')
        try:
            target_path = output_folder_name + '\\' + p_id + '.jpg'
            shutil.copyfile(img_path, target_path)
            print(img_path)
        except:
            try:
                print(img_path, 'file not founded, try to get picture from flickr server')
                p_url = p[-1]
                urllib.request.urlretrieve(p_url,'{}{}.jpg'.format(output_folder_name +'\\',p[0]))
                time.sleep(1)
            except:
                request_retry(data = p, folder_name = output_folder_name, timeout = 15)


folder_path = 'data'
file_list = os.listdir(folder_path)
file_list = [os.path.join(folder_path,i) for i in file_list]
f_list = []
for f_path in file_list:
    f_list = get_count_list(f_path, f_list)
sample_size = int(cal_sample_size(len(f_list)))
print('sample size = ',sample_size)
sample_from_list(f_list, sample_size, 'picture\\2021_1120_142943_Images(2016 to 2020 and 2021 part1)\\', 'random_sample')
