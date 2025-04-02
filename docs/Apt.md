---
title: Apt
permalink: /Apt/
---

Apt står för Advanced Package Tool och är ett user interface för
installera och ta bort program på Linux. Apt var från början ett
user-interface mot dpkg (Debian package) men har sedan dess modifierats
att fungera på RPM baserade system som Red hat tex. Apt följer med från
start på alla Debian-baserade distar.

### File locations

-   /etc/apt/sources.list: Locations to fetch packages from.
-   /etc/apt/apt.conf: APT configuration file.
-   /etc/apt/preferences: "pinning", i.e. a preference to get certain
    packages from a separate source or from a different version of a
    distribution.
-   /var/cache/apt/archives/: storage area for retrieved package files.

Kommandon
---------

Apt är en programsvit med flera olika program för att managera dina
program.

Lista installerade paket och deras versioner:

`apt list --installed`

apt-get
-------

Apt-get är programmet som tar hand om nerladdning och installation av
ett program.

#### update

Uppdatera din lista med paket.

`apt-get update`

#### install

Installera ett paket. Hämtar alltid senaste versionen som finns i din
lista.

`apt-get install `<paket>

Installera en specifik version av ett program. Mer info på [apt-cache
show](/Apt#show "wikilink") om hur du ser vilka versioner som finns.

`apt-get install `<paket>`=`<version>

#### upgrade

Kolla om det finns en ny version av ett program du har installerat och
uppgradera det.

`apt-get upgrade`
`apt-get -s upgrade #Dry run`

För att uppgradera hela din dist från tex Debian 7 till Debian 8 kör.

`apt-get dist-upgrade`

#### remove

Ta bort ett program. Config filer finns fortfarande kvar.

`apt-get remove `<paket>

Ta bort ett program och config filer.

`apt-get purge `<paket>

Oftast så är ett paket beroende av ett annat paket för att fungera och
då installeras det paketet också. Men sen om du väljer att ta bort
paketet du ville installera så finns fortfarande dom andra paketen kvar.
Om du vill ta bort paket som inte behövs så kör.

`apt-get autoremove`

apt-cache
---------

apt-cache är ett program för att söka och få fram information om ett
paket i din lista.

#### search

För att söka efter program.

`apt-cache search `<paket>

#### show

Få en kort beskrivning av ett program. Samt vilka olika versioner som
finns att hämta.

`apt-cache show `<paket>

För att endast se vilka versioner det finns av ett program.

`apt-cache show `<paket>` | grep Versions:`

#### showpkg

Ta på mer information om ett program. Tex vilka versioner finns att
hämta, vilka program den är beroende av och vilka program som är
beroende av den.

`apt-cache showpkg `<paket>

apt-mark
--------

Bestämmer ett program/pakets framtid.

#### hold

Markerar ett paket så det inte kan bli automatiskt installerat,
uppgraderat eller tas bort.

`apt-mark hold `<paket>

#### unhold

Tvärtemot hold.

`apt-mark unhold `<paket>

#### auto

Markerar att ett paket blivit installerat automatiskt. Paketet kommer då
att tas bort automatiskt när inget paket som installerats manuellt finns
kvar.

`apt-mark auto `<paket>

#### manual

Markerar ett paket som att det blivit installerat manuellt. Paketet
kommer inte tas bort automatiskt.

`apt-mark manual `<paket>

#### show

Tre kommandon där man ser på namnet vad som händer.

`apt-mark showauto`
`apt-mark showmanual`
`apt-mark showhold`

Apt Proxy
---------

För att spara bandbredd kan man sätta upp en egen cache av Ubuntus repo
och peka sina servrar mot den.
På cachen:

`sudo apt-get install apt-cacher-ng`

På övriga maskiner

`sudo nano /etc/apt/apt.conf`
`Acquire::http { Proxy "`[`http://10.0.0.500:3142`](http://10.0.0.500:3142)`"; };`

Ansible
-------

[Ansible](/Ansible "wikilink") update-playbook

``` yaml
---
- hosts: servers
  sudo: true
  tasks:
   - name: apt-get update
     apt: update_cache=yes
   - name: apt-get upgrade
     apt: upgrade=full
   - name: apt-get --dry-run autoremove
     command: apt-get --dry-run autoremove
     register: check_autoremove
     changed_when: False
   - name: apt-get autoremove
     command: apt-get -y autoremove
     when: "'packages will be REMOVED' in check_autoremove.stdout"
```

[Category:Tools](/Category:Tools "wikilink")