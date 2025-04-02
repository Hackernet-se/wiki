---
title: FirewallD
permalink: /FirewallD/
---

FirewallD ersätter iptables i RHEL 7, centOS 7 och Fedora 18. Den
främsta fördelen är att man kan göra alla ändringar utan att behöva
starta om tjänsten. Denna artikel innehåller grunderna för FirewallD.

Grunder
=======

**Kolla status**

`firewall-cmd --state`

**Detaljerad status**

`systemctl status firewalld.service`

**On/Off**

`systemctl enable firewalld.service`
`systemctl disable firewalld.service`

**Panic mode** (Blockar all traffik)

**On**

`firewall-cmd --panic-on`

**Off**

`firewall-cmd --panic-off`

OBS Om man har flera interface måste man slå på IPv4-forwarding

`sudo sed -i -r 's/net.ipv4.ip_forward=0/net.ipv4.ip_forward=1/g' /etc/sysctl.conf`
`sysctl -p`

Zoner
=====

FirewallD jobbar med säkerhetszoner och följande zoner finns default:

-   Public – For use in public areas. Only selected incoming connections
    are accepted.
-   Drop – Any incoming network packets are dropped, there is no reply.
    Only outgoing network connections are possible.
-   Block – Any incoming network connections are rejected with an
    icmp-host-prohibited message for IPv4 and icmp6-adm-prohibited for
    IPv6. Only network connections initiated within this system are
    possible.
-   External – For use on external networks with masquerading enabled
    especially for routers. Only selected incoming connections are
    accepted.
-   DMZ – For computers DMZ network, with limited access to the internal
    network. Only selected incoming connections are accepted.
-   Work – For use in work areas. Only selected incoming connections are
    accepted.
-   Home – For use in home areas. Only selected incoming connections are
    accepted.
-   Trusted – All network connections are accepted.
-   Internal – For use on internal networks. Only selected incoming
    connections are accepted.

Alla interface ligger default i zonen public. Varje zon är definierad i
en XML-fil som ligger i **/usr/lib/firewalld/zones**

**Kolla vilka zoner som finns**

`firewall-cmd --get-zones`

**Kolla aktiva zoner**

`firewall-cmd --get-active-zones`

**Kolla en zones permanenta konfiguration**

`firewall-cmd --permanent --list-all --zone=public`

**Kolla alla zoner detaljerat**

`firewall-cmd --list-all-zones`

**Ändra default zone**

`firewall-cmd --set-default-zone=home`

**Skapa en ny zone**

`firewall-cmd --permanent --new-zone=test`
`firewall-cmd --reload`

Aktivera zonen
--------------

För att en zone ska gälla behöver man aktivera den på interfacet eller
på CIDR-notation.
**Kolla vilka zoner som körs på ett interface**

`firewall-cmd --get-zone-of-interface=eth0`

**Aktivera en zone tillfälligt**

`firewall-cmd --zone=home --change-interface=eth0 `

**Aktivera en zone permanent**

`firewall-cmd --permanent --zone=home --change-interface=eth0`

**Aktivera på en CIDR-notion**

`firewall-cmd --permanent --zone=work --add-source=192.168.0.0/24`
`firewall-cmd --permanent --zone=work --list-sources`

Services
========

Det finns ett gäng fördefinerade tjänster men man kan enkelt lägga till
en egna för att slippa göra portöppningar.

**Lista alla tjänster**

`firewall-cmd --get-services`

Vill du kolla in varje tjänst mer detaljerat så kan du läsa XML filerna
under **/usr/lib/firewalld/services/ssh.xml**.

Skapa egen tjänst
-----------------

För att lägga till en egen tjänst, skapa en XML under
**/etc/firewalld/services/** med följande innehåll.

<div class="toccolours" style="width:40em">
<center>

**HAProxy.xml**

</center>
<div class="toccolours" style="width:40em">

``` xml
<?xml version="1.0" encoding="utf-8"?>
<service>
 <short>HAProxy</short>
 <description>HAProxy load-balancer</description>
 <port protocol="tcp" port="80"/>
</service>
```

</div>
</div>

Bra att känna till är att en tjänst under **/etc/firewalld/services/**
har högre prioritet än en tjänst under **/usr/lib/firewalld/services/**.

Lägga till en tjänst i en zone.
-------------------------------

För att sedan lägga till tjänsten på en zone permanent.

`firewall-cmd --permanent --zone=public --add-service=HAProxy`
`firewall-cmd --reload`

Portforwarding
--------------

`firewall-cmd --zone=external --add-forward-port=port=80:proto=tcp:toport=8080:toaddr=192.168.0.50`

**Iptables**
Man kan byta tillbaka om man känner sig gammalmodig.
<http://www.certdepot.net/rhel7-disable-firewalld-use-iptables/>

[Category:Tools](/Category:Tools "wikilink")