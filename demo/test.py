import os

path = os.getcwd() + "/files/"
for files in os.listdir(path):
    file_split = files.split(".")
    if file_split[1] == "txt":
        f = open(path + files, 'r')
        for line in f:
            line = line[0:-1]
            print(line)
    else:
        print(files)