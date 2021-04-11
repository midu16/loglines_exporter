"""
This is the loglines_exporter ephemeral exporter of number of lines into a logfile.
The ephemeral is determed by the dynamic of the creation of the files over time.
"""
__author__ = 'Mihai IDU'

"""
Importing the libraries.
"""
import argparse
from os import stat
import os
import time
import requests
from custom_classes import CountLogfileLines
from pwd import getpwuid

def logfilenoline_data_payload(dirname):
    """
        This function is building the payload of the post method to the pushgateway-server.
    :param dirname:            The dirname of the directory under which the current are persistent store.
    :return:                    The retun is a REST-API POST call to the Prometheus-pushgateway endpoint.
    """
    files = os.listdir(dirname)
    temp = map(lambda name: os.path.join(dirname, name), files)
    list_temp = list(temp)
    loglines_dict = {
        "NumberofLinesinFile" + "{" + "filename=" + '"' + str(''.join(list_temp[index])) + '"' + " , " + "username=" +
        '"' + str(getpwuid(
            stat(str(''.join(list_temp[index]))).st_uid).pw_name) + '"' + "}": CountLogfileLines.LogFileLinesLister(
            str(''.join(list_temp[index]))).no_of_lines
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
    return data

def logfilesize_data_payload(dirname):
    """
        This function is building the payload of the post method to the pushgateway-server.
    :param dirname:            The dirname of the directory under which the current are persistent store.
    :return:                    The retun is a REST-API POST call to the Prometheus-pushgateway endpoint.
    """
    files = os.listdir(dirname)
    temp = map(lambda name: os.path.join(dirname, name), files)
    list_temp = list(temp)
    loglines_dict = {
        "SizeOfLogFile" + "{" + "filename=" + '"' + str(''.join(list_temp[index])) + '"' + " , " + "username=" +
        '"' + str(getpwuid(
            stat(str(''.join(list_temp[index]))).st_uid).pw_name) + '"' + "}": str(os.stat(str(''.join(list_temp[index]))).st_size)
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
    return data




# building the pushgateway_post function
def pushgateway_post(endpoint, data):
    """"
        The function is transporting the payload to the designated endpoint.
    :param endpoint:            Cli custom value of the enpoint. type string. <ip_addr>:<port>
    :param data:                The data-payload to be transporter
    :return:                    The return is a REST-API POST call to the prometheus-pushgateway-server endpoint.
    """
    #curl -X POST -H  "Content-Type: text/plain" --data "$var" http://localhost:9091/metrics/job/top/instance/machine
    myhost = os.uname()[1]
    url = 'http://'+str(endpoint)+'/metrics/job/loglines_exporter/instance/'+str(myhost)
    headers = {'X-Requested-With': 'Python requests', 'Content-type': 'text/xml'}
    return requests.post(url, data='%s' % data, headers=headers)


#list to plain text function conversion for better
def fun(data):
    return "".join([str(item) for var in data for item in var])


if __name__ == '__main__':
    # building the one-line-protocol for prometheus
    parser = argparse.ArgumentParser(
                            description="Process Exporting the number of lines from a specific logfile - Mihai Idu 2021")
    parser.add_argument("-pp", "--prometheus-pushgateway", action="store_true",
                        help="Push the data to the Prometheus pushgateway each second. Using default "
                             "endpoint http://localhost:9091/metrics/job/top/instance/machine")
    parser.add_argument("-e", "--pushgateway-server-ipaddr", type=str, default="localhost",
                        help="Changing the localhost pudshgateway-server IPaddr. Default=localhost")
    parser.add_argument("-p", "--pushgateway-server-port", type=str, default="9091",
                        help="Changing the pushgateway-server port. Default=9091.")
    parser.add_argument("-l", "--logfile-path", type=str,
                        help="Logfile path")
    parser.add_argument("-ns", "--not-server", action="store_true",
                        help="Activate the loglines_exporter server")
    # cli input are parse to variable
    args = parser.parse_args()
    logfile_path = args.logfile_path
    not_server = args.not_server
    prometheus_pushgateway = args.prometheus_pushgateway
    pushgateway_server_ip_addr = str(args.pushgateway_server_ipaddr)
    pushgateway_server_port = str(args.pushgateway_server_port)

    if prometheus_pushgateway:
        while prometheus_pushgateway:
            endpoint_pushgateway = str(pushgateway_server_ip_addr) + ":" + str(pushgateway_server_port)
            pushgateway_post(endpoint_pushgateway, fun(logfilenoline_data_payload(logfile_path)))
            time.sleep(1)
            pushgateway_post(endpoint_pushgateway, fun(logfilesize_data_payload(logfile_path)))
    else:
        if not_server:
            print(fun(logfilenoline_data_payload(logfile_path)))
            print(fun(logfilesize_data_payload(logfile_path)))
        else:
            print("Please, check the $loglines_exporter -h!")
