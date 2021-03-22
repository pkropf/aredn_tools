# aredn_tools - influxdb
Parse the json result of a call to http://NODE/cgi-bin/sysinfo.json?link_info=1 and write the information out to an influxdb instance.

Normally, the JSON parser would be used with the HTTP Telegraf plugin to process the JSON from a web server and send the results to the influxdb. However, the format of the link_info portion of the JSON from the Aredn sysinfo.json call is formated such that processing it results in data being written that's difficult to process with tools like Grafana. The issue is that the JSON sets up the data for each node with the IP address of the node as a key to the details. Telegraf processes this just fine but the tags and fields that are written make graphing difficult.

Here's an example link_info section:

```
    "link_info": {
	"10.88.42.36": {
	    "neighborLinkQuality": 0.71699999999999997,
	    "noise": -95,
	    "linkQuality": 1,
	    "linkType": "RF",
	    "hostname": "KJ6WEG-OAK-Griz-SectorM5.local.mesh",
	    "tx_rate": 19.5,
	    "olsrInterface": "wlan0",
	    "rx_rate": 19.5,
	    "signal": -81
	},
	"10.111.157.186": {
	    "neighborLinkQuality": 1,
	    "linkQuality": 1,
	    "hostname": "KK6RUH-Oakland-Nanobeam-M5.local.mesh",
	    "olsrInterface": "eth0.2",
	    "linkType": "DTD"
	}
    },
```

The linkQuality values are written into two fields called link_info_10.100.98.190_linkQuality and link_info_10.111.157.186_linkQuality. As time goes on and different nodes connect and disconnect, these field keys will keep increasing. Since they're separate fields, it's difficult to build dashboards within tools like Grafana that can automatically change as the connected nodes change. You would have to build a new dashboard each time a new node connects. In a mesh network, this can happen on a regular basis. It would be better if the like fields from the different nodes were written to fields with the same names. Like link_info_linkQuality and link_info_tx_rate, etc.

This issue could be resolved if the resulting link_info JSON section instead used arrays

```
    "link_info": [
        {"IPAddress": "10.88.42.36",
         "neighborLinkQuality": 0.71699999999999997,
         "noise": -95,
         "linkQuality": 1,
         "linkType": "RF",
         "hostname": "KJ6WEG-OAK-Griz-SectorM5.local.mesh",
         "tx_rate": 19.5,
         "olsrInterface": "wlan0",
         "rx_rate": 19.5,
         "signal": -81
        },
        {"IPAddress": "10.111.157.186",
         "neighborLinkQuality": 1,
         "linkQuality": 1,
         "hostname": "KK6RUH-Oakland-Nanobeam-M5.local.mesh",
         "olsrInterface": "eth0.2",
         "linkType": "DTD"
	    }
    },
```

Unfortunately I'm unable to fathom how to configure the JSON Telegraf plugin to make this transformation so here we are with some Python code to do the work for us.

Update: 
[Franky1](https://community.influxdata.com/u/Franky1) with the Influx data community offered a solution using the Telegraf execd plugin. See the [message thread](https://community.influxdata.com/t/telegraf-json-and-transformations/19013/3) for more details. Example code he created is in pyjsonparser.py.
