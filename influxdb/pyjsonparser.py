#! /usr/bin/env python3

#
# This codes comes via https://community.influxdata.com/u/Franky1 with the Influx data community. The
# message thread can be found at:
#   https://community.influxdata.com/t/telegraf-json-and-transformations/19013/3
#
# To use it, the telegraf.conf should look like:

#   [[inputs.http]]
#     urls = ["https://jsonblob.com/api/jsonBlob/4da2f61e-8a89-11eb-a428-a5fa7295f33b"]
#     method = "GET"
#     headers = {"Content-Type"="application/json", "Accept"="application/json"}
#     name_override = "http"
#     data_format = "json"
#     json_query = "link_info"
#     json_string_fields = ["*hostname", "*linkType", "*olsrInterface"]
#
#   [[processors.execd]]
#     namepass = ["http"]
#     command = ["python", "pyjsonparser.py"]
#
#   [[outputs.file]]  # only for debugging
#     files = ["link_info.out"]
#     influx_sort_fields = true

# This code needs a couple of modules before it can be used:

#   pip install influxdb-client
#   pip install line-protocol-parser


from influxdb_client import Point
from line_protocol_parser import parse_line

while True:
    try:
        input_line = input()  # read from stdin
    except EOFError:  # catch EOF error
        break
    else:
        data = parse_line(input_line)  # parse input line
        fields = data['fields']
        ips = dict()
        for key, value in fields.items():
            ipaddress, substring = key.split('_', 1)
            if ipaddress not in ips:
                ips[ipaddress] = dict()
            ips[ipaddress][substring] = value
        for key, value in ips.items():
            datapoint = dict()
            datapoint['measurement'] = data['measurement']
            datapoint['fields'] = value
            datapoint['tags'] = {'ip' : key}
            datapoint['time'] = data['time']
            point = Point.from_dict(datapoint)  # new metric object
            print(point.to_line_protocol())  # write to stdout
