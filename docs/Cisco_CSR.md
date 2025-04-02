---
title: Cisco CSR
permalink: /Cisco_CSR/
---

Cisco Cloud Services Router 1000V är en mjukvarurouter. CSR har DPDK
integrerat i dataplane och kör [IOS-XE](/Cisco_IOS "wikilink"), samma OS
som ASR 1000. Unlicensed Cisco IOS XE 3.13S och senare har en throughput
begränsad till 100 kbps (**show platform hardware throughput level**).

Installation
------------

Ladda ned mjukvaran från Ciscos hemsida,
[download](https://software.cisco.com/download/type.html?mdfid=284364978&flowid=39582)

-   **[VMware ESXi](/VMware_ESXi "wikilink"):** Deploy OVF template.

<!-- -->

-   **[KVM](/KVM "wikilink"):** Qemu image (.qcow2) finns att ladda ner
    direkt.

**Licens**
Ladda ner licens från cisco (http:/www.cisco.com/go/license) och lägg in
på bootflash på enheten. Det finns 60 dagars eval-licens.

`license install bootflash:lic25ax.lic`
`show license detail`

Konfiguration
-------------

Här listas CSR-specifik info, för övrig konfiguration se [Cisco
IOS](/Cisco_IOS "wikilink").

Nyare CSR har ett modernt webbgränssnitt som man kan använda för att
managera och monitorera enheten.

`ip http server`
[`http://10.0.10.1/webui/`](http://10.0.10.1/webui/)

### Resurser

**CPU**
Show processes inside the IOS daemon.

`show processes cpu sorted`

Show processes for the underlying operating system.

`show processes cpu platform sorted`

Increase the control-plane CPU

`platform resource control-plane-heavy`

**Memory**

`show memory platform`

Increase the Cisco IOS XE memory

`platform memory add 3286`

**NIC**

`show platform software vnic-if interface-mapping`

### Uppgradering

För att uppgradera en CSR laddar man ner nyare bin-fil och lägger på
local storage.

`copy `[`http://`](http://)*`fileserver`*`/csr1000v-universalk9.03.16.04b.S.155-3.S4b-ext.SPA.bin bootflash:`
`verify bootflash:csr1000v-universalk9.03.16.04b.S.155-3.S4b-ext.SPA.bin`

`boot system flash bootflash:csr1000v-universalk9.03.16.04b.S.155-3.S4b-ext.SPA.bin`
`show bootvar`
`reload`

REST API
--------

Standard port for IOS XE REST API: 55443

`virtual-service csr_mgmt`
` ip shared host-interface GigabitEthernet1`
` activate`

Verify

`show virtual-service`
`show virtual-service detail | i API`
`show remote-management status`

**URL-exempel**
{\| class="wikitable" ! URL \|\| Method \|- \|
/api/v1/global/running-config \|\| GET \|- \| /api/v1/global/save-config
\|\| PUT \|- \| /api/v1/global/cli \|\| PUT \|- \| /api/v1/vrf \|\| GET
\|- \| /api/v1/routing-svc/bgp/100/neighbors \|\| GET \|}

**CURL**
curl -X POST <https://10.0.10.1:55443/api/v1/auth/token-services> -H
"Accept:application/json" -u "cisco:cisco" --insecure

`curl -X GET `[`https://10.0.10.1:55443/api/v1/interfaces`](https://10.0.10.1:55443/api/v1/interfaces)` -H "X-auth-token:+gcg41pecdAvyeBPGmvOPN4yfLIZ55D+sdYPJKPzlT8=" --insecure`

Tokens automatically expire after 15 minutes.

### NETCONF

Legacy NETCONF, port 22.

`netconf ssh`

Enable NETCONF/YANG support, port 830.

`netconf-yang`

Discover capabilities

`from ncclient import manager`
`m = manager.connect(host='192.168.1.21', port=830, username='cisco',`
`                   password='cisco', device_params={'name': 'CSR'})`
`print m.server_capabilities`

Hypervisor
----------

IOS-XE har numera stöd för att själv köra virtuella maskiner, dvs agera
hypervisor. Om man kör på en CSR glöm ej Hardware Assisted
Virtualization.

Förberedelser, lägga in OVA på routerns lokala storage samt:

`virtual-service`
` signing level unsigned`

Installera paket

`virtual-service install name Fedora package bootflash:Fedora.ova`
`show virtual-service list`

För att ge VM:en konnektivitet med outside world skapar man en Virtual
Port Group.

`int virtualportGroup 1`
` ip add 10.0.10.1 255.255.255.0`

Starta VM

`activate`

Anslut till console på VM

`virtual-service connect name Fedora console`

Aktivera shell

`guestshell enable`

[Category:Cisco](/Category:Cisco "wikilink")