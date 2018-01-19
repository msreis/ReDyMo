""" This file is part of ReDyMo.

    ReDyMo is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or (at your
    option) any later version.

    ReDyMo is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License along
    with ReDyMo. If not, see <http://www.gnu.org/licenses/>. """

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
                    N, speed, period, time_1, inter_dist_1 = line.split('\t')[0:-1]
                    data = aggregated_data.get((int(N), int(speed), int(period)), [0, 0, 0, 0, 0])
                    data[0] += 1
                    data[1] += float(time_1)
                    data[2] += float(time_1) ** 2
                    data[3] += float(inter_dist_1)
                    data[4] += float(inter_dist_1) ** 2

                    aggregated_data[(int(N), int(speed), int(period))] = data

        p = re.compile('(Tb927_.+_v5\.1)\.txt')
        for file_name in next(os.walk(simulation_folder_path))[2]:
            file_path = simulation_folder_path + file_name
            if p.match(file_name):
                with open(file_path) as output_file:
                    l = []
                    l_squared = []
                    for line in output_file:
                        l.append(int(line))
                        l_squared.append(int(line)**2)
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
    aggregated_cell_file.write("N\tspeed\tperiod\ttime_S_avg\ttime_S_sd\tinter_S_avg\tinter_S_sd\t"
                               "measurements\t\n")
    for key, value in aggregated_data.items():
        time_s_avg = value[1]/value[0]
        inter_s_avg = value[3] / value[0]

        time_s_sd = 0 if value[0] == 1 else ((value[2] / value[0] - (value[1] / value[0]) ** 2) * (value[0] / (value[0] - 1))) ** (1 / 2)
        inter_s_sd = 0 if value[0] == 1 else ((value[4] / value[0] - (value[3] / value[0]) ** 2) * (value[0] / (value[0] - 1))) ** (1 / 2)
        line = "{}\t{}\t{}\t" \
               "{}\t{}\t{}\t{}\t" \
               "{}\t\n".format(key[0], key[1], key[2],
                               time_s_avg, time_s_sd, inter_s_avg, inter_s_sd,
                               value[0])
        aggregated_cell_file.write(line)
