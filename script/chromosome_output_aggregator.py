import os
import sys

output_path = sys.argv[1]
chromosome_dict = dict()
for folder_name in next(os.walk(output_path))[1]:
    if folder_name.startswith('simulation_'):
        simulation_folder_path = output_path + folder_name + '/'
        for file_name in next(os.walk(simulation_folder_path))[2]:
            file_path = simulation_folder_path + file_name
            with open(file_path) as output_file:
                if file_name.startswith('cell'):
                    pass

                else:
                    l = []
                    for line in output_file:
                        l.append(int(line))

                    if not chromosome_dict.get(file_name):
                        chromosome_dict[file_name] = [l, 1]
                    else:
                        chromosome_dict[file_name][1] += 1
                        for i, value in enumerate(l):
                            chromosome_dict[file_name][0][i] += value

for key, value in chromosome_dict.items():
    with open("aggregated_{}".format(key), 'w') as aggregated_file:
        for i in value[0]:
            aggregated_file.write("{}\n".format(float(i/value[1])))
