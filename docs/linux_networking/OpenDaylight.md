---
title: OpenDaylight
permalink: /OpenDaylight/
---

OpenDaylight är en öppen kontroller-infrastruktur byggd för
SDN-implementeringar.

Installation
------------

Ladda ner senaste version: <https://www.opendaylight.org/downloads>

`wget `[`https://nexus.opendaylight.org/content/repo`](https://nexus.opendaylight.org/content/repo)`...-SR1.tar.gz`

*Beryllium on Ubuntu*

`sudo apt-get -y install openjdk-7-jdk`
`cd && echo "export JAVA_HOME=/usr/lib/jvm/java-1.7.0-openjdk-amd64" >> .profile`
`tar -xzf distribution-karaf-0.4.1-Beryllium-SR1.tar.gz`

Stäng av ipv6, java har ipv6 som preferred.

Konfiguration
-------------

Starta OpenDaylight

`cd ./distribution-karaf-[TAB]`
`bin/karaf   #starta med karaf console`
`bin/start   #starta i bakgrund`
`bin/stop    #stoppa controller`

Från början är ODL tomt så man får ladda in de features man vill
använda. En feature installeras en gång sedan är den aktiverad även
efter omstart. Lista tillgängliga features och installera några basic:

`feature:list`
`feature:install odl-restconf odl-l2switch-switch odl-dlux-all`
`feature:list --installed`

OpenFlow

`feature:install odl-openflowplugin-flow-services-ui`

DLUX web gui, admin pw: admin

[`http://`](http://)<ip>`:8181/index.html`

*Unable to login* Det tar några minuter innan man kan logga in.

Network
-------

ODL kan prata med nätverksutrustning med många olika protokoll, t.ex.
OpenFlow, NETCONF, BGP och OVSDB. Se [Mininet](/Mininet "wikilink").
För [Open_vSwitch](/Open_vSwitch "wikilink"):

`ovs-vsctl set-controller br0 tcp:10.0.0.20:6633`

[Category:Network](/Category:Network "wikilink")