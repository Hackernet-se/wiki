---
title: Cisco WAN
permalink: /Cisco_WAN/
---

Den vanligaste L2-tekniken nuförtiden är Ethernet men det finns andra.

HDLC
====

Ciscos implementation av HDLC har ett 2-byte stort Type-fält som gör det
properitärt, detta för att stödja multipla protkoll över HDLC-länkar.
HDLC är default enkapsulering på seriella interface på Cisco-routrar och
keepalives skickas default var 10:e sekund. DCE-änden av kabeln står för
clockrate.

DCE eller DTE?

`show controllers serial 0/0`

HDLC är default.

`interface serial 0/0`
` encapsulation hdlc`
`show interface serial 0/0`

PPP
===

PPP använder likadan header som ursprungs HDLC men har ett Protocol-fält
så det blir i princip Cisco HDLC. Det har dessutom fler features. PPP
använder kontrollprotokoll för L2 och L3. För L2 heter dessa Link
Control Protocol (LCP) och för L3 heter de Network Control Protocol
(NCP). Ett exempel på PPP NCP är IPCP för IP och möjliggör dynamic
address assignment. När LCP har förhandlat klart om Link Quality
Monitoring, Looped link detection, LB/MLPPP och autentiseringsmetoder
och sett resultat av dessa tar NCP vid.

<div class="mw-collapsible mw-collapsed" style="width:270px">

LCP Request:

<div class="mw-collapsible-content">

[<File:Cisco_WAN_LCP_Request.png>](/File:Cisco_WAN_LCP_Request.png "wikilink")

</div>
</div>
<div class="mw-collapsible mw-collapsed" style="width:270px">

LCP Ack:

<div class="mw-collapsible-content">

[<File:Cisco_WAN_LCP_Ack.png>](/File:Cisco_WAN_LCP_Ack.png "wikilink")

</div>
</div>
<div class="mw-collapsible mw-collapsed" style="width:270px">

IPCP Request:

<div class="mw-collapsible-content">

[<File:Cisco_WAN_IPCP_Request.png>](/File:Cisco_WAN_IPCP_Request.png "wikilink")

</div>
</div>
<div class="mw-collapsible mw-collapsed" style="width:270px">

IPCP Ack:

<div class="mw-collapsible-content">

[<File:Cisco_WAN_IPCP_Ack.png>](/File:Cisco_WAN_IPCP_Ack.png "wikilink")

</div>
</div>

`interface serial 0/0`
` encapsulation ppp`
`show interface serial 0/0`

LQM ställs med:

`ppp quality <%>`

Peer neighbor route är en PPP feature som låter connected interfaces som
inte är på samma subnät att kommunicera. Detta är användbart t.ex. när
man använder ip unnumbered interfaces på PPP-länken men kan stängas av
om interfacen befinner sig på samma subnät. Detta är påslaget default på
Cisco IOS när man använder PPP-enkapsulering.

`interface `<ppp-interface>
` no peer neighbor-route`

### Authentication

PPP har bl.a. stöd för PAP, CHAP, MS-CHAPv1/v2 och EAP.

PAP

`username R2 password SECRET`

`interface serial 0/0`
` ppp authentication pap`
` ppp pap sent-username R1 password SECRET`

CHAP, default används routerns hostname som username.

`username R2 password SECRET`

`interface serial 0/0`
` ppp authentication chap`
` ppp chap hostname R1`
` ppp chap password SECRET`

Använd andra metoden som fallback genom att ange dem på samma rad.

`ppp authentication chap pap`

Troubleshoot

`debug ppp authentication`

### Compression

Det finns två typer av compression, layer 2 payload compression och
TCP/RTP header compression. Payload compression funkar bäst med stora
paket medans header compression funkar bäst med små paket. L2 payload
compression kan göras med *stacker*, *MPPC* eller *predictor*. De första
två använder lite mer CPU men brukar resultera i bättre ratio.

`compress predictor`

TCP Header. Detta är legacy-metoden för att konfigurera det, man kan
också använda [MQC](/Cisco_QoS#MQC "wikilink").

`ip tcp header-compression`

Encryption

`ppp encrypt mppe 40 required`

Verify

`show compress details`
`show ppp mppe`

### MLPPP

Multilink PPP är en teknik för att L2-lastdela på två eller fler
parallella seriella länkar. MLPPP fragmenterar frames och skickar dem
över olika länkar.

`interface multilink1`
` encapsulation ppp`
` ppp multilink`
` ppp multilink group 1`

`interface serial 0/0`
` encapsulation ppp`
` ppp multilink`
` ppp multilink group 1`

Verify

`show ppp multilink`
`show interface multilink1`

**Interleaving**
För att förhindra att små delay-känsliga paket hamnar bakom stora paket
som tar lång tid att serialisera kan man använda LFI. Det är ett Cisco
QoS tool som gör att de små paketen kan skickas mellan fragmenten av de
stora paketen.

`interface multilink1`
` ppp multilink fragment-delay 10`
` ppp multilink interleave`

PPPoE
=====

PPPoE (RFC 2516) är enkapsulering av PPP över ethernet och används mest
i gamla DSL-tjänster. Det använder en ethernet-baserad
discovery-funktion för att klient ska hitta till server. PPPoE har inte
support för MLPPP.

<div class="mw-collapsible mw-collapsed" style="width:270px">

Initiation (broadcast):

<div class="mw-collapsible-content">

[<File:Cisco_WAN_PPPoE_PADI.png>](/File:Cisco_WAN_PPPoE_PADI.png "wikilink")

</div>
</div>
<div class="mw-collapsible mw-collapsed" style="width:270px">

Offer:

<div class="mw-collapsible-content">

[<File:Cisco_WAN_PPPoE_PADO.png>](/File:Cisco_WAN_PPPoE_PADO.png "wikilink")

</div>
</div>
<div class="mw-collapsible mw-collapsed" style="width:270px">

Request:

<div class="mw-collapsible-content">

[<File:Cisco_WAN_PPPoE_PADR.png>](/File:Cisco_WAN_PPPoE_PADR.png "wikilink")

</div>
</div>
<div class="mw-collapsible mw-collapsed" style="width:270px">

Session-confirmation:

<div class="mw-collapsible-content">

[<File:Cisco_WAN_PPPoE_PADS.png>](/File:Cisco_WAN_PPPoE_PADS.png "wikilink")

</div>
</div>
<div class="mw-collapsible mw-collapsed" style="width:270px">

Termination:

<div class="mw-collapsible-content">

[<File:Cisco_WAN_PPPoE_PADT.png>](/File:Cisco_WAN_PPPoE_PADT.png "wikilink")

</div>
</div>

När MAC-adressen för servern är känd och sessionen är upprättad kan PPP
ta vid.

### Server

På ethernet-interfacen behöver man inte ha någon IP-adress alls eftersom
discovery-funktionen är ethernet-baserad.

`bba-group pppoe global`
` virtual-template 1`
` sessions per-mac limit 2`

`interface gi2`
` no ip address`
` pppoe enable group global`

`interface virtual-template 1`
` ip address 192.168.0.1 255.255.255.0`
` peer default ip address pool PPPoE`

`ip local pool PPPoE 192.168.0.10 192.168.0.20`

### Klient

PPPoE-klienter bör ha MTU 1492 på sina dialer interface för att undvika
fragmentering på ethernet-interface eftersom PPPoE lägger på 8 bytes
header. Man kan använda statiska ip-adresser, ip unnumbered eller
dynamiska med hjälp av IPCP på PPP-interfacet.

`interface Fa0/1`
` no shut`
` pppoe enable `
` pppoe-client dial-pool-number 1`

`interface Dialer1`
` ip mtu 1492`
` ip tcp adjust-mss 1452`
` encapsulation ppp`
` ip address negotiated   `*`#IPCP`*
` dialer pool 1`

Verify

`show pppoe summary`
`show ppp all`
`show pppoe session`
`show derived-config interface virtual-access1.1`

**Default route**
PPP kan dynamiskt installera en default route när IPCP-förhandlingen
lyckas och ta bort den igen när dialer-interfacet går ner. Denna route
är en static route och får därmed AD 1 så det går ej att trumfa den.

`interface Dialer1`
` encapsulation ppp`
` ppp ipcp route default`

**SNMP**

`snmp-server enable traps pppoe`

[Category:Cisco](/Category:Cisco "wikilink")