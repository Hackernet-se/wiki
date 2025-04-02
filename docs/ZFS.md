---
title: ZFS
permalink: /ZFS/
---

ZFS är filsystem kombinerat med volymhanterare. Det körs främst på BSD
men finns även till [Linux](http://zfsonlinux.org/).

Installation
============

*Ubuntu 16.04 onwards*

`sudo apt-get update && sudo apt-get -y install zfs`

*Fedora*

`sudo dnf install --nogpgcheck `[`http://archive.zfsonlinux.org/fedora/zfs-release$(rpm`](http://archive.zfsonlinux.org/fedora/zfs-release$(rpm)` -E %dist).noarch.rpm`
`sudo dnf install kernel-devel zfs `
`sudo /sbin/modprobe zfs`

*Debian*

`su -`
`apt-get install lsb-release`
`wget `[`http://archive.zfsonlinux.org/debian/pool/main/z/zfsonlinux/zfsonlinux_6_all.deb`](http://archive.zfsonlinux.org/debian/pool/main/z/zfsonlinux/zfsonlinux_6_all.deb)
`dpkg -i zfsonlinux_6_all.deb`
`apt-get update && apt-get install debian-zfs`

Konfiguration
=============

### Pool

`zpool create POOL raidz1 \`
`        /dev/disk/by-id/ata-WDC_WD.. \`
`        /dev/disk/by-id/ata-WDC_WD.. \`
`        /dev/disk/by-id/ata-WDC_WD.. \`
`        -o ashift=12 -o failmode=continue`

Lägg till -f om det inte finns någon EFI label.

` zfs set atime=off POOL`

Show-kommandon.

`zpool list`
`zpool status`
`zfs get all`
`zpool iostat -v POOL`

Radera en pool.

`zpool destroy POOL`

Återställ raderad pool.

`zpool import -D POOL`

### Mount point

`zfs set mountpoint=/path/pool POOL`
`chown -R user:user /path/pool`

### Dataset

`zfs create POOL/test`

Kompression.

`zfs set compression=on POOL/test`

Deduplicering.

`zfs set dedup=on POOL/test`

Radera dataset.

`zfs destroy POOL/test`

### L2ARC

Level 2 Adjustable Replacement Cache (L2ARC), är en utökning av den read
cache (ARC) som finns i RAM.

`zpool add -f POOL cache sdf`

### ZIL & SLOG

ZFS Intent Log (ZIL) går att likna vid journalen i ett journalförande
filsystem. Synkrona skrivningar skrivs alltid till ZIL först och flushas
senare till poolen vid fasta intervall. En Separate Intent Log (SLOG) i
form av SSD rekommenderas för ökad prestanda vid synkrona skrivningar.
ZIL är ingen write cache utan används enbart som ett skydd mot
dataförlust, den enda prestandaökningen rör synkrona skrivningar som
utan en SLOG hade skrivits två gånger till samma disk då ZIL befunnit
sig inuti den pool dit data skrivs.

`zpool add -f POOL log sdg`

Om man är extra rädd om sin data kan man tvinga alla skrivningar att gå
genom ZIL med kommandot nedan. Det går att ställa på enskilda dataset
eller hela pooler om så önskas.

`zfs set sync=always POOL/test`

Det går även att stänga av ZIL helt om man inte bryr sig om
dataintegritet (samma syntax som ovan fast disable istället för always,
standard är default).

Underhåll
=========

### Scrub

Scrubbing används i ZFS för att bibehålla dataintegritet och fixa
eventuella fel på diskarna i din pool. Detta sker inte per automatik
utan måste triggas, cronjob rekommenderas starkt. Rekommendationen som
finns för frekvens av scrubbing på Solaris för enterprise- och
konsumentdiskar är en gång i månaden resp. en gång i veckan.

`zpool scrub`

*IO intensive*

### Snapshots

Snapshot kan tas både på pools och datasets, varje snapshot kräver ett
unikt namn.

Dataset snapshot.

`zfs snapshot POOL/test@NAME`

Pool snapshot.

`zfs snapshot POOL@NAME`

Lista snapshots.

`zfs list -t snapshot`

Rollback till snapshot.

`zfs rollback POOL/test@NAME`

Ta bort snapshot.

`zfs destroy POOL/test@NAME`

**Automatiska snapshots**
Det finns ett antal olika paket/skript för att sköta automatisering av
snapshots för ZFS. Här beskrivs användning av det cron-baserade
zfs-auto-snapshot som skapats av ZFS on Linux-utvecklarna. Nedan följer
ett antal kommandon för justering av frekvens och historik:

`zfs set com.sun:auto-snapshot=true POOL/test` Enable/disable av
automatiska snapshots på ett dataset.

`zfs set com.sun:auto-snapshot:monthly=false POOL/test` Enable/disable
av månatliga snapshots, som mest bevaras tolv snapshots.

`zfs set com.sun:auto-snapshot:weekly=false POOL/test` Enable/disable av
veckovisa snapshots, som mest bevaras åtta snapshots.

`zfs set com.sun:auto-snapshot:daily=true POOL/test` Enable/disable av
dagliga snapshots, som mest bevaras 31 snapshots.

`zfs set com.sun:auto-snapshot:hourly=false POOL/test` Enable/disable av
snapshots varje timme, som mest bevaras 24 snapshots.

`zfs set com.sun:auto-snapshot:frequent=false POOL/test` Enable/disable
av snapshots varje kvart, som mest bevaras fyra snapshots.

För att ändra t ex antal sparade snapshots får man editera de
medföljande cron-jobb som installeras tillsammans med zfs-auto-snapshot,
växeln som används för att ställa just detta är `--keep=X`.

### Byta disk

Det går att starta en replace av disk oavsett om disken i fråga
fortfarande är online eller om den tagits bort från systemet. Men innan
du börjar, kör en scrub för att garantera att poolen är intakt!

Är *disk1* online kommer kommandot nedan att attach:a *disk2* till
poolen och starta en resilver (rebuild, för den som inte talar ZFS) av
data på den nya; *disk2*. När *disk1* är redo att tas bort detach:as den
automatiskt från poolen. Om *disk1* inte är tillgänglig är det samma
förfarande för att göra en replace. Det är dock möjligt att strunta i
att ange den nya diskens namn eftersom ZFS antar att den nya disken
sitter på samma plats som den förra (/dev/sdX) och konfigurerar den då
automatiskt. Om disk-ID används för att referera till diskarna i poolen
måste dock den nya disken specificeras med sin path. Poolens namn på
disken ändras då disken är frånvarande, för att ta reda på vad *disk1*
heter istället används i vanlig ordning `zpool status`.

`zpool replace POOL disk1 disk2`

Får du ett felmeddelande som säger "*disk2* does not contain an EFI
label but it may contain partition information in the MBR" bör det räcka
att skapa en GPT-tabell på disken med t ex. parted. Vänta på att
resilvering körs färdigt, kolla status med `zpool status`.

Tips'N'Trix
===========

### Byte från "/dev/sdX" till disk-ID

Om du gjort misstaget att tilldela din pool diskar med hjälp av disknamn
(/dev/sdX) och i efterhand vill byta till det mer konsekventa disk-ID
finns en enkel lösning, helt utan dataförlust. Gör såhär:

Exportera din pool, poolen tas nu bort från systemet i förberedelse för
"flytten".

`zpool export POOL`

Importera poolen från /dev/disk/by-id.

`zpool import -d /dev/disk/by-id POOL`

Verifiera att poolen är tillbaks och att diskarna i poolen refereras med
sitt ID istället för "sdX" med `zpool status`.

[Category:Guider](/Category:Guider "wikilink")