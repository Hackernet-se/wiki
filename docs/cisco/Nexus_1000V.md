---
title: Nexus 1000V
permalink: /Nexus_1000V/
---

Nexus 1000V är en distribuerad virtuell switch som sträcker sig över
många hypervisor-hostar. Varje server i datacentret representeras som
ett linjekort i Nexusen och kan hanteras som om det vore ett linjekort i
en fysisk Cisco switch. N1Kv har bl.a. stöd för
[NetFlow](Cisco_NetFlow.md), [IGMP
Snooping](Cisco_IGMP.md#IGMP_Snooping#IGMP_Snooping#IGMP_Snooping#IGMP_Snooping#IGMP_Snooping#IGMP_Snooping#IGMP_Snooping#IGMP_Snooping),
[SPAN](Cisco_SPAN.md), [VXLAN](Cisco_VXLAN.md),
[Private VLAN](Cisco_VLAN.md#Private_VLAN#Private_VLAN#Private_VLAN#Private_VLAN#Private_VLAN#Private_VLAN#Private_VLAN#Private_VLAN), [DHCP
Snooping](Cisco_DHCP.md#Snooping#Snooping#Snooping#Snooping#Snooping#Snooping#Snooping#Snooping),
[DAI](Cisco_L2_Security.md#DAI#DAI#DAI#DAI#DAI#DAI#DAI#DAI) och
[IPSG](Cisco_L3_Security.md#IPSG#IPSG#IPSG#IPSG#IPSG#IPSG#IPSG#IPSG). Nexus 1000V kan köras
tillsammans med [vSphere](../vmware/VMware_ESXi.md), Hyper-V eller
[KVM](../linux_virt/KVM.md).

**Virtual Ethernet Module** (VEM) är ett virtuellt linjekort och körs
som en del av ESXi-kärnan (VEM agent) och ersätter vSwitcharna.

**Virtual Supervisor Module** (VSM) är control plane och styr alla VEMs.
I stället för fysiska SUPar körs VSM som vms på ESXi-hostarna.
Konfigurationen görs i VSM och slår på alla VEMs.

*Du behöver vSphere Enterprise Plus licensiering för att kunna använda
Nexus 1000V.*

Installation
============

**Dokumentation**

[`http://www.cisco.com/c/en/us/support/switches/nexus-1000v-switch-vmware-vsphere/products-installation-guides-list.html`](http://www.cisco.com/c/en/us/support/switches/nexus-1000v-switch-vmware-vsphere/products-installation-guides-list.html)

VSM
---

VSM installeras som en vm.

### Registrera Nexus i vCenter

[`http://VSM-IP`](http://VSM-IP)

Ladda ner cisco_nexus1000v_extension.xml
vCenter
Manage Plug-ins -\> New Plug-in -\> xml file -\> Register Plug-in

### SVS Connection

Kan göras i L2 eller L3 mode.

```
svs connection vCenterName 
 protocol vmware-vim
```
` remote ip address `<vCenter-IP>
` vmware dvs datacenter-name `<name>
```
 max-ports 8192
 connect
```

Verify

```
show svs connections
show module
```

VEM
---

Linjekort, ett per esxi-host. Default sätts ID dynamiskt men man kan
binda det till uuid.

```
vem 3
  host vmware id 8f862310-4c63-11e2-0000-00000000000f
vem 4
  host vmware id 8f862310-4c63-11e2-0000-00000000001f
```

Show

```
show module
```

Port Profile
============

Fysiska NICs konfas med "type ethernet".

```
port-profile type ethernet vMotion-Uplink
 vmware port-group
 switchport mode trunk
 switchport trunk allowed vlan 99
 no shutdown
 state enabled
```

```
port-profile type ethernet VM-Guests-Uplink
 vmware port-group
 switchport mode trunk
 switchport trunk allowed vlan 100,110,111,112,120,121
 no shutdown
 system vlan 100,120,121
 state enabled
```

System VLAN är speciella vlan som får kommunicera innan VEM:en har lagts
i vDS. Det betyder att forwarding på VEM kan göras innan VSM har
programmerat forwarding tables.

Management network.

```
port-profile type vethernet VMKernel
 capability l3control
 vmware port-group
 switchport mode access
 switchport access vlan 100
 no shutdown
 system vlan 100
 state enabled
```

Port profiles "type vethernet" är motsvarigheten till port groups i
VMware och för varje port profile i Nexus 1000v skapas en portgrupp i
VMware.

```
port-profile type vethernet vMotion
 vmware port-group
 switchport mode access
 switchport access vlan 116
 no shutdown
 state enabled
```

```
port-profile type vethernet VM-110
 vmware port-group
 switchport mode access
 switchport access vlan 110
 no shutdown
 state enabled
```

```
port-profile type vethernet VM-111
 vmware port-group
 switchport mode access
 switchport access vlan 111
 no shutdown
 state enabled
```

```
port-profile type vethernet N1Kv-Control
 vmware port-group
 switchport mode access
 switchport access vlan 120
 no shutdown
 system vlan 120
 state enabled
```

```
port-profile type vethernet N1Kv-Management
 vmware port-group
 switchport mode access
 switchport access vlan 121
 no shutdown
 system vlan 121
 state enabled
```
