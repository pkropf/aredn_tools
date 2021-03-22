#! /usr/bin/env python3
#
# This is the wrong direction to use with Telegraf but would work with additional code as a standalone
# scrapper and processor of the JSON obtained via an HTTP GET call.


import json
import sys


def link_info(j):
    new_info = []
    for section in j:
        if section == 'link_info':
            for ip in j['link_info']:
                info = {'IPAddress': ip}
                for field in j['link_info'][ip]:
                    info[field] = j['link_info'][ip][field]
                new_info.append(info)
    j['link_info'] = new_info
    return j


if __name__ == '__main__':
    j = json.loads(sys.stdin.read())
    print(link_info(j))
