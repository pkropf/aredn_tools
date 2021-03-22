#! /usr/bin/env python3

#
# transform influxdb line protocol data from:
#
#   http,host=data,url=http://omni-m5.sfwem/cgi-bin/sysinfo.json?link_info\=1 link_info_10.88.42.36_signal=-81,link_info_10.88.42.36_tx_rate=21.7,link_info_10.111.157.186_neighborLinkQuality=1,link_info_10.88.42.36_noise=-95,sysinfo_loads_1=0.39,sysinfo_loads_2=0.45,link_info_10.111.157.186_linkQuality=1,link_info_10.88.42.36_rx_rate=14.4,link_info_10.88.42.36_linkQuality=1,sysinfo_loads_0=0.27,link_info_10.88.42.36_neighborLinkQuality=0.765 1616379411000000000
#
# to:
#
#   http,host=data,url=http://omni-m5.sfwem/cgi-bin/sysinfo.json?link_info\=1 sysinfo_loads_0=0.27,sysinfo_loads_1=0.39,sysinfo_loads_2=0.45 1616379411000000000
#   http,host=data,link_IP=10.88.42.36,url=http://omni-m5.sfwem/cgi-bin/sysinfo.json?link_info\=1 link_info_linkQuality=1,link_info_neighborLinkQuality=0.765,link_info_noise=-95,link_info_rx_rate=14.4,link_info_signal=-81,link_info_tx_rate=21.7 1616379411000000000
#   http,host=data,link_IP=10.111.157.186,url=http://omni-m5.sfwem/cgi-bin/sysinfo.json?link_info\=1 link_info_linkQuality=1,link_info_neighborLinkQuality=1 1616379411000000000
#

from influxdb_client import Point
from line_protocol_parser import parse_line

while True:
    try:
        input_line = input()  # read from stdin
    except EOFError:  # catch EOF error
        break
    else:
        data = parse_line(input_line)  # parse input line
        tags = data['tags']
        fields = data['fields']
        new_fields = {}
        other_fields = {}
        ips = {}
        for key, value in fields.items():
            if 'link_info_' in key:
                ip = key.split('_')[2]
                if ip not in ips:
                    ips[ip] = {}
                ips[ip]['link_info%s' % key.split(ip)[1]] = value
            else:
                other_fields[key] = value


        # for each set of link_info_IPADDRESS_* found, create and print an influx
        # line protocol for the values
        for ip in ips:
            tags['link_IP'] = ip
            datapoint = {'measurement': data['measurement'],
                         'fields': ips[ip],
                         'tags': tags,
                         'time': data['time']
            }
            point = Point.from_dict(datapoint)  # new metric object
            print(point.to_line_protocol())  # write to stdout

            # count the number of linkType entries to be included with the other data
            if 'link_info_linkType' in ips[ip]:
                count_link_type = 'count_linkType_' + ips[ip]['link_info_linkType']
                if count_link_type not in other_fields:
                    other_fields[count_link_type] = 0
                other_fields[count_link_type] += 1

        # create and print an influx line protocol for any non-link_info fields
        datapoint = {'measurement': data['measurement'],
                     'fields': other_fields,
                     'tags': tags,
                     'time': data['time']
        }
        point = Point.from_dict(datapoint)  # new metric object
        print(point.to_line_protocol())  # write to stdout
