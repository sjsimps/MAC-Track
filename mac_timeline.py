import csv
import matplotlib.pyplot as plt
import sys
import os

from operator import itemgetter
from collections import defaultdict

def plot_timeline(dataset, **kwargs):
    colors  = kwargs.pop('colors', {})
    name  = kwargs.pop('name', {})
    series  = set([])

    # Bring the data into memory and sort
    dataset = sorted(list(dataset), key=itemgetter(0))

    # Make a first pass over the data to determine number of series, etc.
    for _, source, category in dataset:
        series.add(source)
        if category not in colors:
            colors[category] = 'k'

    # Sort and index the series
    series  = sorted(list(series))

    x = []
    y = []
    c = []
    for timestamp, source, category in dataset:
        x.append(timestamp)
        y.append(series.index(source))
        c.append(colors[category])

    plt.figure(figsize=(14,4))
    plt.title(kwargs.get('title', "Device Network Access Timeline : {}".format(name)))
    plt.ylim((-1,len(series)))
    plt.xlim((0, 86400))
    plt.yticks(range(len(series)), series)
    plt.scatter(x, y, color=c, alpha=0.85, s=10)

    print "MAC ADDRESS       | MANUFACTURER"
    print "------------------|------------------------------------------------"
    for s in reversed(series):
        print "{} | {}".format(s,query_oui(s))

    return plt

def get_oui_database():
    oui_file = "oui_database.txt"
    if not (os.path.exists(oui_file) and os.path.isfile(oui_file)):
        unformatted = "oui_database_unformatted.txt"
        url = "http://standards-oui.ieee.org/oui.txt"
        command = "curl " + url + " > " + unformatted
        os.system(command)
        lines = tuple(open(unformatted, 'r'))
        f = open(oui_file,'a')
        for line in lines:
            br1 = line.find('(')
            br2 = line.find(')')
            if br1 > 0 and br2 > 0:
                line = [line[:br1], line[br1+1:br2], line[br2+1:]]
            if len(line) == 3 and line[1] == "hex":
                mac = line[0].strip() 
                info = line[2].strip() 
                f.write("{}|{}\n".format(mac,info))
        f.close()

def query_oui(mac_address):
    oui_file = "oui_database.txt"
    mac = mac_address.split(':')
    mac = mac[0] + '-' + mac[1] + '-' + mac[2]
    with open(oui_file, 'r') as f:
        for line in f:
            (search_mac, info) = line.split('|')
            if mac == search_mac:
                return info.strip()


if __name__ == '__main__':
    get_oui_database()
    colors = {'red': 'r', 'blue': 'b', 'green': 'g'}
    with open(sys.argv[1], 'r') as f:
        reader = csv.reader(f)
        plt = plot_timeline([
            (float(row[0]), row[1], row[2])
            for row in reader
        ], colors=colors
        , name=sys.argv[1])
        plt.show()
