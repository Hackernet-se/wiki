---
title: Cisco TCLSH
permalink: /Cisco_TCLSH/
---

Cisco IOS Tcl shell designades för att kunna köra tcl-kommandon direkt i
IOS. Man kan köra script i detta skal.

`#tclsh`

Ping sweeps
-----------

Flera hostar

`foreach ip {`
`192.168.0.5`
`192.168.0.6`
`8.8.8.8} {`
`ping $ip repeat 2 timeout 1 }`

Ett subnät

`for {set i 1} {$i < 255} {incr i} { `
`ping 192.168.0.$i re 2 ti 0`

Flera subnät

`foreach subnet {`
`14`
`15`
`100 } {`
`for {set i 1} {$i < 255} {incr i} {`
`ping 172.0.$subnet.$i re 2 ti 0`
`}`
`}`

[Category:Cisco](/Category:Cisco "wikilink")