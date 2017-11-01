import sys
import os


aggregated_data = dict()
for result_file_name in next(os.walk(sys.argv[1]))[2]:
    if result_file_name.startswith('cell_'):
        result_path = '{}{}'.format(sys.argv[1], result_file_name)
        with open(result_path) as result_file:
            for line in result_file:
                if len(line) == 1:
                    break

                N, speed, time, inter_dist = line.split('\t')[0:4]
                data = aggregated_data.get((int(N), int(speed)), [0, 0, 0, 0, 0])
                data[0] += float(time)
                data[1] += float(inter_dist)
                data[2] += float(time)**2
                data[3] += float(inter_dist)**2
                data[4] += 1
                aggregated_data[(int(N), int(speed))] = data

with open(sys.argv[2], 'w') as output_file:
    output_file.write("N\tinterorigin_distance\ttime_avg\ttime_sd\tinter_avg\tinter_sd\tmeasurements\t\n")
    for key, value in aggregated_data.items():
        time_avg = value[0]/value[4]
        inter_avg = value[1]/value[4]
        time_sd = 0 if value[4] == 1 else ((value[2] / value[4] - (value[0] / value[4]) ** 2) * (value[4] / (value[4] - 1))) ** (1 / 2)
        inter_sd = 0 if value[4] == 1 else ((value[3] / value[4] - (value[1] / value[4]) ** 2) * (value[4] / (value[4] - 1))) ** (1 / 2)
        line = "{}\t{}\t{}\t{}\t{}\t{}\t{}\t\n".format(key[0], key[1], time_avg, time_sd, inter_avg, inter_sd, value[4])
        output_file.write(line)
