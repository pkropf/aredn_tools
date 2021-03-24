# aredn_tools
Tools to work in devices running on an Aredn Mesh

The [telegraf](telegraf/readme.md) folder contains the first work to push the json data read from nodes into an Influx database. It's working though it'll most likely be abandoned since there's no easy to have Telegraf follow the links of the mesh network and pull data from all the nodes.

The [nodewalker](nodewalker/) contains the second attempt at pulling all the json data from the nodes in an Aredn mesh network.

