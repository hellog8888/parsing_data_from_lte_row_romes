import csv
import glob
import os
import datetime
#from string import zfill
from PIL import Image, ImageDraw, ImageFont

BASE_STATION_LIST = []
BASE_STATION_OPERATOR = dict()
DICT_OPERATOR = {'1': 'mts', '2': 'megafon', '20': 't2_mobile', '99': 'beeline'}

def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.datetime.now()
        elapsed_time = end_time - start_time
        print(f"Execution time: {elapsed_time}")
        return result

    return wrapper

def convert_to_img(file_name, path_to_save=''):
    path_to_save_file = path_to_save

    # Задаем размеры изображения и цвет фона
    width = 1830
    height = 180
    bg_color = (255, 255, 255)

    # Определяем шрифт, размер и цвет текста
    font_size = 30
    font = ImageFont.truetype("arial.ttf", font_size)
    text_color = (0, 0, 0)

    #file_to_img = glob.glob('*.txt')
    h_Data = 'Date'
    h_Time = 'Time'
    h_EARFCN = 'EARFCN'
    h_Frequency = 'Frequency'
    h_PCI = 'PCI'
    h_MCC = 'MCC'
    h_MNC = 'MNC'
    h_TAC = 'TAC'
    h_CI = 'CI'
    h_eNodeB_ID = 'eNodeB-ID'
    h_Power = 'Power'
    h_MIB_Bandwidth_MHz = 'MIB_Bandwidth(MHz)'
    header_to_img = f'{h_Data.center(15)} | {h_Time.center(10)} | {h_EARFCN.center(0)} | {h_Frequency.center(0)} | {h_PCI.center(0)} | {h_MCC.center(0)} | {h_MNC.center(0)} | {h_TAC.center(6)} | {h_CI.center(17)} | {h_eNodeB_ID.center(0)} | {h_Power.center(0)} | {h_MIB_Bandwidth_MHz.center(0)}'
    line_separator = '-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'

    with open(file_name, 'r') as file:
        count_line = 0
        for line in file.readlines():
            # print(line.strip())
            count_line += 1
            # Создаем объект Image и объект ImageDraw
            image = Image.new('RGB', (width, height), color=bg_color)
            draw = ImageDraw.Draw(image)
            # 1) смещение по размеру изображения
            draw.text((30, 47), f'{header_to_img}\n{line_separator}\n{line}', fill=text_color, font=font)
            # Сохраняем изображение в файл
            image.save(f'{path_to_save_file}_{count_line}.png')

@measure_time
def search_row(tecRaw_file, bs_list_file):
    with open(tecRaw_file) as tecRaw_in, open(bs_list_file, 'r') as bs_nums:

        count = 0
        temp_row_from_reader = []
        temp_dict_EARFCN = dict()
        header_row = 'Date;Time;EARFCN;Frequency;PCI;MCC;MNC;TAC;CI;eNodeB-ID;Power;MIB_Bandwidth(MHz)'

        for i in bs_nums:
            BASE_STATION_LIST.append(i.strip())

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
                os.mkdir(f'result_folder\{i}_{DICT_OPERATOR[BASE_STATION_OPERATOR[i]]}')
            except FileExistsError:
                pass
            except KeyError:
                pass

        for i in BASE_STATION_LIST:
            try:
                name_operator = DICT_OPERATOR[BASE_STATION_OPERATOR[i]]
                with open(f'result_folder\{i}_{name_operator}\{i}_{name_operator}.csv', 'w') as temp_result_file,\
                        open(f'result_folder\{i}_{name_operator}\{i}_{name_operator}.txt', 'w') as temp_result_file_txt:

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
                        #print(f'Date | Time | EARFCN | Frequency | PCI | MCC | MNC | TAC | CI | eNodeB-ID | Power | MIB_Bandwidth(MHz)', file=temp_result_file_txt)

                        row_to_res = temp_row_dict.split(';')
                        date_, time_, earfcn, = row_to_res[0], row_to_res[1][:8], row_to_res[9]
                        frequency_, pci, mcc, mnc = f'{row_to_res[10][:4]}.{row_to_res[10][4]}', row_to_res[11], row_to_res[12], row_to_res[13]
                        tac, ci, enodebid, power = row_to_res[14], row_to_res[15], row_to_res[16], row_to_res[20]
                        mib_dl_bandwidth_mhz_ = row_to_res[32]

                        print(date_, time_, earfcn, frequency_, pci, mcc, mnc, ci, enodebid, power, mib_dl_bandwidth_mhz_)
                        print(';'.join([date_, time_, earfcn, frequency_, pci, mcc, mnc, tac, ci, enodebid, power, mib_dl_bandwidth_mhz_]), file=temp_result_file)
                        print(f'{date_.center(0)} | {time_.center(0)} | {earfcn.center(12)} | {frequency_.center(12)} | {pci.center(3)} | {mcc.center(5)} | {mnc.center(7)} | {tac.center(0)} | {ci.center(0)} | {enodebid.center(12)} | {power.center(0)} | {mib_dl_bandwidth_mhz_.center(30)}', file=temp_result_file_txt)
                        print('\n', file=temp_result_file)
                        #print('\n', file=temp_result_file_txt)

                temp_dict_EARFCN.clear()
                print()
            except FileExistsError:
                pass
            except KeyError:
                pass

        for i in BASE_STATION_LIST:
            try:
                name_operator = DICT_OPERATOR[BASE_STATION_OPERATOR[i]]
                #path_to_folder = f'result_folder\{i}_{name_operator}\{i}_{name_operator}.txt'
                convert_to_img(f'result_folder\{i}_{name_operator}\{i}_{name_operator}.txt', f'result_folder\{i}_{name_operator}\{i}_{name_operator}')
            except FileExistsError:
                pass
            except KeyError:
                pass


if __name__ == "__main__":

    export_file = glob.glob('source_folder\*.csv')
    bs_file = glob.glob('source_folder\*.txt')

    search_row(export_file[0], bs_file[0])


# information:
# +107 power and -107 power convert for spectre
