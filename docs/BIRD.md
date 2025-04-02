---
title: BIRD
permalink: /BIRD/
---

Bird Internet Routing Daemon. Senaste version: 1.5.0 (22.4.2015)

Installation
============

`sudo apt-get update && sudo apt-get install bird `
`sudo dnf install bird`

Konfiguration
=============

**Ubuntu**

Enable IPv4 and IPv6 Forwarding:

`echo "net.ipv4.conf.all.forwarding=1" | sudo tee -a /etc/sysctl.conf `
`echo "net.ipv4.conf.default.forwarding=1" | sudo tee -a /etc/sysctl.conf `
`sed 's/#net.ipv6.conf.all.forwarding=1/net.ipv6.conf.all.forwarding=1/g' /etc/sysctl.conf | sudo tee /etc/sysctl.conf `
`echo "net.ipv6.conf.default.forwarding=1" | sudo tee -a /etc/sysctl.conf `
`sudo sysctl -p `

Backup the configuration files:

`sudo cp /etc/bird/bird.conf /etc/bird/bird.conf.original `
`sudo cp /etc/bird/bird6.conf /etc/bird/bird6.conf.original `

Create the configuration files:

`sudo nano /etc/bird/bird.conf `
`sudo nano /etc/bird/bird6.conf `

Restart the daemons:

`sudo service bird restart `
`sudo service bird6 restart `

**Fedora**

Backup

`sudo cp /etc/bird.conf /etc/bird.conf.original`

Edit

`sudo nano /etc/bird.conf`

Restart

`sudo systemctl restart bird`

CLI
---

Gå till cli

`sudo birdc`
`bird> show route`

Quit

`bird> exit`

OSPF
----

`show ospf interface `
`show ospf neighbors `
`show ospf state `
`show ospf topology`

BGP
---

`protocol bgp {`
`#       disabled;`
`        description "My BGP uplink";`
`        local as 65002;`
`        neighbor 172.22.0.90 as 65000;`
`#       multihop;`
`        hold time 240;`
`        startup hold time 240;`
`        connect retry time 120;`
`        keepalive time 80;      # defaults to hold time / 3`
`        start delay time 5;     # How long do we wait before initial connect`
`        error wait time 60, 300;# Minimum and maximum time we wait after an error (when consecutive`
`        error forget time 300;  # ... until this timeout expires)`
`        path metric 1;          # Prefer routes with shorter paths (like Cisco does)`
`        default bgp_med 0;      # MED value we use for comparison when none is defined`
`        default bgp_local_pref 0;       # The same for local preference`
`        source address 172.22.0.19;     # What local address we use for the TCP connection`
`#       password "secret";      # Password used for MD5 authentication`
`}`

Birdc

`show protocols all bgp1`

[Category:Network](/Category:Network "wikilink")