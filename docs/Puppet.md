---
title: Puppet
permalink: /Puppet/
---

[Category:Guider](/Category:Guider "wikilink")
[Category:Sparco](/Category:Sparco "wikilink") Puppet är ett
automatiseringsverktyg för servrar. Puppet är ett väldigt kraftfullt
verktyg, du kan få en fil att se likadan ut på 1000 olika servrar på
bara 2 minuter eller att se till att SSH confen är den samma. Puppet kan
köras i både Unix och Windows miljör. Många stora företag använder
Puppet tex, Google, Twitter, Spotify, Dell. Puppet är mycket användbart
om man har servrar med olika operativsystem. Skillnaderna mellan olika
operativsystem spelar ingen roll, man kan sätta upp en huvudserver och
lagra konfigurationer för alla servrar. Huvudservern kallas master och
klienterna kör agenter. Klienterna ansluter regelbundet till mastern för
att synkronisera sina konfigurationer och rapportera alla lokala
ändringar tillbaka till mastern. Master måste vara av samma version
eller nyare än de agenter som ansluter till den. Puppet finns i
Enterprise eller som open source.

Förberedelse
============

Lägg in Puppets egna repos för att få tag på fler och senare versioner
av Puppet.

Tanka hem och kör rätt deb paket från
[`https://apt.puppetlabs.com/`](https://apt.puppetlabs.com/)

Installation
============

Det är viktigt att man kör samma version på puppet master och puppet
agent för att inte få några kompatibilitets problem.

### Server

#### Debian/Ubuntu

`sudo apt-get update && sudo apt-get -y upgrade && sudo apt-get -y install puppetmaster rdoc ntp`
`sudo touch /etc/puppet/manifests/site.pp`

#### CentOS/RedHat

`sudo yum update && sudo yum install puppet-server ntp`
`sudo touch /etc/puppet/manifests/site.pp `

### Klient

`sudo apt-get update && sudo apt-get upgrade && sudo apt-get -y install puppet ntp`
`sudo yum update && sudo yum install puppet ntp`

Namnuppslag
===========

Default för att hitta till mastern gör klienterna ett namnuppslag på
*puppet*. Sätt upp i din DNS så att puppet pekar mot mastern. T.ex.
puppet.exempel.se. Sedan på klienten:

`echo "search exempel.se" | sudo tee -a /etc/resolv.conf`

Om klienten använder DHCP kan det hända att resolv.conf skrivs över.
Testa

`ping puppet`

Det måste också vara öppet för klienterna mot mastern på TCP 8140

Konfiguration
=============

| Pre-2.6       | Post-2.6          |
|---------------|-------------------|
| puppetmasterd | puppet master     |
| puppetd       | puppet agent      |
| puppet        | puppet apply      |
| puppetca      | puppet cert       |
| ralsh         | puppet resource   |
| puppetrun     | puppet kick       |
| puppetqd      | puppet queue      |
| filebucket    | puppet filebucket |
| puppetdoc     | puppet doc        |
| pi            | puppet describe   |

Master
------

Konfigurations av puppet görs under `/etc/puppet/`

Börja med att skapa ett CA cert för din master server. Under `[main]` i
`puppet.conf` lägg till,

`dns_alt_names = puppet,puppet.domän.se`

Skapa sedan CA certet med kommandot,

`sudo puppet master --verbose --no-daemonize`

När det står `Notice: Starting Puppet master version `<VERSION> har
certet skapats. Tryck ctrl-c för att stoppa.

### Hiera

Är ett enklare sätt att konfigurera dina klienter på. Hiera följer med
puppet och inget som ska behöva installeras. När man konfar sina noder
med hiera använder man sig av yaml kod.

Skapa filen `site.pp` i mappen `manifests` och skriv,

`hiera_include('classes')`

Skapa sedan filen `hiera.yaml` i rooten av puppet och fyll den med,

``` yaml
 ---
  :backends:
    - yaml
  :yaml:
    :datadir: /etc/puppet/hieradata
  :hierarchy:
    - "node/%{::fqdn}"
    - "os/%{::osfamily}"
    - common
  :logger:
    - puppet
```

Skapa sedan en mapp som heter `hieradata` i rooten av puppet. I den
mappen ska du skapa mapparna `node` och `os`. I mappen `os` kan du skapa
en fil som heter tex `Ubuntu.yaml`. Då kommer alla ubuntu maskiner få
den confen som står där i. I mappen `hieradata` skapa en fil som heter
`common.yaml`. Confen som står i denna filen kommer alla noder att få.
Exempel conf på `common.yaml` som kommer använda modulen utils och
installera paketet vim och autofs.

``` yaml
 ---
 classes:
   -utils

 utils::packages:
   - vim
   - autofs
```

Klient
------

Puppet agenten funkar direkt utan inställningar om man inte har ett
annat FQDN på puppet master(se under). En sak man ska välja är om man
vill köra puppet agent som ett cronjob eller som en service som hämtar
ny conf automatiskt.

Har man ett annat FQDN på sin puppet master än puppet.domän.se bör man
lägga till under `[main]` i `/etc/puppet/puppet.conf`

`server = FQDN`

### Cron job

För att köra puppet agent som ett cron job skriv följande.

`sudo puppet resource cron puppet-agent ensure=present user=root minute=30 command='/opt/puppet/bin/puppet agent --onetime --no-daemonize --splay --splaylimit 60'`

### Service

I filen `/etc/default/puppet` ändra till `START=yes`. För att starta
puppet agenten och att den autostartar vid omstart.

`sudo puppet resource service puppet ensure=running enable=true`

Vill man ändra intervalen på hur ofta agenten frågar mastern efter ny
conf. Default är 30 minuter, lägg till följande under `[agent]` i
`puppet.conf`.

`runinterval = 2h`

Certifikat
----------

All kommunikation görs med SSL och certifikat används för
autentisering.
På klient:

`sudo puppet agent --waitforcert 120 --test`

På master:

`sudo puppet cert list`
`sudo puppet cert sign `<hostname>

För att autosigna certifikat så lägg till detta under `[master]` i
`puppet.conf` på din puppet master.

`autosign = true`

Lista alla cert på puppet master:

`puppet cert list -a`

Ta bort klient cert på puppet master:

`puppet cert clean `<hostname>

Moduler
=======

För att söka efter moduler till puppet använd
[forge](https://forge.puppetlabs.com/).

Moduler installerar man på sin master och sedan använder tex hiera för
att konfigurera sina klienter.

För att installera och ta bort moduler använd kommandot,

`puppet module install `<modulnamn>
`puppet module uninstall `<modulnamn>

Det är viktigt att läsa readme filen om varje modul för att förstå hur
den fungerar. Den finns under `/etc/puppet/modules/"modulnamn"/`

Varje gång du ska använda en modul måste du kalla efter den tex under
`classes:` i hiera.

Autofs
------

Modul som styr upp autofs mounts på din server.

`puppet module install EagleDelta2-autofs`

Exempel conf för hiera.

``` yaml
 ---
 classes:
  - autofs

 mapOptions:
   backup:
     mount: '/opt'
     mapfile: '/etc/auto.backup'
     mapcontents:
       - 'backup -fstype=nfs,auto,rw,async,hard,intr 192.168.1.200:/mnt/zfs/Backup'
     options: '--timeout=60'
     order: 01
   home:
     mount: '/home'
     mapfile: '/etc/auto.home'
     mapcontents:
       - '* -fstype=nfs,user,auto,rw,async,hard,intr 192.168.1.200:/mnt/zfs/Home/&'
     options: '--timeout=120'
     order: 02
```

Finns mer info att läsa om modulen på
[forge](https://forge.puppetlabs.com/EagleDelta2/autofs).

Utils
-----

Utils är en modul som installerar paket på en node. Den har stöd för
följande operativsystem. RedHat, Windows, Ubuntu, Debian, Solaris, SLES,
Scientific, CentOS, OracleLinux, AIX, SLED

`puppet module install ghoneycutt-utils`

Exempel conf för hiera.

``` yaml
 ---
 classes:
  - utils

 utils::packages:
  - vim
  - fail2ban
  - apache2
```

Mer om modulen finns på
[forge](https://forge.puppetlabs.com/ghoneycutt/utils).

Rsyslog
-------

`puppet module install saz-rsyslog`

Exempel conf för hiera.

``` yaml
 ---
 classes:
  - rsyslog::client

 rsyslog::client::server: '192.168.1.205'
```

Mer om modulen finns på
[forge](https://forge.puppetlabs.com/saz/rsyslog).