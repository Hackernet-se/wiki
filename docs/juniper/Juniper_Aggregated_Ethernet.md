---
title: Juniper Aggregated Ethernet
permalink: /Juniper_Aggregated_Ethernet/
---

Aggregated Ethernet(ae) är Junipers implementation av IEEE 802.3ad som
används för att bundla ihop flera fysiska interface till ett logiskt
interface som kallas LAG. Med hjälp av ett ae interface kan man få högre
redundans och även högre hastighet eftersom att man kan last balansera
trafiken på flera portar.

Ciscos motsvarighet heter [EtherChannel](/Cisco_EtherChannel "wikilink")

Link Aggregation Control Protocol
=================================

LACP är en subkomponent till IEEE 802.3ad som tillför extra kontroll för
att hålla koll på din LAG och att det finns mindre risk för
konfigurationsmisstag. För att LACP ska kunna fungera så krävs det att
båda sidorna använder LACP. När LACP är påslaget så skickas det LACPDU
en gång i sekunden med information tills förhandlingen är genomförd
sedan återgår det till vad keepalive är satt till.

-   Keepalive är hur ofta enheterna skickar LACPDU där default mode
    slow=30s och fast=1s.
-   LACP använder alltid multicast MAC adressen 01:80:c2:00:00:02 för
    att skicka sina frames.

Fördelen med att använda LACP är att din enhet inte kommer försöka
skicka trafik mot ett interface som inte svarar på LACPDU och att
kommunikationen failar för andra applikationer. Har man en
mediaconverter på en länk mellan 2st enheter som utbyter LACPDU så
kommer den ena enheten känna till om den andra enheten skulle tappa
kontakten med mediaconvertern på sin sida och därav sluta skicka trafik
på det interfacet.

[Category:Juniper](/Category:Juniper "wikilink")