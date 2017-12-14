import os
import sys
import re


output_path = sys.argv[1]
chromosome_dict = dict()
aggregated_data = dict()
number_of_folders = 0
for folder_name in next(os.walk(output_path))[1]:
    if folder_name.startswith('simulation_'):
        simulation_folder_path = output_path + folder_name + '/'
        N = None
        speed = None
        period = None
        for file_name in next(os.walk(simulation_folder_path))[2]:
            file_path = simulation_folder_path + file_name
            if file_name.startswith('cell'):
                with open(file_path) as output_file:
                    line = output_file.readline()
                    N, speed, period, time, inter_dist = line.split('\t')[0:5]
                    data = aggregated_data.get((int(N), int(speed), int(period)), [0, 0, 0, 0, 0])
                    data[0] += float(time)
                    data[1] += float(inter_dist)
                    data[2] += float(time) ** 2
                    data[3] += float(inter_dist) ** 2
                    data[4] += 1
                    aggregated_data[(int(N), int(speed), int(period))] = data

        for file_name in next(os.walk(simulation_folder_path))[2]:
            file_path = simulation_folder_path + file_name
            if not file_name.startswith('cell'):
                with open(file_path) as output_file:
                    l = []
                    l_squared = []
                    for line in output_file:
                        l.append(int(line))
                        l_squared.append(int(line)**2)
                    p = re.compile('(.*)\.txt')
                    key = p.match(file_name).group(0) + "_" + str(N) + "_" + str(speed) + "_" + str(period) + ".txt"
                    if not chromosome_dict.get(key):
                        chromosome_dict[key] = [l, l_squared, 1]

                    else:
                        chromosome_dict[key][2] += 1
                        for i, value in enumerate(l):
                            chromosome_dict[key][0][i] += value

                        for i, value in enumerate(l_squared):
                            chromosome_dict[key][1][i] += value

    number_of_folders += 1
    if number_of_folders > 1000:
        break

for key, value in chromosome_dict.items():
    with open("aggregated_{}".format(key), 'w') as aggregated_file:
        for i in range(len(value[0])):
            i_sum = value[0][i]
            i_sum_squared = value[1][i]
            i_avg = i_sum/value[2]
            i_sd = 0 if value[2] == 1 else ((i_sum_squared - ((i_sum ** 2) / value[2])) / (value[2] - 1)) ** (1 / 2)
            aggregated_file.write("{}\t{}\t\n".format(i_avg, i_sd))

with open("aggregated_cell_data.txt", 'w') as aggregated_cell_file:
    aggregated_cell_file.write("N\tspeed\ttime_avg\ttime_sd\tinter_avg\tinter_sd\tmeasurements\t\n")
    for key, value in aggregated_data.items():
        time_avg = value[0]/value[4]
        inter_avg = value[1]/value[4]
        time_sd = 0 if value[4] == 1 else ((value[2] / value[4] - (value[0] / value[4]) ** 2) * (value[4] / (value[4] - 1))) ** (1 / 2)
        inter_sd = 0 if value[4] == 1 else ((value[3] / value[4] - (value[1] / value[4]) ** 2) * (value[4] / (value[4] - 1))) ** (1 / 2)
        line = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t\n".format(key[0], key[1], time_avg, time_sd, inter_avg, inter_sd, value[4])
        aggregated_cell_file.write(line)
