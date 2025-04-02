---
title: GlusterFS
permalink: /GlusterFS/
---

GlusterFS är ett open source och skalbart network-attached storage file
system som numera utvecklas av Red Hat. Genom att klustra ihop resurser
(servrar, diskar, filsystem etc.) kan man bygga High-Availability
storage. Varje directory som ska lagra data kallas brick och med bricks
bygger man volymer. Volymer kan spänna över flera servrar och
kommunikation görs med TCP (eller
[InfiniBand](https://en.wikipedia.org/wiki/InfiniBand)). Det finns
Gluster Native Client för t.ex. linuxhostar annars går det att dela ut
en volym med klassiska protokoll som [NFS](/NFS "wikilink").

Det finns olika typer av volymer. Dessa går även att kombinera för att
skapa en distributed-replicated volume.

-   **Distributed Mode:** kombinera alla tillgängliga storage-resurser
    till en volym.
-   **Replicated Mode:** spegla datan (mirror) mellan resurser, likt
    RAID 1. Synchronous replication.

Lägger man till en ny tom brick till en Distributed volym med mycket
data kan man balansera ut det med kommandot **gluster volume rebalance
VOLNAME start**. GlusterFS har inbyggd self-heal funktion i replicated
mode, dvs om en brick går offline och filer modifieras så synkas det upp
när den kommer tillbaka.

Installation
============

`sudo dnf/apt-get install glusterfs-server`
`systemctl status glusterfs-server`

**Klient**

`sudo dnf/apt-get install glusterfs-client`

**Version**

`glusterfsd --version`

Konfiguration
=============

För att klustra noder måste man peera och lägga till enheter till
trusted server pool. Detta går även göra med hostnamn.

`sudo gluster peer probe 10.0.0.11`
`gluster peer status`

### Volym

Replicated, 2 är antalet noder med datan.

`sudo gluster volume create gluster-vol replica 2 10.0.0.10:/data 10.0.0.11:/data`
`sudo gluster volume start gluster-vol`

Vitlista klienter baserat på IP-adresser.

`sudo gluster volume set gluster-vol auth.allow 10.0.0.*,10.5.5.10`

Verify

`sudo gluster volume status`
`sudo gluster volume info  `

### Klient

`mount.glusterfs 10.0.0.10:/data /mnt/glusterfs`
`df -h`

Geo-replication
---------------

GlusterFS är designat för datacenter men vill man över t.ex. ett WAN
(high latency) bör man använda geo-replication. Då används istället
asynchronous och inkrementell replikering. Ena sidan är master och andra
slave. Klockorna ska vara synkade och [NTP](/NTP "wikilink") bör
användas.

`gluster volume geo-replication [SOURCE_DATASTORE] [REMOTE_SERVER]:[REMOTE_PATH] start`

[Category:Guider](/Category:Guider "wikilink")