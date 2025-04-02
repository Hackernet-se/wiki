---
title: Juniper VLAN
permalink: /Juniper_VLAN/
---

Konfiguration
-------------

**Skapa vlan**

`set vlans [VLAN-name] vlan-id [VLAN-id]`

**Access port**

`set interfaces ge-0/0/0 unit 0 family ethernet-switching vlan members [VLAN-name]`

**Trunk port**

`set interfaces ge-0/0/0 unit 0 family ethernet-switching port-mode trunk`
`set interfaces ge-0/0/0 unit 0 family ethernet-switching vlan members [VLAN-name]`

[Category:Juniper](/Category:Juniper "wikilink")