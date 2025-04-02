---
title: Systemd
permalink: /Systemd/
---

Systemd är ett init-system och en service-hanterare som är standard för
de flesta linux-distar. Det grundläggande syftet med ett init-system är
att initiera de komponenter som måste startas efter att Linuxkärnan har
startat. Systemd är det första som startar efter att kernel har startat
och får alltid Process ID 1. Init-systemet används också för att hantera
tjänster och demoner för servern medan systemet är igång.

Default sedan:
Debian 8
Ubuntu 15.04
Fedora 15
RHEL 7
CentOS 7

Systemctl
=========

Systemctl är det centrala verktyget för att kontrollera init-systemet.
Systemctl ersätter service och chkconfig.
Grundfunktioner

`systemctl start sshd`
`systemctl stop sshd`
`systemctl reload sshd`
`systemctl restart sshd`

Status

`systemctl status sshd`

Autostarta en service

`systemctl enable sshd`
`systemctl disable sshd`

Lista alla aktiva enheter

`systemctl `

Lista alla enheter

`systemctl list-units --all`

OBS .service behöver inte skrivas ut, det läggs till efter tjänsten
automatiskt
Fler kommandon

`systemctl show sshd.service`
`systemctl list-dependencies sshd.service`

Titta på senaste uppstart grafiskt. Testa detta, seriöst det är coolt!

`systemd-analyze plot > plot.svg`

Lägga till egna services
------------------------

Under `/etc/systemd/system` kan man lägga till egna services som man
vill hantera med systemd.

En basic service fil ser ut så här.

`[Unit]`
`Description=Hello world`
`After=network-online.target`
`Wants=network-online.target`

`[Service]`
`ExecStart=/usr/bin/echo "Hello world!"`

`[Install]`
`WantedBy=multi-user.target`

Om servicen kräver att det finns nätverk före den startar kan man skriva
**After/Wants=network-online.target** då kommer servicen att försöka
starta efter serverns nätverk har gått upp och den har fått en routebar
IP.

För att systemd ska köra servicen vid boot måste man köra enable.

`systemctl enable /etc/systemd/system/hello.service`

För att starta tjänsten skriv.

`systemctl start hello.service`

Övervaka en service
-------------------

Med systemd kan man övervaka en tjänst så att den startas automatiskt om
den skulle krasha.

`systemctl edit sshd`

Skriv sedan in:

`[Service]`
`Restart=always`

Spara sedan filen. Den kommer att sparas under
**/etc/systemd/system/sshd.service.d/overrides.conf**

Vill du ha en delay innan systemd startas tjänsten igen så går det också
med:

`RestartSec=30`

Kör sedan en reload:

`systemctl daemon-reload`

Journald
========

Journald är en systemd-komponent som har hand om loggar från
applikationer och kärna. Kommandot man använder är journalctl. Kör
igenom dessa för att bilda dig en uppfattning av vad de gör och hur de
fungerar.

`journalctl`
`journalctl -k`
`journalctl -u nginx.service`
`journalctl -u nginx.service --since today`
`journalctl _PID=8088`
`journalctl --disk-usage`

Networkd
========

`systemctl start systemd-networkd`
`networkctl`
`networkctl status`

Nspawn
======

Systemd-nspawn är en container manager som är inbyggd i systemd.
*Debian*

`apt-get install -y dbus debootstrap bridge-utils`
`debootstrap --arch=amd64 jessie /var/lib/machines/container1/`
`systemd-nspawn -D /var/lib/machines/container1/ --machine first_container -b`

OBS med denna setup delas network namespace med värdhosten. Annars måste
man skapa en brygga och koppla containern till den.

`systemd-nspawn -D /var/lib/machines/container1/ --machine second_container --network-bridge=my-bridge -b`

Kolla containers

`machinectl`
`machinectl status first_container`
`machinectl login first_container`

Template unit
=============

En template unit går att identifera med hjälp av **@** som är efter base
unit namnet och före unit type suffixen.

`openvpn-client@.service`

För att använda sig av en template unit så lägger man in en instance
identifier mellan **@** och punkten när man kallar på den med
`systemctl start` eller annat kommando.

`openvpn-client@`**`hackernet-vpn`**`.service`

Med detta sättet så behöver man bara en unit fil istället för en fil per
instans man försöker starta.

Variabler
---------

-   `%n`: Ger hela unit namnet. **Ex:
    openvpn-client@hackernet-vpn.service**
-   `%N`: Samma som ovan fast all escape tecken kommer vara omvänd.
    **Ex: openvpn-client@hackernet-vpn**
-   `%p`: Ger unit namnet som är före **@**. **Ex: openvpn-client**
-   `%P`: Samma som ovan fast escape är omvänt. **Ex: openvpn/client**
-   `%i`: Ger det som är efter **@** och punkten. **Ex: hackernet-vpn**
-   `%I`: Samma som ovan fast escape är omvänt. **Ex: hackernet/vpn**
-   `%f`: Samma som ovan och den lägger på ett **/** före. **Ex:
    /hackernet/vpn**
-   `%u`: Vilken användare som är confad att köra uniten. **Ex: root**
-   `%U`: Samma som ovan fast visar `UID` istället. **Ex: 0**
-   `%h`: Visar vart användarens home folder finns. **Ex: /root**
-   `%H`: Visar hostnamnet på servern. **Ex vpnserver**
-   `%s`: Visar användarens shell. **Ex: /bin/sh**
-   `%v`: Visar vilken kernel release som körs. Samma svar som
    `uname -r`. **Ex: 3.10.0-514.6.1.el7.x86_64**
-   `%%`: Används för att skapa ett procent tecken.

Exempel template unit
---------------------

[Category:Tools](/Category:Tools "wikilink")