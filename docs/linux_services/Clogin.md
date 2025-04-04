---
title: Clogin
permalink: /Clogin/
---

Clogin är ett script som används för inloggning på Ciscoenheter. Det är
en komponent för [Rancid](/Rancid "wikilink").

Installation
============

`sudo apt-get -y install rancid`

Förberedelser
=============

Kopiera clogin till ditt hem-directory, t.ex. cp
/var/lib/rancid/bin/clogin \~/

cloginrc

`cd && nano .cloginrc`
`#add autoenable * 1`
`add method * ssh`
`add user * cisco`
`add password * cisco cisco`

Skydda filen så gott det går

`chmod 600 .cloginrc`

Script

`nano clogin-execute.sh`
`#!/bin/bash`
`for line in $(cat device-iplist.txt | grep -v '#')`
`do`
`/home/$USER/clogin -x commands.txt $line`
`done`

Rättigheter

`chmod +x clogin-execute.sh`

Konfiguration
=============

Lista vilka enheter kommandona ska köras på.

`nano device-iplist.txt`
`# Kommentera ut med #`
`10.0.0.100`
`10.0.0.101`
`#10.0.0.102`
`...`

Lista vilka kommandon som ska köras på varje enhet. Exempel, skapa vlan.

`nano commands.txt`
`show vlan id 50 | i 50`
`conf t`
` vlan 50`
`  name Vlan50`
`  mode fabricpath`
` exit`
`exit`
`show vlan id 50 | i 50`
`wr`
`exit`

Exekvera scriptet

`./clogin-execute.sh`

[Category:Cisco](/Category:Cisco "wikilink")