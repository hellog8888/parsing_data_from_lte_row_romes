import os
import glob
import sqlite3
import openpyxl
import warnings
warnings.simplefilter("ignore")
from main import measure_time

file_xlxl_1 = glob.glob('source_folder\*.xlsx')

@measure_time
def export_to_sqlite(file_open):
    base_name = 'db_from_eirs.sqlite3'

    # метод sqlite3.connect автоматически создаст базу, если ее нет
    connect = sqlite3.connect('data_bases\\' + base_name)

    cursor = connect.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS cellular (Наименование_РЭС, Адрес, №_ЕТС, Наименование_вида_ЕТС, Состояние, Владелец, Широта, Долгота, Частоты, Дополнительные_параметры, Классы_излучения, Серия_последнего_действующего_РЗ_СоР, Номер_последнего_действующего_РЗ_СоР, Дата_начала_действия_последнего_действующего_РЗ_СоР, Срок_действия_последнего_действующего_РЗ_СоР, Номер_последнего_действующего_РИЧ, Дата_начала_последнего_действующего_РИЧ, Срок_действия_последнего_действующего_РИЧ)')

    file_to_read = openpyxl.load_workbook(file_open, data_only=True)
    sheet = file_to_read['SQL Results']

    for row in range(3, sheet.max_row + 1):
        data = []
        for col in range(1, sheet.max_column + 1):
            # value содержит значение ячейки с координатами row col
            value = sheet.cell(row, col).value
            data.append(value)

        cursor.execute("INSERT INTO cellular VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[10], data[11], data[17], data[18], data[19], data[20], data[21], data[24], data[25], data[26]))

    connect.commit()
    connect.close()


def clear_base():
    
    prj_dir = os.path.abspath(os.path.curdir)

    base_name = 'auto.sqlite3'

    connect = sqlite3.connect(prj_dir + '/' + base_name)
    cursor = connect.cursor()

    cursor.execute("DELETE FROM cellular")
    connect.commit()
    connect.close()


export_to_sqlite(file_xlxl_1[0])
#clear_base()
