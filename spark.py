#!/bin/env python

import sys,requests,re

#only for debug
import json,datetime,logging

# API Key Test
key = ""

# Address Test
address = ""

hostname = sys.argv[1]
hostaddress = sys.argv[2]
servicedesc = sys.argv[3]
state = sys.argv[4]
output = sys.argv[5]

# Headers
headers = {
    'accept': 'application/json',
    'content-type': 'application/x-www-form-urlencoded'
}

# Proxies
proxies = {
    'http': 'http://user:pass@domain:8080',
    'https': 'http://user:pass@domain:8080'
}

# Buil monitored item
if servicedesc:
        monitored_item = servicedesc + " service of " + hostname
else:
        monitored_item= hostname + " with IP " +hostaddress

# Build the json payload
payload = {
   "monitored_item": monitored_item,
   "alert_summary": state,
   "detailed_description": output,
   "apikey": key,
   "monitoring_system": "NAGIOSXI"
}

print(payload)

request = requests.post(address,headers=headers,json=payload,proxies=proxies)

# For debug
#print(request.text)
#print("Status Code", request.status_code)
#print("JSON Response ", request.json())

# DEBUG - Writing log of notification
log_file_name = "/var/log/spark_notification-log-" + datetime.datetime.today().strftime("%Y%m%d")
logging.basicConfig(filename = log_file_name, level = logging.DEBUG, format = '%(asctime)s %(message)s', datefmt = '%Y%m%d-%H%M%S')
logging.debug("PAYLOAD: " + str(payload) + ", RESPONSE: " + str(request.status_code) + ", TOKEN: " + request.text)
