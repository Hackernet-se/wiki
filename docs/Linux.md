---
title: Linux
permalink: /Linux/
---

**Linux** är ett Unix-liknande operativsystem som till största delen,
och i några varianter helt, består av fri programvara.

Tools
=====

<DynamicPageList> category = Tools ordermethod = sortkey order =
ascending </DynamicPageList>

Distar
======

<DynamicPageList> category = Distar ordermethod = sortkey order =
ascending </DynamicPageList>

Tips'n'trix
===========

#### Skapa ny disk

Skapa en volume group av en disk.

`vgcreate cs_log02_data /dev/sdb`

Skapa en logical volume av volume groupen du skapa.

`lvcreate -l 100%FREE -n logs cs_log02_data`
`mkfs.xfs /dev/cs_log02_data/logs`

Skapa en folder och mounta nya disken.

`mkdir -p /data/logs`
`mount /dev/cs_log02_data/logs /data/logs`

Se till att mounten är permanenet när servern rebootar.

`echo "/dev/mapper/cs_log02_data-logs /data/logs                       xfs     defaults        0 0" >> /etc/fstab`

#### Expandera disk

`Scanna om disken du vill expandera efter du utökat i exempelvis vmware.`
`echo 1>/sys/class/block/sdc/device/rescan`
`fdisk -l kolla så den är utökad`
`Utöka PVn`
`pvresize /dev/sdc`
`utöka lv lvextend -l +100%FREE /dev/mapper/datavg`
`expandera volymen med.`
`xfs_growfs /dev/mapper/datavg`

#### Skapa egna selinux med grep och audit2allow.

Kommando

`cat /var/log/audit/audit.log |grep postgres_expo |grep denied |audit2allow`

Resultat som visar vad det är du skapar en regel på

`#============= init_t ==============`
`allow init_t postgresql_port_t:tcp_socket name_connect;`

Kommando

`cat /var/log/audit/audit.log |grep postgres_expo |grep denied |audit2allow -M postgres`

Resultat som bara visar vad du skall köra för att implementera selinux
regeln ovan

`******************** IMPORTANT ***********************`
`To make this policy package active, execute:`
`semodule -i postgres.pp`

kommando

`semodule -i postgres.pp`

#### Ansluta till trådlöst nätverk.

`nmcli d wifi connect `<SSID>` password `<password>` iface wlan0`

#### Ta reda på om det är något lokalt prestanda eller kapacitetsproblem med maskinen.

Finns på Github och [PyPI](/Python#PIP "wikilink")

`glances `

#### Ta reda på publik IP du har

`wget `[`http://ipinfo.io/ip`](http://ipinfo.io/ip)` -qO -`

#### Testa hårdvaruaccelerering

`openssl speed -evp AES256`

#### Speedtest mot internet med cli

`wget -O speedtest-cli `[`https://raw.github.com/sivel/speedtest-cli/master/speedtest_cli.py`](https://raw.github.com/sivel/speedtest-cli/master/speedtest_cli.py)
`chmod +x speedtest-cli`
`./speedtest-cli --simple`

#### Lista filer efter storlek

`for i in T G M K; do du -hsx * | grep "[0-9]$i\b" | sort -nr; done 2>/dev/null`

#### Summera alla filer i en mapp och printa storleken.

`du -hs *`

#### Restricted Shell

`useradd[mod] -s /usr/sbin/scponly user1`

#### Process Run Time

`ps -p PID -o etime=`

#### Skydda mot SYN flood

`ss -a | grep SYN-RECV | awk '{print $4}' | awk -F":" '{print $1}' | sort | uniq -c | sort -n`

`sudo netstat -antp | grep SYN_RECV|awk '{print $4}'|sort|uniq -c | sort -n`

#### Parallellpinga IP-adresser från fil

`echo $(cat iplist.txt) | xargs -n 1 -P0 ping -w 1 -c 1`

#### Kolla vilken tjänst som vanligtvis ligger på vilken port, t.ex.

`cat /etc/services | grep mysql`

#### Kör en filesystem check vid nästa uppstart

`touch /forcefsck`

#### Kolla distinfo

`lsb_release -a`
`eller`
`cat /etc/*release`

#### Titta på senaste uppstart grafiskt

`systemd-analyze plot > plot.svg`

#### Kolla vad ett kommando kör för systemfrågor. Väldigt användbart vid felsökning.

`strace `<kommando>

#### Kör ett kommando tex 1 gång i sekunden. (Default 2 sekunder)

`watch -n 1 date`

#### Kopiera directory-struktur utan att kopiera filer

`rsync -a -f"+ */" -f"- *" source/ destination/`

#### Lista hårddiskar, partitioner och RAID.

`lsblk`

#### Simpelt prestandatest av hårddiskar

`dd if=/dev/zero of=(fil på disken/raiden) bs=1G count=1 oflag=dsync`

#### Packa upp initrd.

`gunzip -dc ../initrd | cpio -idmuv`

#### Packa ner initrd.

`find . -print |cpio -o -H newc | xz --format=lzma > ../initrd`

#### Byt namn på alla filer och mappar från uppercase till lowercase i en mapp.

**Upper till lower**.

`for i in *; do mv "$i" "$(echo $i|tr A-Z a-z)"; done`

**Lower till upper**.

`for i in *; do mv "$i" "$(echo $i|tr a-z A-Z)"; done`

#### Sök efter en text i alla filer i en mapp

`grep -r "string" .`

#### Kollar antal dagar det är kvar på ett certifikat

``` bash
 remote_cert_remaining_days() { cert_remaining_time=$(date -d "$(openssl s_client -connect $1 2>/dev/null </dev/null | openssl x509  -enddate -noout | cut -d'=' -f2)" "+%s");  current_time=$(date "+%s"); echo remaining $((($cert_remaining_time - $current_time) / 60 / 60 / 24)) days; }
```

`remote_cert_remaining_days fqdn:443`

#### Räkna ut option 121 för DHCP

För att kunna skicka ut fler routes via DHCP behöver man skriva på ett
visst sätt. Följande sida kan hjälpa till med det: [Route
calculator](https://www.nboquestal.fr/outils/route-calculator/)

Intervjufrågor
==============

Ska du på arbetsintervju för ett linuxjobb? Prepare your anus!

1.  Vad är det för skillnad på en vanlig fil och ett directory?
2.  Vad är en i-node?
3.  Vad är det för skillnad på hard och soft links? Vad händer om man
    tar bort källan för länken?
4.  Vad är en process och vad består den logiskt av?
5.  Vad är det för skillnad på mtab och fstab?
6.  Vad gör rm-kommandot? (utan växlar)
7.  Vad är det för skillnad på kill och kill -9?
8.  Villka process states finns det?
9.  Vad är det för skillnad på process och thread?
10. Vad är en Socket?
11. Vad är Huge Pages och vad används de till?
12. Hur frigör man cacheat minne utan att reboota systemet?
13. Vad är det för skillnad på chmod och setfacl?
14. Vad är Memory Overcommit?
15. Vad är system load average som visas av uptime-kommandot?
16. Vad finns det för för- och nackdelar med kernel kontra user space?
17. Vad är runlevel?
18. Vad är det för skillnad på TTY och PTS?
19. Du är fast på en öde ö och får bara använda ett enda kommando,
    vilket väljer du?

### Svar

Kommer inom sinom tid, har du svar bidra gärna