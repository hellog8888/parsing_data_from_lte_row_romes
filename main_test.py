import glob

file = glob.glob('source_folder/344.txt')

temp = []

with open(file[0], 'r') as f:
    for i in f:
        temp.append(i)

print(len(temp))
print(len(set(temp)))