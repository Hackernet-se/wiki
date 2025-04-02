---
title: InspIRCd
permalink: /InspIRCd/
---

[Category:Guider](/Category:Guider "wikilink") InspIRCd är en modulär
IRC server. Servern är skriven från scratch för att vara stabil, modern
och lättviktigt och stöd för många extra features som SSL stöd med
GNUTLS eller OpenSSL, LDAP stöd för användare med mera. Servern går att
köra på Linux, Windows, BSD och Mac OSX.

Installation
============

Börja med att installera paket för att kunna kompilera servern och kunna
ladda ner moduler.

`apt-get install g++ clang libwww-perl pkg-config`

Clona ner senaste stabila releasen från Github.

`git clone -b insp20 `[`git://github.com/inspircd/inspircd.git`](git://github.com/inspircd/inspircd.git)

För att kolla vilka extra features det finns kör:

`./configure --list-extras`

För att lägga till en feature tex SSL stöd med GNUTLS skriv:

`./configure --enable-extras=m_ssl_gnutls.cpp`

**OpenSSL vs. GnuTLS** Det har körts benchmarks mellan GnuTLS och
OpenSSL där GnuTLS har varit snabbare än OpenSSL. Därför rekommenderas
det att använda GnuTLS som SSL module.

Om du vill lägga till nån extra modul använd. Det går också att lägga
till moduler i efterhand med modulemanager.

`./modulemanager`

När du är klar kör följande kommando. Du kommer få en del frågor att
svara på. Du behöver inte vara root för att kompilera eller starta
servern.

`./configure`
`make`
`make install`

Konfiguration
=============

Kopiera exempel conf filerna från exempel mappen och gör dom ändringar
du känner för.

`cp modules.conf.example ../modules.conf`
`cp inspircd.conf.example ../inspircd.conf`
`cp opers.conf.example ../opers.conf`

GnuTLS
------

Om du vill att klienter ska kunna köra SSL behövs följande rader:

<bind address="" port="6667" type="clients" ssl="gnutls">
<gnutls cafile="conf/fullchain.pem" certfile="conf/cert.pem" keyfile="conf/privkey.pem" dhfile="conf/dh_4096.pem" dhbits="4096" hash="sha1">

Hashade lösenord
----------------

För att använda en sha256 hash i conf filerna istället för okrypterat
lösenord krävs följande module i **modules.conf** laddad:

<module name="m_sha256.so">

Använd denna [sida](http://www.xorbin.com/tools/sha256-hash-calculator)
för att generera en hash.

För att använda en hash till något krävs denna raden inom samma block:

`<... hash="sha256" password="SecretHash" ...>`

Lösenords skydda servern
------------------------

Om du vill lösenords skydda din IRC server så ange följande i connect
blocket:

`password="SecretPW"`

Skapa ett operator konto
------------------------

Ett operator konto kan vara bra att ha för att inte tappa kontrollen
eller ladda om configen på servern utan att behöva starta om.

I **oper.conf** anger du följande rad:

<oper name="username" hash="sha256" password="SecretHASH" host="*" type="netadmin">

För att bli operator skriver du följande i din IRC klient till servern:

`/oper Username password`

Tips n Tricks
=============

Medans InspIRCd har många moduler och features så saknar den vissa saker
som att kunna registrera sitt nickname, skydda sin kanal mot takeovers
och andra bra och ha IRC tjänster.

Därför kan man behöva använda sig av [Shaltúre](/Shaltúre "wikilink")
IRC services.