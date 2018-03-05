""" This file is part of ReDyMo.

    Copyright (c) 2018  Gustavo Cayres and Marcelo Reis.

    ReDyMo is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or (at your
    option) any later version.
    ReDyMo is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
    for more details.
    You should have received a copy of the GNU General Public License along
    with ReDyMo. If not, see <http://www.gnu.org/licenses/>.

"""

import os
import sys

output_path = sys.argv[1]
chromosome_dict = dict()
aggregated_data = dict()
i = 0
for folder_name in next(os.walk(output_path))[1]:
    i += 1
    if folder_name.startswith('simulation_'):
        simulation_folder_path = output_path + folder_name + '/'
        for file_name in next(os.walk(simulation_folder_path))[2]:
            file_path = simulation_folder_path + file_name
            with open(file_path) as output_file:
                if file_name.startswith('cell'):
                    for line in output_file:
                        if len(line) == 1:
                            break

                        N, speed, time, inter_dist = line.split('\t')[0:4]
                        data = aggregated_data.get((int(N), int(speed)), [0, 0, 0, 0, 0])
                        data[0] += float(time)
                        data[1] += float(inter_dist)
                        data[2] += float(time) ** 2
                        data[3] += float(inter_dist) ** 2
                        data[4] += 1
                        aggregated_data[(int(N), int(speed))] = data

                else:
                    l = []
                    l_squared = []
                    for line in output_file:
                        l.append(int(line))
                        l_squared.append(int(line)**2)

                    if not chromosome_dict.get(file_name):
                        chromosome_dict[file_name] = [l, l_squared, 1]
                    else:
                        chromosome_dict[file_name][2] += 1
                        for i, value in enumerate(l):
                            chromosome_dict[file_name][0][i] += value

                        for i, value in enumerate(l_squared):
                            chromosome_dict[file_name][1][i] += value
    if i > 1000:
        break

for key, value in chromosome_dict.items():
    with open("aggregated_{}".format(key), 'w') as aggregated_file:
        for i in range(len(value[0])):
            i_sum = value[0][i]
            i_sum_squared = value[1][i]
            i_avg = i_sum/value[2]
            i_sd = 0 if value[2] == 1 else ((i_sum_squared / value[2] - (i_sum / value[2]) ** 2) * (value[2] / (value[2] - 1))) ** (1 / 2)
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
