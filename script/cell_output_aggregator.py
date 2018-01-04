import os
import sys


output_path = sys.argv[1]
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
                    N, speed, period, time_1, time_2, inter_dist_1, inter_dist_2 = line.split('\t')[0:-1]
                    data = aggregated_data.get((int(N), int(speed), int(period)), [0, 0, 0, 0, 0, 0, 0, 0, 0])
                    data[0] += 1
                    data[1] += float(time_1)
                    data[2] += float(time_1) ** 2
                    data[3] += float(time_2)
                    data[4] += float(time_2) ** 2
                    data[5] += float(inter_dist_1)
                    data[6] += float(inter_dist_1) ** 2
                    data[7] += float(inter_dist_2)
                    data[8] += float(inter_dist_2) ** 2

                    aggregated_data[(int(N), int(speed), int(period))] = data

with open("aggregated_cell_data.txt", 'w') as aggregated_cell_file:
    aggregated_cell_file.write("N\tspeed\tperiod\ttime_S_avg\ttime_S_sd\tinter_S_avg\tinter_S_sd\t"
                               "time_limit_avg\ttime_limit_sd\tinter_limit_avg\tinter_limit_sd\t"
                               "measurements\t\n")
    for key, value in aggregated_data.items():
        time_s_avg = value[1]/value[0]
        time_limit_avg = value[3]/value[0]
        inter_s_avg = value[5] / value[0]
        inter_limit_avg = value[7] / value[0]

        time_s_sd = 0 if value[0] == 1 else ((value[2] / value[0] - (value[1] / value[0]) ** 2) * (value[0] / (value[0] - 1))) ** (1 / 2)
        time_limit_sd = 0 if value[0] == 1 else ((value[4] / value[0] - (value[3] / value[0]) ** 2) * (value[0] / (value[0] - 1))) ** (1 / 2)
        inter_s_sd = 0 if value[0] == 1 else ((value[6] / value[0] - (value[5] / value[0]) ** 2) * (value[0] / (value[0] - 1))) ** (1 / 2)
        inter_limit_sd = 0 if value[0] == 1 else ((value[8] / value[0] - (value[7] / value[0]) ** 2) * (value[0] / (value[0] - 1))) ** (1 / 2)
        line = "{}\t{}\t{}\t" \
               "{}\t{}\t{}\t{}\t" \
               "{}\t{}\t{}\t{}\t"\
               "{}\t\n".format(key[0], key[1], key[2],
                               time_s_avg, time_s_sd, inter_s_avg, inter_s_sd,
                               time_limit_avg, time_limit_sd, inter_limit_avg, inter_limit_sd,
                               value[0])
        aggregated_cell_file.write(line)
