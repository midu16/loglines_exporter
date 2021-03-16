
"""
This is the loglines_exporter non-ephemeral exporter of number of lines into a logfile
"""
__author__ = 'Mihai IDU'
import argparse
import time
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY, GaugeMetricFamily
from custom_classes import LogfileLister, CountLogfileLines

class CustomCollector(object):
    def __init__(self):
        pass
    def collect(self):
        g = GaugeMetricFamily("NumberofLinesinFile", 'Help text', labels=['filename'])
        for index in range(0, len(no_files)):
            file_name = str(logfile_path) + str(''.join(no_files[index]))
            no_lines_logfile = CountLogfileLines.LogFileLinesLister(str(file_name)).no_of_lines
            g.add_metric([file_name], no_lines_logfile)
        yield g

if __name__ == '__main__':
    # defining the global variable to be accessible to the class CustomCollector():
    global no_files
    global logfile_path
    # building the one-line-protocol for prometheus
    parser = argparse.ArgumentParser(
        description="Process Exporting the number of lines from a specific logfile - Mihai Idu 2021")
    parser.add_argument("-l", "--logfile-path", type=str,
                        help="Logfile path")
    parser.add_argument("-p", "--port", type=str, default="9091",
                        help="Changing the loglines_exporter port. Default=9091.")
    parser.add_argument("-s", "--server", action="store_true",
                        help="Activate the loglines_exporter server")
    # cli input are parse to variable
    args = parser.parse_args()
    logfile_path = args.logfile_path
    server = args.server
    port = int(args.port)
    # start the http server
    start_http_server(port)
    # building the objects related to the logfiles
    dl = LogfileLister.DirectoryLister(str(logfile_path))
    no_files = dl.directory
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(0.5)
