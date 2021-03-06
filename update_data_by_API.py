#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import urllib2
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(base_dir)

def read_json(file_name):
    with open(file_name, 'r') as input_file:
        return json.load(input_file)

def write_json(file_name, content):
    with open(file_name, 'w') as output_file:
        json.dump(content, output_file, indent=4)

api = 'http://127.0.0.1:10080/'
api_today = 'http://127.0.0.1:10080/today'

data = read_json('data/data.json')

response = urllib2.urlopen(api);
try:
    new_data = json.loads(response.read())
except e:
    print e
    sys.exit(1)

for name, reservoir in data.iteritems():
    for reservoir_new in new_data['data']:
        if name == reservoir_new['reservoirName']:
            print name, reservoir['id']
            reservoir['name'] = reservoir_new['reservoirName']
            reservoir['daliyInflow'] = reservoir_new['daliyInflow']
            reservoir['daliyOverflow'] = reservoir_new['daliyOverflow']
            reservoir['baseAvailable'] = reservoir_new['baseAvailable'].replace(',', '')
            try:
                reservoir['daliyNetflow'] = float(reservoir_new['daliyOverflow']) -\
                        float(reservoir_new['daliyInflow'])
            except:
                print 'daliyflow currently not updated'
                #reservoir['daliyInflow'] = None

response = urllib2.urlopen(api_today);
try:
    new_data = json.loads(response.read())
except e:
    print e
    sys.exit(1)

for name, reservoir in data.iteritems():
    for reservoir_new in new_data['data']:
        if name == reservoir_new['reservoirName']:
            print name, reservoir['id'], reservoir_new['immediateTime']
            reservoir['updateAt'] = reservoir_new['immediateTime']
            reservoir['percentage'] = reservoir_new['immediatePercentage'][:-2]
            reservoir['volumn'] = reservoir_new['immediateStorage']

write_json('data/data.json', data)
