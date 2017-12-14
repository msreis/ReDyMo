import os
import sys
import re


output_path = sys.argv[1]
chromosome_dict = dict()
number_of_folders = 0
for folder_name in next(os.walk(output_path))[1]:
    if not folder_name.startswith('simulation_'):
        continue

    simulation_folder_path = output_path + folder_name + '/'
    N = None
    speed = None
    period = None
    for file_name in next(os.walk(simulation_folder_path))[2]:
        file_path = simulation_folder_path + file_name
        if file_name.startswith('cell'):
            with open(file_path) as output_file:
                line = output_file.readline()
                N, speed, time, inter_dist = line.split('\t')[0:4]

    if N != "10":
        continue

    number_of_folders += 1
    if number_of_folders > 100:
        break

    for file_name in next(os.walk(simulation_folder_path))[2]:
        file_path = simulation_folder_path + file_name
        if not file_name.startswith('cell'):
            with open(file_path) as output_file:
                l = []
                for line in output_file:
                    l.append(int(line))

                p = re.compile('(.*)\.txt')
                key = p.match(file_name).group(0) + "_" + str(N) + ".txt"
                if not chromosome_dict.get(key):
                    chromosome_dict[key] = [l]

                else:
                    chromosome_dict[key].append(l)


for key, value in chromosome_dict.items():
    with open("union_{}".format(key), 'w') as union_file:
        for data_list in list(map(list, zip(*value))):
            for data in data_list:
                union_file.write("{} ".format(data))

            union_file.write("\n")
