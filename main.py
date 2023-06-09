import csv
import glob
import os
import datetime
from numpy import genfromtxt

BASE_STATION_LIST = []
BASE_STATION_OPERATOR = dict()

def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.datetime.now()
        elapsed_time = end_time - start_time
        print(f"Execution time: {elapsed_time}")
        return result

    return wrapper

@measure_time
def search_row(tecRaw_file, bs_list_file):
    with open(tecRaw_file) as tecRaw_in, open(bs_list_file, 'r') as bs_nums:

        count = 0
        temp_row_from_reader = []
        temp_dict_EARFCN = dict()
        header_row = 'Date;Time;EARFCN;Frequency;PCI;MCC;MNC;TAC;CI;eNodeB-ID;Power;MIB_Bandwidth(MHz)'

        for r in bs_nums:
            BASE_STATION_LIST.append(r.strip())
        print(f'номера бс: {BASE_STATION_LIST}')
        print()

        for row in csv.reader(tecRaw_in, delimiter=','):
            count += 1
            if count > 383:
                temp_row_operator = row[0].split(';')[13]
                temp_row = row[0].split(';')[16]
                if temp_row in BASE_STATION_LIST:
                    temp_row_from_reader.append(*row)
                    BASE_STATION_OPERATOR[temp_row] = BASE_STATION_OPERATOR.get(temp_row, temp_row_operator)

        for i in BASE_STATION_LIST:
            try:
                os.mkdir(f'result_folder\{i}')
            except FileExistsError:
                pass

        for i in BASE_STATION_LIST:
            try:
                with open(f'result_folder\{i}\{i}.csv', 'w') as temp_result_file:

                    for x in temp_row_from_reader:
                        temp_x = x.split(';')
                        if temp_x[16] == i:
                            temp_dict_EARFCN[temp_x[9]] = temp_dict_EARFCN.get(temp_x[9], []) + [x]

                    for k, v in temp_dict_EARFCN.items():
                        min_v = -200
                        temp_row_dict = ''
                        for v1 in v:
                            try:
                                temp_v_dict = float(v1.split(';')[20])
                                if temp_v_dict > min_v:
                                    min_v = temp_v_dict
                                    temp_row_dict = v1
                            except ValueError:
                                pass

                        print(header_row, file=temp_result_file)

                        row_to_res = temp_row_dict.split(';')
                        date_, time_, earfcn, = row_to_res[0], row_to_res[1][:8], row_to_res[9]
                        frequency_, pci, mcc, mnc = f'{row_to_res[10][:4]}.{row_to_res[10][4]}', row_to_res[11], row_to_res[12], row_to_res[13]
                        tac, ci, enodebid, power = row_to_res[14], row_to_res[15], row_to_res[16], row_to_res[20]
                        mib_dl_bandwidth_mhz_ = row_to_res[32]

                        print(date_, time_, earfcn, frequency_, pci, mcc, mnc, ci, enodebid, power, mib_dl_bandwidth_mhz_)
                        print(';'.join([date_, time_, earfcn, frequency_, pci, mcc, mnc, tac, ci, enodebid, power, mib_dl_bandwidth_mhz_]), file=temp_result_file)
                        print('\n', file=temp_result_file)

                temp_dict_EARFCN.clear()
                print()
            except FileExistsError:
                pass

def convert_to_img():
    test_csv_file = glob.glob('result_folder\\453535\*.csv')
    print(test_csv_file)
    my_data = genfromtxt(test_csv_file, delimiter=',')
    print(my_data)
    print(BASE_STATION_LIST)


if __name__ == "__main__":

    export_file = glob.glob('source_folder\*.csv')
    bs_file = glob.glob('source_folder\*.txt')

    search_row(export_file[0], bs_file[0])
    print(BASE_STATION_OPERATOR)
    #convert_to_img()

# +107 power and -107 power
