import glob
import pandas as pd
import warnings
warnings.simplefilter("ignore")

file_xlxl_1 = glob.glob('source_folder\*.xlsx')
print(file_xlxl_1[0])

#data = pd.read_excel(file_xlxl_1[0], usecols=[1, 2])
data = pd.read_excel(file_xlxl_1[0])
LTE_db = data.loc[:, ['Адрес']]

#print(LTE_db)

print(data)