---
title: VMware Vsphere Client
permalink: /VMware_Vsphere_Client/
---

VSphere Client kan användas för att managera ESXi Hosts samt Vcenter men
har inte alla funktioner till Vcenter som finns i WebGuit.

Installation
------------

Vsphere client finns att ladda ner via din ESXi Host eller Vcenter och
är bara att klicka next på genom hela.

Kända Fel
---------

Fel som kan uppstå med vsphere client.

**`Om`` ``man`` ``får`` ``felet`` ``VPXclient.exe`` ``har`` ``slutat`` ``svara`` ``vid`` ``start`` ``av`` ``programmet.`**
`Länkplats C:\Program Files (x86)\VMware\Infrastructure\Virtual Infrastructure Client\Launcher (windows 10 Pro x64)`
`   - Redigera fil VpxClient.exe.config och lägg till :`
`         `<startup useLegacyV2RuntimeActivationPolicy="true">
`             `<supportedRuntime version="v4.0"/>
`         `</startup>

[Category:VMware](/Category:VMware "wikilink")
[Category:Guider](/Category:Guider "wikilink")