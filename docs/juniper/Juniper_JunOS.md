---
title: Juniper JunOS
permalink: /Juniper_JunOS/
---

Junos bygger på FreeBSD och man kan därför få shell access och köra
många unix kommandon på switchen.

Junos CLI är uppdelat i två kommandolägen.

-   Operational Mode
-   Configuration Mode

Till skillnad från tex Cisco, HP och Extreme där en ändring sker direkt
när man skrivit kommandot så måste man i JunOS skriva commit.

Operational
-----------

Gå till operational mode. Här kan man köra kommandon för att
troubleshoota och monitorera.

`cli`

Lista conf i set kommandon. Andvändbart om man behöver paste in conf.

`show configuration | display set`

Lista conf efter hierarchy level.(Funkar enbart om man gått in i edit
läge på tex ett interface.)

`show configuration | display set relative`

Visa mac tabellen.

`show ethernet-switching table`

Configuration
-------------

Gå till configuration mode.

`configure `

Går till configuration mode och låser den globala configurationen, så
att andra användare inte kan commita förens du lämnat

configuration mode.

`configure exclusive`

Lämna configuration mode utan att commita.

`exit `

Kör operational mode kommandon i configuration mode.

`run `<operational mode kommando>

Commit
------

Lämna configuration mode och commita ändringar.

`commit and-quit`

Visa vad som kan commitas.

`show | compware`

Ta bort all conf som ligger redo att commitas.

`rollback`

Rollbacka till en conf vid en viss tid.

`rollback ?`

Commita och kör en autorollback efter 2 miniut. För att stoppa
autorollback skriv `commit` bara.

`commit confirmed 2`

Konfiguration
-------------

**Hostnamn**

`set system host-name [hostname]`

**Lösenord på root(autoencryption)**

`set root-authentication plain-text-password`

Om du redan har en krypterad sträng av lösenordet använd följande.

`set root-authentication encrypted-password`

Tillåt enbart root logins över console.

`set services ssh root-login deny`

**Skapa användare**

`set system login user admin uid 2000`
`set system login user admin class super-user`

**Mgmt port**

`set interfaces vme unit 0 family inet address 192.168.0.0/24`
`set routing-options static route 0.0.0.0/0 next-hop 192.168.0.1`

**LLDP**

`set protocols lldp interface all`

**Tid**

`set system time-zone Europe/Stockholm`

`set system ntp server [ip] prefer`
`set system ntp server [ip]`

Firmware
--------

### Scp

Börja med att skicka över imagen till JunOS.

`scp [image] root@[juniper]:/var/tmp/[image]`

Från operational mode kör sedan följande.

`request system software add /var/tmp/[image] no-copy no-validate unlink reboot`

### USB

Börja med att mounta usb stickan med.

`mount_msdosfs /dev/da0s1 /mnt`

Kopiera imagen till JunOS.

`cp /mnt/[image] /var/tmp/`

Unmounta usb stickan.

`unmount /mnt`

Gå in i operational mode.

`request system software add /var/tmp/[image] no-copy no-validate unlink reboot`

Backup
------

### Configuration

Man kan använda system som [Rancid](/Rancid "wikilink") eller
[Oxidized](/Oxidized "wikilink") för att backa upp sin JunOS device. Om
man inte har något sånt system uppsatt så kan man sätta
**transfer-on-commit** eller **transfer-interval**.

**transfer-on-commit** kommer att skicka din config fil till ditt valda
**archive-sites** varje gång du commitar.

**transfer-interval** gör samma sak fast den skickar iväg configen en
gång i timmen bara.

Börja med att sätta dina **archive-sites**

`set system archival configuration archive-sites scp://backupusr@10.10.10.200:/opt/backup/R1 password hackernet`

Byt ut **SCP** mot **FTP** om du hellre vill använda det.

Efter det så väljer du när du vill skicka configen.

`set system archival configuration transfer-on-commit`
`set system archival configuration transfer-interval `**`interval-in-minutes`**

Filen kommer att sparas som
**<router-name>_YYYYMMDD_HHMMSS_juniper.conf.n.gz**.

### Image

Man kan backupa en hel JunOS image och hur configen ser ut vid
tillfället till en annan partition så ifall en firmware upgrade skulle
gå snett kan man boota ifrån den.

**Skapa en recovery snapshot**

`request system snapshot recovery`

På äldre platformar kör man

`request system snapshot slice alternate`

[Category:Juniper](/Category:Juniper "wikilink")