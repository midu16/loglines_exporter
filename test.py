import os
from os import stat
from custom_classes import LogfileLister, CountLogfileLines
from pwd import getpwuid
import fnmatch
extension = '*.log'
dirname = 'test/'
while 1:
    files = os.listdir(dirname)
    temp = map(lambda name: os.path.join(dirname, name), files)
    list_temp = list(temp)
    #print(list_temp)
    for index in list_temp:
        if os.path.isdir(index):
            list_temp.remove(index)
            files_sub_dir = fnmatch.filter(os.listdir(index), extension)
            #print(os.listdir(index))
            temp_sub_dir = map(lambda name: os.path.join(index, name), files_sub_dir)
            list_temp = list_temp + list(temp_sub_dir)
        elif os.path.isfile(index):
            list_temp.remove(index)
            index = index.replace(dirname, "")
            files_sub_maindir = fnmatch.filter(os.listdir(dirname), extension)
            #print(index)
            temp_sub_maindir = map(lambda name: os.path.join(dirname, name), files_sub_maindir)
            list_temp = list_temp + list(temp_sub_maindir)
    print(list_temp)
        #elif fnmatch.filter(os.listdir(index), "*.log"):

    #print(list_temp)
    """
    loglines_dict = {"NumberofLinesinFile" + "{" + "filename=" + '"' + str(''.join(list_temp[index])) + '"' + " , " + "owner=" +
                     '"' + str(getpwuid(stat(str(''.join(list_temp[index]))).st_uid).pw_name) + '"' + "}": CountLogfileLines.LogFileLinesLister(str(''.join(list_temp[index]))).no_of_lines
                        for index in range(0, len(list_temp))}
    key = []
    for index in loglines_dict.keys():
        key.append(str(index))

    value = []
    for index in loglines_dict.values():
        value.append(str(round(index, 2)))

    data = []
    for index in range(0, len(loglines_dict.keys())):
        data.append(str(key[index]) + ' ' + str(value[index]) + '\n')
    #print(data)

    #print(no_lines_logfile)
    """