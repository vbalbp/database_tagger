import requests
import json

from settings import API_TOKEN, DT_URL
from log_messages import DETECTED_DB_LOG, NO_CALLING_SERVICE_LOG


services_api = '/api/v2/entities'
tags_api = '/api/v2/tags'
services_parameters = '?entitySelector=type("SERVICE")'
tags_parameters = '?entitySelector=type("SERVICE")'

def call_dt_api(url):
	'''
	Params:
		url(string): Endpoint to be called with the requests library
	Return(dictionary): Already formatted and covnerted json of the answer of the request.

	Performas a single GET request on the specified URL which expects a Dynatrace API endpoint.
	'''
	request_answer = requests.get(url, headers = {'Authorization': 'Api-Token ' + API_TOKEN, 'Content-Type': 'application/json'})
	json_answer = json.loads(request_answer.text)
	return json_answer

print u"    .oyyyyyson+.           sh                               hs                                        \r\n .:yhhhhhhhhh/ oy.   .:HHHHhd /:     `/: .:HHH:.   :mHHHm.  dh//-  .mmmm. -mHHHm:   -HHHH.   .:HHHH:. \r\n:s.\u00B4\u00B4PPPPPPP nhhh`  od/----yd /m:    sd./d+:\u00B4\u00B4\\dy       :do dh    .ms`````     :do dy:\u00B4\u00B4\u00B4\u00B4  sd/\u00B4\u00B4\u00B4\u00B4\u00B4d+\r\nhhhh.       ohhhh- `m+     sd  om-  +m- hh     oN. -:mmm:ym dy    -N/    -:mmmm:ym N.       my:mmmdh* \r\nhhhh`       shhhh: `m+     sd   sd./m/  hh     oN-hh:    ym dy    -N/   .ds    -ms N.       my        \r\nhhy ::::::: yhhho`  od/---:dh   `hdm+   hh     oN-dh:    hh yd:-- -N/   .mo    :mo dy:----  sd:       \r\ns/ yhhhhhhh-hh+.     .:HHHH:`    -Ns    hh     oN``:HHHHH:` `:HHH:-N/    .HHHHHH:  `-HHHHH.   *HHHH*\u00B4 \r\n `.osyyhhhh+/*                   yy"

# Get all the services
services_json = call_dt_api(DT_URL + services_api + services_parameters)

for service_id in services_json['entities']:
	service_json = call_dt_api(DT_URL + services_api + '/' + service_id['entityId'])
	# Act only on Database services out of the list
	if service_json['properties']['serviceType'] == 'DATABASE_SERVICE':
		print DETECTED_DB_LOG.format(name=service_json['displayName'])
		if 'calls' not in service_json['toRelationships']:
			print NO_CALLING_SERVICE_LOG
		else:
			# Get every calling service
			calling_services = service_json['toRelationships']['calls']
			tags = set()
			for calling_service in calling_services:
				service_to_fetch_json = call_dt_api(DT_URL + services_api + '/' + calling_service['id'])
				# Fetch the tags of every service that calls the Database and group them
				for tag in service_to_fetch_json['tags']:
					tags_to_add = (tag['context'], tag['key'])
					tags.add(tags_to_add)
			payload = [ { 'value': (None if tag[0] == 'CONTEXTLESS' else tag[0]), 'key': tag[1] } for tag in tags ]
			data = {
				'tags': payload
			}
			# Apply every single tag at once
			add_tags = requests.post(DT_URL + tags_api + tags_parameters.format(id=service_id['entityId']), data = json.dumps(data), headers = {'Authorization': 'Api-Token ' + API_TOKEN, 'Content-Type': 'application/json'})
			if add_tags.status_code == 200:
				for tag in tags:
					print "Successfully added tag " + (tag[1] if tag[0] == 'CONTEXTLESS' else tag[0] + ': ' + tag[1]) + ' to database ' + service_json['displayName'] + ' (' + service_id['entityId'] + ')'
			else:
				print add_tags.text
