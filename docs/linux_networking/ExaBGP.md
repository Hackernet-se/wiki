---
title: ExaBGP
permalink: /ExaBGP/
---

ExaBGP är en BGP route announcer som det går att scripta mot. Se även
[Cisco BGP](/Cisco_BGP "wikilink") och [Arista
BGP](/Arista_BGP "wikilink").

Installation
============

`pip install exabgp`

Konfiguration
=============

Exempel där man kan skicka in väldigt mycket routes till BGP.

Script för att generera prefix:
[bs-prefixes.py](http://www.blackhole-networks.com/OSPF_overload/bs-prefixes.py)

`chmod +x bs-prefixes.py`

Script för att annonsera prefix

`touch announce.sh && chmod +x announce.sh`

cat announce.sh

``` bash
#!/bin/sh

# ignore Control C
# if the user ^C exabgp we will get that signal too, ignore it and let exabgp send us a SIGTERM
TEMPFILE=/tmp/prefixes.bgp
PREFIXES=50000
BLOCK=128

trap '' SIGINT

# Dump our prefixs in a file for parsing a block at a time
/path/to/bs-prefixes.py $PREFIXES > $TEMPFILE

# Pause a bit to let BGP sessions come up
sleep 10

LINE=0
while [ $LINE -lt $PREFIXES ]; do
   LINE=$(( $LINE + $BLOCK ))
   for pfx in `head -n $LINE $TEMPFILE | tail -n $BLOCK`; do
      echo "announce route $pfx next-hop 10.0.0.0"
   done
   sleep 2
done
```

Konfigurationsfil för exaBGP, edit *exabgp.conf*

`neighbor 10.0.0.11 {`
` description "R2";`
` router-id 66.66.66.66;`
` local-address 10.0.0.10;`
` local-as 666;`
` peer-as 101;`
` hold-time 600;`
` graceful-restart;`

`  # advertise prefixes`
`  process service-1 {`
`       run /path/to/announce.sh;`
`  }`

Kör

`exabgp exabgp.conf`

Segment Routing
---------------

ExaBGP kan användas för att skicka in segment-lista dvs göra traffic
engineering. ExaBGP kan också parsea IS-IS segment routing extensions
genom BGP-LS. Detta betyder att man kan ta emot segment identifiers
(node och adjacency id:s) genom samma BGP-LS session. Med
label-informationen kan man programera LSP:er via BGP-LU sessionen till
PE. Se även [Arista SR](/Arista_SR "wikilink") och [Cisco
SR](/Cisco_SR "wikilink").

cat ./config/exabgp

`neighbor 172.16.0.20 { `
`   group-updates true; `
`   local-address 172.16.0.10; `
`   peer-as 65000; `
`   local-as 65000; `
`   family { `
`      ipv4 nlri-mpls;`
`   }`
`   static {`
`      route 10.1.1.15/32 {  `
`         next-hop 10.0.0.2;  `
`         label [ 800005 800007 800006 800008 ];`
`      }`
`      route 10.1.1.15/32 {          #egress PE loopback`
`         next-hop 10.0.0.3;         #physical next-hop in core to get towards egress PE`
`         label [ 800005 800006 800008 ];`
`      }`
`   }`
`}`

[Category:Network](/Category:Network "wikilink")