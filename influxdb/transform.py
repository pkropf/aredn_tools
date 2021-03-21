#! /usr/bin/env python3

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
