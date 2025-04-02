---
title: BIND
permalink: /BIND/
---

BIND är ett open source, flexibelt och fullt utrustat DNS-system.

Mjukvaran består av tre delar:

-   Domain Name Resolver
-   Domain Name Authority server
-   Tools

Installation
------------

`apt-get install bind9 bind9utils bind9-doc dnsutils`

Konfiguration
-------------

### Domain Name Resolver

### Domain Name Authority server

#### Zone transfers

Har man flera servrar kan det vara smidigt att vid ändring i en zone att
den syncas över till de andra bind servarna.

Skapa en ACL på master servern i `named.conf.local`.

`acl slave {`
`   172.22.0.0/24;`
`   172.22.0.10;`
`};`

I zonen lägg till följande:

`zone "hackernet.se" {`
`   ....`
`   type master;`
`   allow-transfer { slave; };`
`};`

På din slav server lägg till följande i zonen:

`zone "hackernet.se {`
`   ....`
`   type slave;`
`   masters { 192.168.1.10; };`
`}`

Starta sedan om tjänsten på båda servarna.

##### TSIG

Transaction Signature (TSIG) kan användas för att säkra upp zone
transfern.

Starta med att generera nykeln som ska användas på master DNS'n.

`dnssec-keygen -a HMAC-SHA512 -b 512 -n HOST -r /dev/urandom tsigkey`

Två filer kommer att skapas. I private filen finns nykeln efter
**Key:**. Kopiera nykeln och skapa filen:

`vim /etc/bind/named.conf.tsigkeys`

Med följande info:

`key "my-tsig" {`
` algorithm HMAC-SHA512;`
` secret "`<key>`";`
`};`

Säg till bind att läsa in filen. Lägg till följande i slutet på
**named.conf**:

`include "/etc/bind/named.conf.tsigkeys";`

För att säkra upp en zone skriv följande.

` zone "hackernet.se" {`
`   ....`
`   allow-transfer { key "my-tsig"; };`
`};`

Starta sedan om tjänsten.

På DNS slaven skapa samma tsigkeys fil:

`vim /etc/bind/named.conf.tsigkeys`

Och kopiera in samma innehåll från master servern, men lägg till
följande i slutet. För att säga till vilken nykel den ska använda:

`.....`
`server 192.168.2.254 {`
` keys { my-tsig; };`
`};`

Lägg till följande rad i **/etc/bind/named.conf**

`include "/etc/bind/named.conf.tsigkeys";`

Och starta om tjänsten. Zone transfer ska nu funka, för att prova köra
följande på slaven.

`dig @{master-dns-ip} hackernet.se axfr`

Om du fick följande error:

`; <<>> DiG 9.8.4-rpz2+rl005.12-P1 <<>> @ns1 hackernet.se axfr`
`; (1 server found)`
`;; global options: +cmd`
`; Transfer failed.`

Så visar det att en zone transfer gick inte att köra utan en tsig nykel.

För att använda tsig nykeln kör följande kommando:

`dig @{master-dns-ip} hackernet.se axfr -k /etc/bind/named.conf.tsigkeys`

SRV record
----------

Med hjälp av service record(**SRV**) så kan man peka ut på vilken port
och bakom vilket hostnamn en tjänst körs tex LDAP, SIP, Lync.

Ett SRV record ser ut på följande sätt.

`_service._proto.name. TTL class SRV priority weight port target.`

-   service: namnet på tjänsten.
-   proto: vilket transport protokoll som ska användas, vanligast är TCP
    eller UDP.
-   name: vilket domän namn recordet är till för.
-   TTL: time to live.
-   class: standard DNS klass. Denna är alltid **IN**.
-   priority: hosten med lägst prioritet används i första hand.
-   weight: används vid lastbalansering. Om 2 hostar har samma priority
    så har den host med högre weight större chans att bli vald.
-   port: port på tjänsten.
-   target: hostnamnet på servern.

### LDAP autodiscovery

Skriv följande i din zonefil.

`_ldap._tcp.hackernet.se.   IN      SRV     10 0 389 ldap1.hackernet.se.`
`_ldap._tcp.hackernet.se.   IN      SRV     20 0 389 ldap2.hackernet.se.`

Dynamic DNS
-----------

### ISC DHCP

Sätt upp DDNS så att lokala klienter som får IP från en dhcp server
uppdaterar din lokala forward och reverse zone.

##### Generera en nykel

`dnssec-keygen -a HMAC-MD5 -b 128 -r /dev/urandom -n USER DDNS_UPDATE`

Öppna filen **\*.private** och kopiera allt efter **Key:**

Skapa en ny fil som heter **ddns.key** som ser ut som följande och
kopiera in texten från **\*.private** filen:

`key DDNS_UPDATE {`
`        algorithm HMAC-MD5.SIG-ALG.REG.INT;`
`        secret "`<key>`";`
`};`

Kopiera sedan **ddns.key** filen till bind mappen och dhcp serverns
mapp.

`install -o root -g bind -m 0640 ddns.key /etc/bind/ddns.key`
`install -o root -g root -m 0640 ddns.key /etc/dhcp/ddns.key`

##### Bind konfiguration

Lägg in följande rad i din **named.conf.local** fil:

`include "/etc/bind/ddns.key";`

Lägg till denna raden **allow-update { key DDNS_UPDATE; };** i varje
zone som ska uppdateras.

`zone "example.org" {`
`     type master;`
`     notify no;`
`     file "/var/cache/bind/db.example.org";`
`     allow-update { key DDNS_UPDATE; };`
`};`
`zone "1.168.192.in-addr.arpa" {`
`     type master;`
`     notify no;`
`     file "/var/cache/bind/db.192.168.2";`
`     allow-update { key DDNS_UPDATE; };`
`};`

##### DHCP konfiguration

Följande globala inställningar behövs i din **dhcpd.conf**' fil:

`option domain-name "example.org";`

`ddns-updates           on;`
`ddns-update-style      interim;`
`ignore                 client-updates;`
`update-static-leases   on;`

**option domain-name:** Specificerar vilket domän namn som delas ut,
används också av DDNS.
**ddns-update-style:** Bör alltid vara interim. Adhoc finns som val
också men är utdaterat.
**client-updates:** Om du använder **allow client-updates** så låter du
klienter registrera sitt domän namn på DNS servern själv. Default är
**ignore client-updates**.
**update-static-leases:** Default så uppdaterar inte DHCP-servern DNS
rader som är statiska leases.

Lägg också till följande rader i din **dhcpd.conf** fil:

`include "/etc/dhcp/ddns.key";`

`zone example.org. {`
`  primary 127.0.0.1;`
`  key DDNS_UPDATE;`
`} `

`zone 1.168.192.in-addr.arpa. {`
`  primary 127.0.0.1;`
`  key DDNS_UPDATE;`
`}`

Se till att bind har skrivrättigheter i mappen där zone filen finns
sparad annars kan den inte uppdatera.

Starta sedan om tjänsterna.

`/etc/init.d/isc-dhcp-server restart`
`/etc/init.d/bind9 restart`

Tips n Trix
-----------

### Chroot

För att öka säkerheten bör man lägga tjänsten i en chroot-miljö.

`yum install bind-chroot -y`
`service named restart`

### Serial number reset

Har man råkat sätta för högt serienummer i en zon kan man resetta det
med följande metod. Sätt serienumret till:

`4294967295`

Låt det propagera till slavarna och sedan kan man sätta vad man vill.

### Statistics

Vill du se lite statistik på din DNS-server kan konfa följande och sedan
surfa in på <http://><IP>:8080

`acl "trusted" {`
`  192.168.1.0/24;`
`};`
`statistics-channels { `
`  inet *  port 8080 allow { trusted; }; `
`};`

### Response Rate Limiting

Tools
-----

Kör igenom toolsen för att få en känsla för dem.
Short output

`dnsget hackernet.se`
`dig hackernet.se +short`

Kolla SOA på alla namnservrar

`dig hackernet.se +nssearch`

Kolla om records finns mot wordlist

`dnsmap hackernet.se`

Kolla version på DNS-server

`ldns-chaos hackernet.se`

Monitor queries

`sudo dnstop eth0`

Capture queries

`sudo dnscap -g`

Visualisera

`sudo tcpdump -i eth0 -w dnsdump.pcap port 53`
`dnspktflow dnsdump.pcap`
`eog out.png`

### rndc

Är ett program för att uppdatera dnservern med nya zoner eller uppdatera
befintliga zoner. Fördelen med att använda rndc är att man behöver inte
ladda om alla zoner om man bara gör ändringar i en zone. Har man många
stora zoner kan DNS sluta svara under några sekunder.

`rndc reconfig - Används om du gjort någon ändring i .conf filerna eller för att läsa in nya zoner. Den kommer inte bry sig om du gjort någon ändring i nån zone fil.`
`rndc reload - För att ladda om alla zone filer.`
`rndc reload `<zone name>` - För att enbart ladda om den zonen du gjort en ändring på.`

### dnstracer

[Dnstracer](/Dnstracer "wikilink") följer alla dns servrar tills man
hittar den servern man letar efter.

`dnstracer -o4s . hackernet.se`

### Felsök

Se hur långt i resolve-processen det funkar

`dig hackernet.se +trace`

Kolla efter syntax-errors alla inladdade zoner

`named-checkconf -z`

DNSSEC
------

Known errors
------------

### Journal out of sync error

Om man har en dynamisk zone som uppdateras från tex en DHCP och denna
zonen skulle uppdateras manuellt så kommer den inte längre laddas
korrekt och ger följande meddelande.

`zone hackernet.se/IN: journal rollforward failed: journal out of sync with zone`
`zone hackernet.se/IN: not loaded due to errors.`

Lösningen är att ta bort **.jnl** filen som tillhör zonen. Efter det är
det bara att starta om BIND.

Om du skulle behöva uppdatera en zone manuellt börja med att frysa
zonen.

`rndc freeze hackernet.se`
**`(ändra`` ``i`` ``zonefilen)`**
`rndc reload hackernet.se`
`rndc thaw hackernet.se`

[Category:Guider](/Category:Guider "wikilink")