---
title: Cisco ACI
permalink: /Cisco_ACI/
---

Cisco aci är en av Ciscos senaste innovationer inom hur man bygger
datacenter och är egentligen ett orkestreringsverktyg för Nexus serien
men inte med IOS utan APIC mjukvara i grunden på switcharna. Det är ett
software defined network där man från en kontroller kan man då styra
sitt fabric och integrera andra system med det för att göra automation
mot sitt datacenter nedan är några exempel på hur ACI fungerar. ACI står
för Application Centric Infrastructure men man är inte tvingad att köra
just applikationer utan det kan vara annat som exempel l2 eller l3
integrationer internt i fabricen eller göra integrationer externa också
mot både nät och applikationsresurser.

Datacenter Design
-----------------

Det finns garanterat annan dokumentation på design av hur man bör bygga
datacenter baserat på olika leverantörer eller preferenser men här
beskriver vi grundläggande hur designen ser ut med spine och leaf
uppsättning och vad som är viktigt att tänka på när man bygger och
integrerar sina system.
<https://hackernet.se/images/0/08/ACI-Fabric_layers.png>

**Spine**
Spine kallas de Nexus switchar som sitter på toppen av de andra fabric
switcharna för att tänket man skall ha är att alla Leaf switchar skall
alltid kopplas till alla spines för att få redundans och funktion genom
hela fabricen.
**Leaf**
Leaf är de switcharna som kopplas in till faktiska resurser så som
upklinks till spines och downlinks mot antingen UCS enheter "bare metal"
servrar alternativt annan nätverksutrustning om peering sker utanför
ditt fabric eller om man kör med en annan leverantör för brandväggs
leverans.
**Apic**
**Stretch Fabric**
**Multi-POD**

Mjukvara
--------

Mjukvaran i aci är ett eget typ av operativ för just Apicen som har
möjlighet att styra de olika fabric enheterna.
**APIC**
**Nexus**

Hårdvara
--------

Hårvaran har utvecklats med tiden för att ha stöd för tyngre och större
fabrics med mer resurser.
**Generationer**
**Asic**
**Begränsningar**

Integration
-----------

**UCS**
**Vmware**

Troubleshooting
---------------

On apic:

`#apic`
`acidiag verifyapic`
`cat /data/data_admin/sam_exported.config`
`cat /proc/net/bonding/bond0`
`moquery -c ipv4Addr | grep 100.64.0.20`

`#fabric`
`show versions`
`show switch`
`show endpoints vlan 100`
`show vpc map`
`show oob-mgmt`
`show firmware upgrade status`
`show stats granularity 15min leaf 101 interface ethernet 1/5`
`show epg EPG1 detail`
`show interface bridge-domain BD1 detail`
`show acllog permit l3 flow tenant Tenant1 vrf vrf1 `

On leaf:

`show vlan extended`
`iping -V Tenant1:vrf1 20.0.0.1 -S 10.0.0.1`
`show system internal epm vlan 100`
`show port-channel extended`
`show endpoint vrf Tenant1:vrf1`
`show bgp sessions vrf TEST:L3VRF`
`show bgp vpnv4 unicast vrf TEST:L3VRF`
`show bgp vpnv4 unicast 10.0.101.1/32 vrf TEST:L3VRF`
`show interface | grep -E "Ethernet1|MTU"`
`show isis dteps vrf overlay-1`
`vsh_lc -c "show system internal epm endpoint ip 10.12.2.11"`
`vsh_lc -c "show system internal epm endpoint mac 00:50:56:8A:20:00"`
`vsh_lc -c "show system internal epm vrf TEST:L3VRF detail"`

DHCP Relay

`show ip dhcp relay`
`show dhcp internal info relay address interface vlan XX`
`show dhcp internal info relay discover`
`show dhcp internal errors`
`show dhcp internal event-history traces`

APIC API
--------

**python**

``` Python
import requests
import os

username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')
hostname = 'apic1.hackernet.se'

# Build payload with userid/password and create a session object
payload = {"aaaUser": {"attributes": {"name": username, "pwd" : password }}}
session = requests.session()

# Issue the login request. The cookie will be stored in session.cookies.
login_url = f'https://{hostname}/api/aaaLogin.json'
response = session.post(login_url, json=payload, verify=False)

# Use the session object to get ACI objects
if response.ok:
    response = session.get(f'https://{hostname}/api/node/class/fvTenant.json', verify=False)
else:
    print(f"HTTP Error {response.status_code}:{response.reason} occurred.")
```

**curl**
Login and save to COOKIE

`curl -s -k -d "`<aaaUser name=admin pwd=password/>`" -c COOKIE -X POST `[`https://10.0.0.11/api/mo/aaaLogin.xml`](https://10.0.0.11/api/mo/aaaLogin.xml)

Get tenants xml

`curl -s -k -X GET `[`https://10.0.0.11/api/node/class/fvTenant.xml`](https://10.0.0.11/api/node/class/fvTenant.xml)` -b COOKIE | xmllint --format -`

Post xml from file

`curl -s -k -X POST -d @xml2aci.xml `[`https://10.0.0.11/api/mo/uni.xml`](https://10.0.0.11/api/mo/uni.xml)` -b COOKIE`

==Default Authentication Domain != Local== Om man har t.ex. radius eller
tacacs som default authentication realm men vill ändå kunna logga in med
lokala konton så måste man ange det mha sitt username vid login.

API: **apic\#fallback\\\\username**
SSH: **apic\#fallback\\\\username**
GUI: **apic:fallback\\\\username**

Collecting Metrics - Example
----------------------------

[800px](/File:Cisco_ACI_Metrics.PNG "wikilink")

[Category:Cisco](/Category:Cisco "wikilink")