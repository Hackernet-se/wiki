---
title: Mdadm
permalink: /Mdadm/
---

mdadm är ett öppet verktyg för att skapa, hantera och monitorera
md-raids i Linux. De flesta Debian och Redhat-baserade system har
paketet installerat per default men bör annars finnas i officiella repos
om det skulle fattas.

De flesta kommersiella NASar som tex Synology använder sig av Mdadm för
att hantera deras raids, detta gör det möjligt att flytta över raids och
synca till och från olika enheter som har stöd för verktyget.

Installation
------------

sudo apt-get install mdadm
sudo yum install mdadm

Raidtyper
---------

Mdadm har stöd för standard raidtyper såsom:

-   Raid 0
-   Raid 1
-   Raid 4
-   Raid 5
-   Raid 6
-   Raid 10


Mdadm har även stöd för "**non-raid configurations**" (Tänk JBOD?):
\* Linear – sammanfogar ett antal enheter till en enda stor MD-enhet.

-   Multipath – ger flera vägar med failover till en enda enhet.
-   Faulty – skapar ett antal felscenarior (tex läs/skrivfel) för test.
-   Container – en grupp av enheter som hanteras som en enda enhet, där
    man kan bygga RAID-system.

WIP!

-   Tweaks
-   create, assemble, monitor, build, grow, manage
-   exempel

Create
------

Att skapa en ny mdadm är är väldigt strait-forward. Du skapar en array,
väljer vilka diskar du ska slå ihop och sedan till vilken raidtyp.

När du bygger ihop din raid så kan du köra `cat /cat/mdstat` för att få
fram status från bygget.

### Skapa array:

`mdadm --create /dev/md`**`X`**

`mdadm --monitor /dev/md`**`X`**

### Skapa Raid-0

`mdadm --create --verbose /dev/md`**`X`**` --level=stripe --name `*`'XXX`` `**`--raid-devices=`**`X`*`' /dev/sd`**`X`**`1 /dev/sd`**`X`**`1`

### Skapa raid-1

`mdadm --create --verbose /dev/md'''X '''--level=mirror --name `*`'XXX`` `**`--raid-devices=`**`X`*`' /dev/sd`**`X`**`1 /dev/sd`**`X`**`1`

...Med spare:

`mdadm --create --verbose /dev/md`**`X`**`--level=mirror --name `*`'XXX`` `**`--raid-devices=`**`X`**`/dev/sd`**`X`**`1`**` `**`/dev/sd`**`X`**`1`` ``--spare-device=1`` ``/dev/sd`**`X`*`'`

### Skapa Raid-4/5/6

`mdadm --create --verbose /dev/md`**`X`**` --level=`**`4/5/6`**` --name `*`'XXX`` `**`--raid-devices=`**`X`*`' /dev/sd`**`X`**`1 /dev/sd`**`X`**`1 /dev/sd`**`X`**`1 --spare-devices=`**`X`**` /dev/sd`**`X`**`1`

### Skapa Raid-10

`mdadm --create --verbose /dev/md`**`X`**` --level raid10 --name `**`XXX`**` --raid-devices=`**`X`**` /dev/sd`**`X`**`1 /dev/sd`**`X`**`1 /dev/sd`**`X`**`1 /dev/sd`**`X`**`1`

### Spara din raid och skapa filsystem

Kolla i mdastat`cat /cat/mdstat`f ör att se om din raid är färdigbyggd
och för att se status.

**OM** din raid är färdigbyggd så kör vi följande kommando för att spara
ner vår conf. Om du kör någon annan dist, kolla vart din mdadm.conf är
placerad och skriv till den. '''Detta får inte göras förens din raid är
färdigbyggd!! '''

**RHEL/CentOS/Fedora:**

`mdadm --detail --scan >> /etc/mdadm.conf`

Nu kan vi skapa ett filsystem på vår raid

**ext4:**

`mkfs -t ext4ext4 /dev/`md'''X '''

**XFS:**

För XFS behöver du speca SU som är samma som mdadm-raidens chunk size.
Föra att få fram chunk size kan du köra `mdadm --detail /dev/md`**`X`**

Du behöver också speca sw, vilket är hur många data-diskar du har (ej
spares etc).

-   RAID 0 med 2 diskar: 2 data diskar (n)
-   RAID 1 med 2 diskar: 1 data disk (n/2)
-   RAID 10 med 10 diskar: 5 data diskar (n/2)
-   RAID 5 med 6 diskar (inga spares): 5 data diskar (n-1)
-   RAID 6 med 6 diskar (inga spares): 4 data diskar (n-2)

`mkfs -t xfs -d su=`**`X`**`k -d sw=`**`X`**` /dev/md`**`X`**

Tex: raid 5 med 4 diskar med en chunksize på 64k:

`mkfs -t xfs -d su=64k -d sw=3 /dev/md`**`X`**

Flytta en mdadm raid
--------------------

Lättast om du sparar din /etc/mdadm.conf eller ARRAY-rader från konfen
och flyttar med den/dessa till din nya maskin. Skulle inte det fungera
så är det inte hela världen.

Vi börjar med worst-case, du har inte sparat conf eller ARRAY-info som
UUID, namn etc:

1: Installera mdadm på server B och stäng av servern

2: koppla in dina diskar och starta upp servern igen.

3: Kolla så alla diskar är hittade under /dev/. Är alla där så kan du
köra antingen `cat /proc/mdstat` eller
`ls -l /dev/md/`<RAIDNAMN>` (tabba fram)` för att få fram vilken
md-device din raid ligger som just nu.

4\. Säg att din raid ligger hittad som /dev/md127, kör då
`# mdadm --detail /dev/md127`. När detta körs bör du får fram all info
du behöver. Dvs *'Version, Namn **och** UUID*'.

5\. Kör kommandot:
`echo >> ARRAY /dev/md`**`X`**` metadata=`**`"Version"`**` name=`**`"namn"`**` UUID='''"uuid" '''/etc/mdadm.conf`
'''NOTICE: '''Du får lägga din array vart du vill, även om md127 var där
den hittades så kan du lägga den på tex /dev/md0. Se bara till så att
md0 inte är upptagen. Detta kommando lägger till din "nya" array i
mdadm-confen som läses in varje uppstart.

6\. Reboot och `cat /proc/mdstat` för att se hur din raid bygger ihop
sig.

7\. När raiden har byggt ihop sig så kan du mounta, jag föredrar att
mounta via fstab och UUID. Exempel på fstab conf:

`UUID='''"RaidUUID" ''' /mount/point xfs defaults 0 0`

**OBS** Vet inte om det står något värdefullt här men det kan nog dut
avgöra bättre //Alex

[`http://h3x.no/2011/07/09/tuning-ubuntu-mdadm-raid56`](http://h3x.no/2011/07/09/tuning-ubuntu-mdadm-raid56)

[Category:Tools](/Category:Tools "wikilink")