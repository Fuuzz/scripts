#!/bin/env python

import sys,requests,re

#only for debug
import json,datetime,logging

# Token  Produzione
token = ""

metaip = sys.argv[1]
notificationtype = sys.argv[2]
hostname = sys.argv[3]
hostaddress = sys.argv[4]
servicedesc = sys.argv[5]
state = sys.argv[6]
output = sys.argv[7]
shortdatetime = sys.argv[8]
hg_list = sys.argv[9]

# The hostgroups list for which notifications must be sent to metamonitor
tonotify_list = {"BackBone","AS"}

# metamonitor url and headers
url = "http://" + metaip + "/centreon/api/events/"
headers = { 'Authorization': 'Token ' + token }

# Splits the elements in a list and then convert in a set for better matching
hg_list = (hg_list.split(','))
hg_list = set(hg_list)

tonotify_list = set(tonotify_list)

# Check at least one match in common between host groups of the host and the ones for which the notification needs to be sent
if not set.intersection(hg_list, tonotify_list):
  print('No group match')
  exit()

# Save the matching hostgroup in a variable, trim all unneeded characters
hostgroup_raw = list(set.intersection(hg_list, tonotify_list))

#print(hostgroup_raw)

hostgroup = re.sub("['\[\]]","", str(hostgroup_raw))

#print(hostgroup)

# Build the json payload
payload = {
    "notificationtype": notificationtype,
    "hostname": hostname,
    "hostaddress": hostaddress,
    "servicedesc": servicedesc,
    "state": state,
    "output": output + " | Ambito : " + hostgroup,
    "shortdatetime": shortdatetime,
    "ambito": hostgroup,
}

print(payload)
response = requests.post(url, headers=headers, json=payload)

# For debug
#print(response.text)
#print("Status Code", response.status_code)
#print("JSON Response ", response.json())

# DEBUG - Writing log of notification

log_file_name = "/var/log/centreon-engine/metamonitor_notification-log-" + datetime.datetime.today().strftime("%Y%m%d")
logging.basicConfig(filename = log_file_name, level = logging.DEBUG, format = '%(asctime)s %(message)s', datefmt = '%Y%m%d-%H%M%S')
logging.debug("PAYLOAD: " + str(payload) + "," + " RESPONSE: " + str(response.status_code))
