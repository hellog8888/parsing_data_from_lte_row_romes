import csv
import glob
import os

def search_row(tecRaw_file, bs_list_file):
    with open(tecRaw_file) as tecRaw_in, open(bs_list_file, 'r') as bs_nums:

        count = 0
        temp_bs_list = []
        temp_row_from_reader = []
        temp_dict_EARFCN = dict()

        for r in bs_nums:
            temp_bs_list.append(r.strip())
        print(f'номера бс: {temp_bs_list}')

        for row in csv.reader(tecRaw_in, delimiter=','):
            count += 1
            if count > 383:
                temp_row = row[0].split(';')[16]
                if temp_row in temp_bs_list:
                    temp_row_from_reader.append(*row)

        for i in temp_bs_list:
            try:
                os.mkdir(f'result_folder\{i}')
            except FileExistsError:
                pass

        for i in temp_bs_list:
            try:
                with open(f'result_folder\{i}\{i}.txt', 'w') as temp_result_file:

                    for x in temp_row_from_reader:
                        temp_x = x.split(';')
                        if temp_x[16] == i:
                            temp_dict_EARFCN[temp_x[9]] = temp_dict_EARFCN.get(temp_x[9], []) + [x]

                    for k, v in temp_dict_EARFCN.items():
                        min_v = -200
                        for v1 in v:
                            try:
                                temp_v = float(v1.split(';')[20])
                            except ValueError:
                                pass
                            print(temp_v)
                temp_dict_EARFCN.clear()

            except FileExistsError:
                pass


export_file = glob.glob('source_folder\*.csv')
bs_file = glob.glob('source_folder\*.txt')

search_row(export_file[0], bs_file[0])

# ['15.05.2023;15:10:29.969;1686820229;45.077795;39.015200;19.11;34.16;176.09;10;38750;2310000000;196;250;20;27013;59307298;231669;34;;7;-71.12;11.97;-94.97;-17.13;-16.43;239.37;0.000002054501;2233662;no;no;4;;20.0;']
# [';;;;;;;;;;;;;;;;231669;34;;7;-71.12;11.97;-94.97;-17.13;-16.43;239.37;0.000002054501;2233662;no;no;4;;20.0;']
# count ';' for num_bs

#from datetime import datetime
# time_now = f'{cur_time.day:02}_{cur_time.month:02}_{cur_time.year}__{cur_time.hour:02}_{cur_time.minute:02}_{cur_time.second:02}'
#cur_time = datetime.now()

#tecRaw_in.seek(520)

#print(f'используемые файлы: {export_file}, {bs_file}')