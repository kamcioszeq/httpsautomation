#!/usr/bin/env python3
import socket
import requests
import csv
from datetime import datetime
import sys, os, re
import argparse

# static variables
filesites = sys.argv[-1]
result = []
sumator = []

# static path to files
path_logs = os.path.join(os.path.expanduser('/'), 'var', 'log', 'stats', 'logs.csv')
path_dir_stats = os.path.join(os.path.expanduser('/'), 'var', 'log', 'stats')
path_all_statistics = os.path.join(os.path.expanduser('/'), 'var', 'log', 'stats', 'statistics.csv')


# function to verify input file for arguments
def valid_file(arg):
    base, ext = os.path.splitext(arg)
    if ext.lower() not in ('.txt'):
        raise argparse.ArgumentTypeError('Wrong extension')
    return arg


# function to verificate url
def request_site(url):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((url, 80))
        print("Http connection open :" + url + ": 80")
        status_code = 200
    except:
        print("Http connection close(service unreachable) :" + url)
        status_code = 0

    return str(status_code)


# function to verify SSL port of url
def isSSL_open(url, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((url, port))
        print("Connection open")
        return True
    except Exception:
        print("Port 443 is closed")
        return False


# function to verify SSL Certificate
def check_certificate(url):
    try:
        requests.get(f"https://{url}")
        return ("SSL Certificate Valid")
    except Exception:
        return ('SSL Certificate invalid')


# function to generate output
def generate_csv_stats(url):
    status_code = request_site(url)
    openSSL = isSSL_open(url, 443)
    cert = check_certificate(url)

    return {"url:": url, "status_code": status_code, "SSL open:": openSSL, "SSL Certificate:": cert,
            "Date_time: ": datetime.now()}


# function to generate log file in /var/log/stats
def write_to_file(path_logs):
    with open(path_logs, "a") as csvfile:
        record = [generate_csv_stats(url) for url in lines]
        writer = csv.DictWriter(csvfile, fieldnames=record[0].keys())
        writer.writerows(record)


# function to create /var/log/stats folder if missing
def create_dir(stats_dir):
    try:
        os.mkdir(stats_dir)
        print("Directory /var/log/stats created")
    except:
        print("Directory /var/log/stats exist")


# function to read log file and create CSV with statistics
def read_csv_log(path_logs, stats_path):
    with open(path_logs) as file:
        csv_reader_object = list(csv.reader((line.replace('\0', '') for line in file), delimiter=","))
        for i in lines:
            counter = 0
            total = 0
            for row in csv_reader_object:
                if row[0] == i:
                    if row[1] == "200":
                        counter = counter + 1
                        total = total + 1
                    else:
                        total = total + 1
            try:
                count_percent = ((counter * 100) / total)
                count_percent = count_percent / 100
            except:
                count_percent = 0
            result.append("{:.01%}".format(count_percent))
            sumator.append(int(total))

    with open(stats_path, 'w+') as myfile:
        wr = csv.writer(myfile)
        for i in zip(lines, result):
            wr.writerow(i)


if __name__ == '__main__':

    # Help parser

    parser = argparse.ArgumentParser(
        description="Check http and https connection to selected websites from file 'sites.txt' \
                    or by url of website input. If website is wrongly provied please look at /var/logs/logs.csv file. \
                    and see website statistics for all verified websites",
        add_help=True,
    )
    subparser = parser.add_subparsers(title='subcommands',
                                      description='Subcommand to run url verification - not yet prepared',
                                      help='additional help'
                                      )
    # argument to provide input file
    parser.add_argument('-sf', '--sitesfile', nargs='?', required=True, help="Provide path to notepad file with url "
                                                                             "links in only txt extenstion")
    # argument to provide static url - not yet running
    # add_argument('-url', '--url_path', dest='url', type=str, help="enter full path to website")

    args = parser.parse_args()

    # verification if script run by root
    if not os.getuid() == 0:
        print("Script can run only by root")
        sys.exit(exit(0))
    else:
        with open(filesites, "r") as f:
            lines = [re.sub(r'.*//', '', line.rstrip('\n').replace(',', '')) for line in f]

        # run main functions
        create_dir(path_dir_stats)
        write_to_file(path_logs)
        read_csv_log(path_logs, path_all_statistics)
