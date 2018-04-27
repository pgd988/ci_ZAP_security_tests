#!/usr/bin/python
import sys
import time
import datetime
import json
from zapv2 import ZAPv2
from elasticsearch import Elasticsearch

ZAP_server='server IP here'

input_target = sys.argv[1]
#API_Key = 'tfbgmu72ds3k9rf84murtu96s'
API_Key = None

zap = ZAPv2(apikey=API_Key, proxies={'http': 'http://ZAP_server:8090', 'https': 'http://ZAP_server:8090'})
zap.urlopen(input_target)
time.sleep(3)

print 'Spidering target %s' % input_target
scanid = zap.spider.scan(input_target)
#print 'ZAP_KEY is %s' % API_Key
print 'Scanid is: %s' % scanid
# Give the Spider a chance to start
time.sleep(5)
while (int(zap.spider.status(scanid)) < 100):
    print 'Spider progress %s%%' % zap.spider.status(scanid)
    time.sleep(5)

print 'Spider completed'
time.sleep(5)

print 'Running active scan on target %s' % input_target
scanid = zap.ascan.scan(input_target, apikey = API_Key)

while(int(zap.ascan.status(scanid)) < 100):
    print 'Active scan progress %s%%' % zap.ascan.status(scanid)
    time.sleep(5)

print 'Scan completed'

scanjson = {}
scanjson["zapscanid"] = scanid
scanjson["date"] = str(datetime.datetime.now())
scanjson["url"] = input_target
scanjson["alerts"] = zap.core.alerts()

es = Elasticsearch(['http://ZAP_server:9200'])
es.index(index='scans', doc_type='scan',  body=json.dumps(scanjson))

json_string = json.dumps(scanjson)
parsed_string = json.loads(json_string)

#alerts_list = parsed_string['alerts']

Med_count = 0
Low_count = 0
High_count = 0
Critical_count = 0

for i in parsed_string['alerts']:

    if i["risk"] == 'Medium':
	Med_count=Med_count+1
    else:
	Med_count=Med_count

    if i["risk"] == 'Low':
	Low_count=Low_count+1
    else:
	Low_count=Low_count

    if i["risk"] == 'High':
	High_count=High_count+1
    else:
	High_count=High_count

    if i["risk"] == 'Critical':
	Critical_count=Critical_count+1
    else:
	Critical_count=Critical_count

#    print ( i["risk"])
#print ('Alerts counts: Medium=%s Low=%s High=%s Critical=%s') % (Med_count,Low_count,High_count,Critical_count)
if Critical_count > 1:

    print ('SECURITY TESTS IS FAILED WITH %s Critical alerts! Please see the Report') % (Critical_count)

elif High_count > 1:

    print ('SECURITY TESTS IS FAILED WITH %s HIGH ALERTS! Please see the Report') % (High_count)

else:

    if Med_count > 1:

	print ('TEST PASSED WITH %s MEDIUM SECURITY ALERTS') % (Med_count)

    elif Low_count > 1:

	print ('TEST PASSED WITH %s Low SECURITY ALERTS') % (Low_count)

    else:
	print ' TESTS PASSED WITHOUT ALERTS! ALL IS FINE :)'


#print "Finished!"
