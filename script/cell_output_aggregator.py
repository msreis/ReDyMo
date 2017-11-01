import sys
import os
from collections import defaultdict

aggregated_data = defaultdict(default_factory=lambda: [0, 0, 0, 0, 0])
for result_file_name in next(os.walk(sys.argv[1]))[2]:
    if result_file_name.startswith('cell_'):
        result_path = '{}{}'.format(sys.argv[1], result_file_name)
        with open(result_path) as result_file:
            for line in result_file:
                N, speed, time, inter_dist = line.split('\t')
                aggregated_data[(int(N), int(speed))][0] += float(time)
                aggregated_data[(int(N), int(speed))][1] += float(inter_dist)
                aggregated_data[(int(N), int(speed))][2] += float(time)**2
                aggregated_data[(int(N), int(speed))][3] += float(inter_dist)**2
                aggregated_data[(int(N), int(speed))][4] += 1


with open(sys.argv[2], 'w') as output_file:
    output_file.write("N\tinterorigin_distance\ttime_avg\ttime_sd\tinter_avg\tinter_sd\tmeasurements\t\n")
    for key, value in aggregated_data.items():
        time_avg = value[0]/value[4]
        inter_avg = value[1]/value[4]
        time_sd = 0 if value[4] == 1 else ((value[2] / value[4] - (value[0] / value[4]) ** 2) * (value[4] / (value[4] - 1))) ** (1 / 2)
        inter_sd = 0 if value[4] == 1 else ((value[3] / value[4] - (value[1] / value[4]) ** 2) * (value[4] / (value[4] - 1))) ** (1 / 2)
        line = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t\n".format(key[0], key[1], time_avg, time_sd, inter_avg, inter_sd, value[4])
        output_file.write(line)
