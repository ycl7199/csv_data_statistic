import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import json

def get_cal(file_path, views_cout, favo_count):
    print(file_path, 'start processing')
    with open(file_path, 'r', encoding= 'utf-8-sig') as data:
        csv_reader = csv.reader(data)
        next(csv_reader)
        for i, row in enumerate(csv_reader):
            # print(row[3], row[-1])
            if row[3] not in views_cout:
                views_cout[row[3]] = 1
            else:
                views_cout[row[3]] += 1
            try:
                f_num = int(row[-1])
                if row[-1] not in favo_count:
                    favo_count[row[-1]] = 1
                else:
                    favo_count[row[-1]] += 1
            except:
                pass

            # if i > 100:
            #     break
    return views_cout, favo_count   

def save_csv(f_name,list1, list2):
    with open(f_name, 'w', encoding='utf-8-sig', newline= '') as data:
        csv_writer = csv.writer(data)
        csv_writer.writerow(list1)
        csv_writer.writerow(list2)

def dict2list(input_dict):
    index_num = [int(key) for key, value in input_dict.items()]
    output_list = [0 for i in range(max(index_num)+1)]
    for i in input_dict:
        output_list[int(i)] = input_dict[i]
    return output_list

def visualize_and_save(data, pic_name, csv_name):
    ### Visualize & Generate csv file ###
    x_data = [i[0] for i in data]
    y_data = [i[1] for i in data]
    x = np.arange(len(x_data))
    fig=plt.figure()
    plt.bar(x, y_data, color='blue')
    plt.xticks(x, x_data)
    # plt.xlabel('number')
    # plt.ylabel('count')
    plt.title(pic_name.split('.')[0])
    plt.savefig(pic_name)
    # plt.show()
    plt.cla()
    save_csv(csv_name, x_data, y_data)

def visualize_with_step(data, start, end, step, pic_name, csv_name):
    ### Visualize & Generate csv file ###
    x_data = []
    y_data = []
    print('data length = ', len(data))
    print('start from ',start)
    print('end at ', end)
    for i in range(start, end, step):
        temp = 0
        for j in range(i, i+step):
            try:
                temp += data[j]
            except:
                ### finel step ### 
                continue
        y_data.append(temp)
        x_data.append(i)

    x = np.arange(len(x_data))
    fig=plt.figure()
    plt.bar(x, y_data, color='blue')
    plt.xticks(x, x_data)
    # plt.xlabel('number')
    # plt.ylabel('count')
    plt.title(pic_name.split('.')[0])
    plt.savefig(pic_name)
    plt.show()
    plt.cla()
    save_csv(csv_name, x_data, y_data)
    print(len(x_data))

### load file in specified folder ###
folder_path = 'data'
file_list = os.listdir(folder_path)
file_list = [os.path.join(folder_path,i) for i in file_list]

v_sum = 0
f_sum = 0
v_count = {}
f_count = {}
### load csv file & calculate ###
for f_path in file_list:
    v_count, f_count = get_cal(f_path, v_count, f_count)
    # print(v_count,f_count)

### visual & transfer to csv file ###
v_list = dict2list(v_count)
visualize_with_step(v_list, 1, 20, 1, 'step_test_v.png','step_test_v_1.csv')

f_list = dict2list(f_count)
visualize_with_step(f_list, 1, 20, 1, 'step_test_f.png','step_test_f_1.csv')





    
