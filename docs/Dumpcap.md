---
title: Dumpcap
permalink: /Dumpcap/
---

Dumpcap är ett network traffic dump tool. Det ingår i wireshark-sviten
och är det som används av wireshark och tshark. För att få trafik till
dumpcap kan t.ex. en nätverkstapp eller span-port användas. Default
filformat är pcap-ng.

### Installation

`sudo apt-get install wireshark-common`

Lista möjliga interface

`sudo dumpcap -D`

Exempel, spara data i samma fil under 1h, påbörja sedan nästa fil,
upprepa 24 gånger. Dvs ett dygn.

`sudo dumpcap -i eth0 -b duration:3600 -b files:24 -w packets.pcap`

Exempel, filesize i kB, sedan ny fil. 5GB totalt.

`sudo dumpcap -i eth1 -b filsize:1000000 -b files:5 -w /pcap/packets.pcap`

Se även till att paketdumparna, som kan bli väldigt stora, ligger på ett
eget filsystem för att förhindra att diskutrymme tas upp för
operativsystemet.

[Category:Tools](/Category:Tools "wikilink")