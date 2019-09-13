#!/usr/bin/env python3
import socket
import urllib.request
import requests
import csv
from datetime import datetime
import os

filepath = "stats.csv"
result = []
sumator = []

path = os.path.join(os.path.expanduser('/'), 'var', 'log', 'stats', 'logs.csv')
path_statistics = os.path.join(os.path.expanduser('/'), 'var', 'log', 'stats', 'statistics.csv')


def request_site(url):
    status_code = urllib.request.urlopen(f"http://{url}").getcode()
    if status_code == 200:
        print(url + "Status Code 200")
        return status_code
    else:
        print(url + "Url is unreachable")
        return status_code


def isSSL_open(url, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((url, port))
        print("Connection open")
        return True
    except Exception:
        print("Port 443 is closed")
        return False


def check_certificate(url):
    try:
        requests.get(f"https://{url}")
        return ("SSL Certificate Valid")
    except Exception:
        return ('SSL Certificate invalid')


def generate_csv_stats(url):
    status_code = request_site(url)
    if status_code == 200:
        openSSL = isSSL_open(url, 443)
        if openSSL:
            cert = check_certificate(url)
        else:
            cert = None

    return {"url:": url, "status_code": status_code, "SSL open:": openSSL, "SSL Certificate:": cert,
            "Date_time: ": datetime.now()}


def write_to_file(filepath):
    with open(filepath, "a") as csvfile:
        records = [generate_csv_stats(url) for url in lines]
        print(requests)
        writer = csv.DictWriter(csvfile, fieldnames=records[0].keys())
        writer.writerows(records)


def create_dir(stats_dir):
    access_rights = 0o777
    try:
        os.mkdir(stats_dir, access_rights)
        print("Directory created")
    except:
        print("Directory exist")


def read_csv_log(path_logs, filepath):
    with open(path_logs) as file:
        csv_reader_object = list(csv.reader(file))
        for i in lines:
            counter = 0
            total = 0
            for row in csv_reader_object:
                if row[0] == i:
                    if row[1] == "200":
                        counter = counter + 1
                        total = total + 1
                    else:
                        print("Not accessible")

            count_percent = (counter * 100 / total)
            result.append(count_percent)
            sumator.append(total)

    with open(filepath, 'w') as myfile:
        wr = csv.writer(myfile)
        for i in zip(lines, result):
            wr.writerow(i)


if __name__ == '__main__':
    with open("/bin/sites.txt", "r") as f:
        lines = [line.rstrip('\n').replace(',','') for line in f]
        print(lines)

    create_dir("/var/log/stats")
    write_to_file(path)
    getline = read_csv_log("/var/log/stats/logs.csv", path_statistics)
