---
title: Standard vSwitch
permalink: /Standard_vSwitch/
---

En vSwitch är som namnet antyder en virtuell switch, till vilken
virtuella maskiner ansluter sina virtuella nätverkskort (vNIC). Till en
vSwitch kopplas ett eller flera fysiska NIC:ar (pNIC) från ESXI-hosten
som används som upplänk(ar).

Port Groups
-----------

Port Groups används för att gruppera och/eller separera virtuella
maskiner nätverksmässigt, t ex Test och Produktion. Portgrupperna kan
tilldelas olika, eller samma VLAN, dock måste de ha ett unikt namn.
En portgrupp kan konfigureras med tre olika VLAN Tagging Modes:
**External Switch Tagging** (**EST**), endast otaggad trafik
forwarderas, VLAN ID 0 används.
**Virtual Switch Tagging** (**VST**), vSwitchen taggar trafik, VLAN ID
1-4094 används.
**Virtual Guest Tagging** (**VGT**), det är upp till VM:en att sköta
VLAN-taggningen, VLAN ID 4096 används.

Network Security Policies
-------------------------

I en vSwitch kan en Security Policy konfigureras, de tre inställningar
som kan ändras är:
**Promiscuous Mode** - Promiscuous mode tillåter (vid Accept) att
medlemmar i portgruppen tar emot samtliga frames som traverserar den
virtuella switchen, eller för det VLAN som specificerats i
portgruppen.
**MAC Address Changes** - Tillåter/förbjuder VM:en att byta MAC-adress
inifrån gäst-OS:et. Om policyn är inställd på Reject, stängs den
virtuella switchporten om ett MAC-adressbyte registreras. Porten
avblockeras då MAC-adressen ändras tillbaka till "Initial address".
**Forged Transmits** - Om Forged Transmits är satt till Reject kommer
ESXi-hosten att inspektera L2-headern på varje paket som skickas från
VM:arna i portgruppen/vSwitch:en. MAC-adressen i headern kommer att
jämföras med "Effective address" (adressen som gäst-OS:et tilldelat sin
adapter, oftast samma som Initial address), matchar inte source-adressen
i L2-headern kommer paketet att droppas.

Per default är endast Promiscuous Mode inställt på Reject i en Standard
vSwitch. I en DvSwitch däremot är samtliga inställda på Reject från
början.

[Category:VMware](/Category:VMware "wikilink")