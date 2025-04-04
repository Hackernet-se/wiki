---
title: AutoFS
permalink: /AutoFS/
---

autofs är ett program för att automatiskt mounta kataloger efter behov
när det behövs. Auto-mounts är endast mountade när de används, och
umountas efter en period av inaktivitet. Mount av en remote share genom
fstab förblir mountad såvida du inte umountar den. Automounting
NFS/Samba-shares sparar bandbredd och ger bättre prestanda jämfört med
statiska mounts genom fstab. fstab kan dessutom orsaka problem om sharen
blir otillgänglig, vilket resulterar i inaktuella mounts. Till exempel
kan filservern du ansluter till krascha eller nätverket kan gå ner.

Installation
------------

`sudo apt-get install autofs`
`sudo yum install autofs`

Konfiguration
-------------

Skapa en mount point eller välj en befintlig katalog, t.ex. /mnt eller
/media. Du kommer att behöva definiera mount points för att ange hur du
ansluter till din nätverksresurs.

`sudo mkdir /nfs-share`
`sudo mkdir /smb-share`

Redigera konfigurationsfilen för autofs:

`sudo nano /etc/auto.master`
`/nfs-share   /etc/auto.nfs-share`
`/smb-share   /etc/auto.smb-share`

Skapa en ny fil i /etc/.

**SMB**

`sudo nano /etc/auto.smb-share`
`filserver -fstype=smbfs,rw,username=buenos,password=nachos,file_mode=0777,dir_mode=0777 ://192.168.0.50/share`

Där "filserver" anger den mapp som ska skapas under /share som host för
dina shares

**NFS**

`sudo nano /etc/auto.nfs-share`
`filserver -fstype=nfs,rw,soft,tcp,nolock 192.168.0.50:/mnt/ProdPool`

Klienten behöver samma ändringar i /etc/default/nfs-common för att
ansluta till en NFSv4-server.

`NEED_IDMAPD = yes`
`NEED_GSSD = no # no är default`

**CIFS**
Får man inte säga, <http://blog.fosketts.net/2012/02/16/cifs-smb/>

### Home Folder

För att mounta hem-mapparna med autofs enkelt och slippa att skapa en
rad för varje användare i autofs filerna eller att man mountar alla hem
mappar som finns på sharen kan man använda sig av wildcard.

`echo * -fstype=nfs,user,auto,rw,async,hard,intr 192.168.1.200:/mnt/zfs/Home/& > /etc/auto.home`
`echo /home /etc/auto.home >> /etc/auto.master`

Där "\*" och "&" är wildcard.

Felsökning
----------

Reboota och försök komma åt din share.

`ls /nfs-share`
`cd /smb-share`

Om det inte fungerar, måste du felsöka. Stoppa autofs demonen

`sudo service autofs stop`

Kör automount i förgrunden med verbose

`sudo automount -f -v`

[Category:Guider](/Category:Guider "wikilink")