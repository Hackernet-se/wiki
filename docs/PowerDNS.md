---
title: PowerDNS
permalink: /PowerDNS/
---

[Category:Guider](/Category:Guider "wikilink") PowerDNS är en open
source DNS som skapades i slutet av 1990 talet. PowerDNS är väldigt
anpassningsbart för man är inte bunden att använda enbart text filer
utan man kan ha sina records i databaser också. Det har gjort att
PowerDNS har blivit enkelt att integrera i andra tjänster som tex
[PhpIPAM](/PhpIPAM "wikilink") och det finns ännu fler olika web
interface på nätet. PowerDNS har också något dom kallar för en
supermaster, som gör att nya zoner som skapas automatiskt finns på alla
slavar. PowerDNS har också ett väldigt bra DNSSEC stöd och driver 90% av
Europas DNSSEC domäner.

PowerDNS har delats upp i två delar, **[PowerDNS Authoritative
Server](https://www.powerdns.com/auth.html)** och **[PowerDNS
Recursor](https://www.powerdns.com/recursor.html)**.

PowerDNS Authoritative Server
=============================

Authoritative server är den sort DNS server som har hand om en domän.
Klienter frågar denna servern för att få svar på sina DNS uppslag.

Termer
------

**Native replication**: PowerDNS kommer inte skicka ut eller agera vid
en DNS update notification. Utan tar förgivet att backend systemet tar
hand om replikeringen. Att låta databaser ta hand om replication har
visat sig väldigt stabilt enligt PowerDNS även vid dålig anslutning.
Native väljs default på nya zoner.

**Master operation**: PowerDNS skickar ut notifikationer till sina
slavar vid en zone ändring och sköter själv replikeringen till en slav
server.

**Slave operation**: Vid uppstart skickar PowerDNS en request till alla
backends en lista med domäner som nyligen inte kollat om dom ändrats.
Alla domäner som inte har senaste versionen kommer laddas ner.

**Supermaster**: En supermaster automatiskt konfigurerar slavar med nya
zoner när dom skapas. För att det ska fungera krävs bla att slaven vet
om vem som är supermaster, supermastern har ett SOA record i domänen och
att ett NS record måste finnas som stämmer överens med supermastern IP'n
som konfigurerats på slaven.

-   <btn data-toggle="tab" class="">\#tab1\|CentOS 7</btn>
-   <btn data-toggle="tab" class="">\#tab2\|Ubuntu 16.04</btn>

<div class="tab-content">
<div id="tab1" class="tab-pane fade in active">

Lägg till PowerDNS repo och installera epel samt yum priority plugin.

`yum install epel-release yum-plugin-priorities`
`curl -o /etc/yum.repos.d/powerdns-auth-master.repo `[`https://repo.powerdns.com/repo-files/centos-auth-master.repo`](https://repo.powerdns.com/repo-files/centos-auth-master.repo)

Installera sedan PowerDNS servern.

`yum install pdns`

</div>
<div id="tab2" class="tab-pane fade">

Börja med att lägga till PowerDNS repot:

`echo "deb [arch=amd64] `[`http://repo.powerdns.com/ubuntu`](http://repo.powerdns.com/ubuntu)` xenial-auth-master main" > /etc/apt/sources.list.d/pdns.list`

Skapa sedan **/etc/apt/preferences.d/pdns** med följande innehåll:

`Package: pdns-*`
`Pin: origin repo.powerdns.com`
`Pin-Priority: 600`

Kör sedan dessa kommandon:

`curl `[`https://repo.powerdns.com/CBC8B383-pub.asc`](https://repo.powerdns.com/CBC8B383-pub.asc)` | sudo apt-key add - &&`
`sudo apt-get update`

Installera sedan PowerDNS servern.

`sudo apt-get install pdns-server`
`  `

</div>
</div>

Välj vilken backend du vill använda, olika backends har olika stöd se
följande [lista](https://doc.powerdns.com/md/authoritative/).(Bind stöd
är inbyggt)

`pdns-backend-geoip - geoip backend for PowerDNS`
`pdns-backend-ldap - LDAP backend for PowerDNS`
`pdns-backend-lua - Lua backend for PowerDNS`
`pdns-backend-mydns - MyDNS compatibility backend for PowerDNS`
`pdns-backend-mysql - generic MySQL backend for PowerDNS`
`pdns-backend-pgsql - generic PostgreSQL backend for PowerDNS`
`pdns-backend-pipe - pipe/coprocess backend for PowerDNS`
`pdns-backend-remote - remote backend for PowerDNS`
`pdns-backend-sqlite3 - sqlite 3 backend for PowerDNS`
`pdns-backend-tinydns - tinydns compatibility backend for PowerDNS`

Konfiguration
-------------

**10.0.0.1** Supermaster.hackernet.se

**10.0.0.2** ns1.hackernet.se

**10.0.0.3** ns2.hackernet.se

I guiden har vi valt att använda [MySQL](/MySQL "wikilink") som backend.
Och skapa en supermaster server som låter PowerDNS sköta replikeringen.

### Master

Lägg in följande i `/etc/powerdns/pdns.conf`:

`allow-recursion=0.0.0.0/0`
`allow-axfr-ips=10.0.0.2/32,10.0.0.3/32`
`also-notify=10.0.0.2,10.0.0.3`
`config-dir=/etc/powerdns`
`daemon=yes`
`disable-axfr=no`
`guardian=yes`
`local-address=0.0.0.0`
`local-port=53`
`log-dns-details=on`
`loglevel=3`
`module-dir=/usr/lib/x86_64-linux-gnu/pdns/`
`master=yes`
`slave=no`
`setgid=pdns`
`setuid=pdns`
`socket-dir=/var/run`
`version-string=powerdns`
`include-dir=/etc/powerdns/pdns.d`
`launch=gmysql`

I **/etc/powerdns/pdns.d** skapa filen `pdns.local.gmysql.conf`. Om
filen redan fanns gå till nästa steg.

`gmysql-host=localhost`
`gmysql-port=`
`gmysql-dbname=pdns`
`gmysql-user=pdns`
`gmysql-password=`<PaSSw0RD>
`gmysql-dnssec=yes`

Om filen skulle finnas med ett lösenord redan i så är det troligt att
under installationen så skapades det en databas och fylldes med default
tables. Ifall du behöver skapa tables själv så kör följande MySQL
kommando för att skapa dom.

<div class="toccolours mw-collapsible mw-collapsed" style="width:800px">

MySQL kommandon.

<div class="mw-collapsible-content">

``` mysql
CREATE TABLE domains (
  id                    INT AUTO_INCREMENT,
  name                  VARCHAR(255) NOT NULL,
  master                VARCHAR(128) DEFAULT NULL,
  last_check            INT DEFAULT NULL,
  type                  VARCHAR(6) NOT NULL,
  notified_serial       INT DEFAULT NULL,
  account               VARCHAR(40) DEFAULT NULL,
  PRIMARY KEY (id)
) Engine=InnoDB;

CREATE UNIQUE INDEX name_index ON domains(name);


CREATE TABLE records (
  id                    INT AUTO_INCREMENT,
  domain_id             INT DEFAULT NULL,
  name                  VARCHAR(255) DEFAULT NULL,
  type                  VARCHAR(10) DEFAULT NULL,
  content               VARCHAR(64000) DEFAULT NULL,
  ttl                   INT DEFAULT NULL,
  prio                  INT DEFAULT NULL,
  change_date           INT DEFAULT NULL,
  disabled              TINYINT(1) DEFAULT 0,
  ordername             VARCHAR(255) BINARY DEFAULT NULL,
  auth                  TINYINT(1) DEFAULT 1,
  PRIMARY KEY (id)
) Engine=InnoDB;

CREATE INDEX nametype_index ON records(name,type);
CREATE INDEX domain_id ON records(domain_id);
CREATE INDEX recordorder ON records (domain_id, ordername);


CREATE TABLE supermasters (
  ip                    VARCHAR(64) NOT NULL,
  nameserver            VARCHAR(255) NOT NULL,
  account               VARCHAR(40) NOT NULL,
  PRIMARY KEY (ip, nameserver)
) Engine=InnoDB;


CREATE TABLE comments (
  id                    INT AUTO_INCREMENT,
  domain_id             INT NOT NULL,
  name                  VARCHAR(255) NOT NULL,
  type                  VARCHAR(10) NOT NULL,
  modified_at           INT NOT NULL,
  account               VARCHAR(40) NOT NULL,
  comment               VARCHAR(64000) NOT NULL,
  PRIMARY KEY (id)
) Engine=InnoDB;

CREATE INDEX comments_domain_id_idx ON comments (domain_id);
CREATE INDEX comments_name_type_idx ON comments (name, type);
CREATE INDEX comments_order_idx ON comments (domain_id, modified_at);


CREATE TABLE domainmetadata (
  id                    INT AUTO_INCREMENT,
  domain_id             INT NOT NULL,
  kind                  VARCHAR(32),
  content               TEXT,
  PRIMARY KEY (id)
) Engine=InnoDB;

CREATE INDEX domainmetadata_idx ON domainmetadata (domain_id, kind);


CREATE TABLE cryptokeys (
  id                    INT AUTO_INCREMENT,
  domain_id             INT NOT NULL,
  flags                 INT NOT NULL,
  active                BOOL,
  content               TEXT,
  PRIMARY KEY(id)
) Engine=InnoDB;

CREATE INDEX domainidindex ON cryptokeys(domain_id);


CREATE TABLE tsigkeys (
  id                    INT AUTO_INCREMENT,
  name                  VARCHAR(255),
  algorithm             VARCHAR(50),
  secret                VARCHAR(255),
  PRIMARY KEY (id)
) Engine=InnoDB;

CREATE UNIQUE INDEX namealgoindex ON tsigkeys(name, algorithm);
```

</div>
</div>

Ta bort `pdns.simplebind.conf` om du inte tänkt använda bind som
backend.

Starta sedan om PowerDNS tjänsten.

`service pdns restart`

### Slave

Gör exakt samma på slaven med databasen fast lägg in följande i
`pdns.conf` istället:

`allow-recursion=0.0.0.0/0`
`config-dir=/etc/powerdns`
`daemon=yes`
`disable-axfr=yes`
`guardian=yes`
`local-address=0.0.0.0`
`local-port=53`
`log-dns-details=on`
`loglevel=3`
`module-dir=/usr/lib/x86_64-linux-gnu/pdns/`
`master=no`
`slave=yes`
`slave-cycle-interval=60`
`setgid=pdns`
`setuid=pdns`
`socket-dir=/var/run`
`version-string=powerdns`
`include-dir=/etc/powerdns/pdns.d`
`launch=gmysql`

Slaven kommer fråga supermastern efter ny zone update var 60 sekund.
Vanligast är att mastern skickar ut en notifikation till slaven men om
det skulle vara problem med anslutningen under den tiden så kommer
slaven fråga mastern när dom kan nå varandra igen.

Lägg till en supermaster för slaven.

Logga in på databasen med:

`mysql -u pdns -p`

Byt till databasen:

`USE pdns;`

Lägg in en rad i supermasters table:

`insert into supermasters values ('10.0.0.1', 'supermaster.hackernet.se', 'admin');`

Lämna MySQL:

`exit;`

Starta om PowerDNS:

`service pdns restart`

Skapa zone
----------

Skapa en zone med hjälp av **pdnsutil**:

`pdnsutil create-zone hackernet.se supermaster.hackernet.se`

Lägg till några **A** record:

`pdnsutil add-record hackernet.se supermaster A 10.0.0.1`
`pdnsutil add-record hackernet.se ns1 A 10.0.0.2`
`pdnsutil add-record hackernet.se ns2 A 10.0.0.3`

Lägg till fler **NS** record:

`pdnsutil add-record hackernet.se @ NS ns1.hackernet.se`
`pdnsutil add-record hackernet.se @ NS ns2.hackernet.se`

Ändra zonen från native zone till master zone.

`pdnsutil set-kind hackernet.se master`

Verifiera att zonen är master:

`pdnsutil show-zone hackernet.se`

Skicka ut en notifikation med mastern eller vänta tills slaven själv
hämtar zonen:

`pdns_control notify hackernet.se`

Säkra upp zonetransfer
----------------------

Man kan säkra upp zonetransfer med hjälp av en TSIG nykel.

Börja med att generera en TSIG nyckel på master servern.

`pdnsutil generate-tsig-key tsig-transfer hmac-sha512`

Aktivera sedan nykel på det zoner du vill säkra upp.

`pdnsutil activate-tsig-key hackernet.se tsig-transfer master`

Lista sedan TSIG nykeln så du kan kopiera den till slaven.

`pdnsutil list-tsig-keys`

Importera nyckeln på slaven.

`pdnsutil import-tsig-key tsig-transfer hmac-sha512 'Långsuperhackerkod'`

Aktivera sedan TSIG nykeln på samma zoner som på mastern.

`pdnsutil activate-tsig-key hackernet.se tsig-transfer slave`

**Att tänka på:** Det är viktigt att nyckeln har samma namn på både
mastern och slaven.

PowerDNS Recursor
=================

Skickar vidare din fråga till olika DNS servrar tills den hittar svaret.

Installation
------------

**Debian/Ubuntu**

`apt-get install pdns-recursor`

Konfiguration
-------------

Recursor är väldigt simpelt att konfigurera upp. Om man vill köra
recursor och authoritative på samma server så behöver man byta vilken
port recursor lyssnar på. Och sedan skicka vidare svar från
authoritative servern som den inte kan svara på.

**recursor.conf**

`forward-zones=8.8.8.8,8.8.4.4`
`trace=on`

### Recursor och authoritative

Lägg till följande rad i **pdns.conf**:

`recursor=127.0.0.1:5678`

Och ändra vilken port recursor lyssnar på i **recursor.conf**:

`local-port=5678`

Var noga med att peka på rätt port så att du inte pekar tillbaka på
authoritative servern för då kommer man få en loop.

DNSSEC
======

DNSSEC är en funktion som signerar DNS-uppslagningar med krypto nycklar
så att man kan säkerställa att det svaret man fått kommit från rätt
källa, och inte manipulerats på vägen. Med DNSSEC skyddas du från bland
annat cacheförgiftning och pharming som är dom vanligaste attackerna.

För att sätta på DNSSEC:

`pdnsutil secure-zone ZONE`

För att stänga av DNSSEC:

`pdnsutil disable-dnssec ZONE`

Kör sedan följande kommando för visa dina DS record:

`pdnsutil show-zone ZONE`

Outputen du är intresserad av är i slutet och ser ut som följande:

`...`
`DS = hackernet.se. IN DS 17379 13 1 75a7f4a06792509298bfb0996df3614b129a6570 ; ( SHA1 digest )`
`DS = hackernet.se. IN DS 17379 13 2 c72f7424c86a46866499ae284bec1b55095ca32e0f6955a9a9ba21df5d010d57 ; ( SHA256 digest )`
`...`

Formatet för ett DS record är:

`DS = `<zone name>` IN DS `<key tag>` `<dnskey algo>` `<digest type>` `<key digest>

Det din domän återförsäljare kommer vara intresserad av för att kunna
uppdatera din Top-level domain är:

-   Key tag: 17379
-   DNSKEY Algorithm: 13 (ECDSAP256SHA256)
-   Digest Type: 1 (SHA-1)
-   Key Digest: 75a7f4a06792509298bfb0996df3614b129a6570

Dynamic DNS
===========

Gör att en DHCP server automatiskt uppdaterar båda din forward och
reverse zone när den tilldelar en enhet en IP, då slipper man själv
uppdatera zoner.

DDNS stöds bara av följande backends

-   gmysql
-   gpgsql
-   gsqlite3
-   goracle
-   godbc

Börja med att generera en TSIG nykel som kommer användas för att göra
uppdateringen säkrare:

`pdnsutil generate-tsig-key ddns_update hmac-sha512`

Aktivera nykeln på dom domäner du vill uppdatera.

` pdnsutil set-meta hackernet.se TSIG-ALLOW-DNSUPDATE ddns_update`

Tillåt enbart vissa nät att få uppdatera zonen.

`pdnsutil set-meta hackernet.se ALLOW-DNSUPDATE-FROM 192.168.1.0/24`
`pdnsutil set-meta hackernet.se ALLOW-DNSUPDATE-FROM 10.100.0.0/24`

Se till så att mastern skickar en notification till slavarna vid varje
uppdatering. Annars får man vänta tills slaven själv frågar mastern.

`pdnsutil set-meta hackernet.se NOTIFY-DNSUPDATE 1`

Lägg sedan till följande rad i **pdns.conf**

`dnsupdate=yes`

Starta om PowerDNS, för att verifiera att det funkar kan du köra
följande kommando:

`nsupdate <<!`
`server `<ip>` `<port>
`zone hackernet.se`
`update add ddnstest.hackernet.se 3600 A 10.13.37.1`
`key ddns_update `<lång nykel>
`send`
`! `

Om det funkar kommer ett record i hackernet.se zonen att skapas som
heter ddnstest. Repitera på fler domäner samt reverse zoner om sådana
finns. Samma nykel kan användas på alla zoner om man vill.

##### dhcpd

Konfigurera din DHCP server att använda nykeln och det namn du valt på
nykeln i detta fallet **ddns_update**.

Under här kommer ett exempel för [ISC_DHCP](/ISC_DHCP "wikilink").

Skapa en fil som heter ddns.key med följande innehåll under
**/etc/dhcp/**:

`key "ddns_update" {`
`        algorithm hmac-sha512;`
`        secret "`<lång nykel>`";`
`};`

Lägg sedan in följande rader i DHCP conf filen:

`ddns-updates on;`
`ddns-update-style interim;`
`update-static-leases on;`

`ddns-domainname "hackernet.se";`
`ddns-rev-domainname "in-addr.arpa.";`

`include "/etc/dhcp/ddns.key";`
`zone hackernet.se {`
`    primary 127.0.0.1;`
`    key ddns_update;`
`}`

`zone 0.168.192.in-addr.arpa. {`
`    primary 127.0.0.1;`
`    key ddns_update;`
`}`

Byt ut 127.0.0.1 mot din primära dns server.

Starta om DHCP servern.

Tools
=====

Det finns massa olika verktyg för PowerDNS tex kraftiga webinterface och
cli verktyg.

PDNS Manager
------------

Ett enkelt webinterface där du kan skapa nya zoner, records och som har
stöd för att signa certifikat med [Let's
Encrypt](/Let's_Encrypt "wikilink") och ett API.

<https://pdnsmanager.lmitsystems.de/>

Poweradmin
----------

Ett webinterface som också kan skapa zoner och records men har även ett
bättre stöd för användare där man kan ställa in permissions på vilka
domäner som en användare får ändra i. Och har stöd för att LDAP koppla
användare.

<http://www.poweradmin.org/>

pdnsutil
--------

Är ett CLI verktyg för PowerDNS. Där man i stort sett kan göra allt på
zoner tex generera och lägga till tsig nycklar, migrera backend lösning,
benchmarka backend delen och mycket mer.

**Skapa en native zone**:

`pdnsutil create-zone hackernet.se`

**Skapa en native zone med ett NS record**:

`pdnsutil create-zone hackernet.se ns1.hackernet.se`

**Skapa en slave zone där IP'n i slutet är master server**:

`pdnsutil create-slave-zone hackernet.se 10.0.0.1`

**Editera en zone**:

`pdnsutil edit-zone hackernet.se`

**Skapa ett NS record**:

`pdnsutil add-record hackernet.se @ NS ns1.hackernet.se`

**Skapa ett record**:

`pdnsutil add-record hackernet.se ns1 [A/AAAA/MX/CNAME/...] 10.0.0.2`

**Lista alla zoner**:

`pdnsutil list-all-zones`

**Ändra zone operation**:

`pdnsutil set-kind hackernet.se master/native/slave`

**Tillåt alla IP's som är inlagda som en namnserver för domänen att göra
zone transfers**:

`pdnsutil set-meta hackernet.se ALLOW-AXFR-FROM AUTO-NS`

**Öka SOA serial med 1**:

`pdnsutil increase-serial hackernet.se`

pdnscat
-------

pdnscat är ett bash script som hämtar alla records genom PowerDNS API
och gör så att man kan greppa på records. När man filtrerat ner till ett
resultat så kan man välja att SSHa mot det recordet med förinställda
username som root, admin och den användaren du är.

**Curl** och **JQ** behövs för att scriptet ska fungera.

`git clone `[`https://github.com/Hackernet-se/pdnscat`](https://github.com/Hackernet-se/pdnscat)
`./pdnscat arg1 arg2 arg3 ... [f] [a|r|q] ..."`

#### Exempel

<div class="panel-group" id="accordion">

<accordion parent="accordion" heading="Hitta alla DNS servrar.">

    sparco@jumpgate:~$ y ns
    10.240.100.12   A       ns3
    172.22.0.12     A       ns4
    10.240.100.13   A       ns5
    172.22.0.13     A       ns6

</accordion>

<div class="panel-group" id="accordion">

<accordion parent="accordion" heading="SSH till NS5">

    sparco@jumpgate:~$ y ns 5
    10.240.100.13   A       ns5
    sparco@jumpgate:~$ y ns 5 r

    --- IP and hostname ---
    10.240.100.13
    ns5
    ssh root@10.240.100.13

    root@10.240.100.13's password:
    Welcome to Ubuntu 16.04.2 LTS (GNU/Linux 4.4.0-79-generic x86_64)

</accordion>

<div class="panel-group" id="accordion">

<accordion parent="accordion" heading="Filtrera ut alla records från en subdomän.">

    sparco@jumpgate:~$ y rsg f
    10.60.0.50      A       rsg-proxy.hackernet.se.
    10.60.0.4       A       esxispa1-ilo.rsg.hackernet.se.
    10.60.0.5       A       esxispa2-ilo.rsg.hackernet.se.
    10.60.0.6       A       esxispa3-ilo.rsg.hackernet.se.
    10.60.0.16      A       esxispa3.rsg.hackernet.se.
    10.60.0.53      A       foreman.rsg.hackernet.se.
    10.60.0.12      A       ilocz3128ldh5.rsg.hackernet.se.
    10.60.0.5       A       ilocz3128ldje.rsg.hackernet.se.
    10.60.0.6       A       ilocz3128ldjv.rsg.hackernet.se.
    10.60.0.10      A       ilocz3128ldjy.rsg.hackernet.se.
    10.60.0.11      A       ilocz3128ldkb.rsg.hackernet.se.
    10.60.0.4       A       ilocz3128le5v.rsg.hackernet.se.
    10.60.0.7       A       ilocz32025rlt.rsg.hackernet.se.
    10.60.0.9       A       ilocz32025rma.rsg.hackernet.se.
    10.60.0.8       A       iloczj2100hf4.rsg.hackernet.se.

</accordion>

Abbreviation
============

**AXFR**= Är en full zone transfer som överför hela zonen.

**IXFR**= Är en incremental zone transfer som endast överför det som har
förändrats.