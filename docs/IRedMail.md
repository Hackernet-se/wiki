---
title: IRedMail
permalink: /IRedMail/
---

[Category:Guider](/Category:Guider "wikilink") Att sätta upp en
e-postserver är ett relativt stort projekt. Innan du börjar att
installera och konfigurera de nödvändiga paketen på mailservern bör du
lära dig vad allt betyder och förstå hur komponenterna samverkar för att
skicka och ta emot e-post. För detta finns många resurser på internet.
Det finns nackdelar med att köra sin egna mailserver. T.ex. om en
användare har glömt eller vill byta lösenord måste du fixa det. Får du
problem med spam blir din domän svartlistad. Du kan behöva unik
relay-konfiguration för att få det att lira ut från din ISP:s nät.

Denna artikel behandlar en av de smidigaste kompletta maillösningarna
idag, iRedMail.

### Alternativ

Vill man istället sätta upp alla komponenterna manuellt rekommenderar
jag att man följer följande guide istället:

[`https://www.linode.com/docs/email/postfix/email-with-postfix-dovecot-and-mysql`](https://www.linode.com/docs/email/postfix/email-with-postfix-dovecot-and-mysql)

Det är den absolut bästa postfix/dovecot/mysql-guide som finns.
Teoriavsnittet är också välskrivet. Att köra igenom denna guide är
väldigt lärorikt men ganska tidskrävande.

Installation
------------

Vill man ha samma komponenter och funktionalitet men en smidigare
installationsprocess är iRedMail ett utmärkt alternativ. Man får även
ett webgui för kontohantering
Rekommenderat OS: Ubuntu 14.04 / Debian 7

`sudo su -`
`mkdir /mailroot `
`wget `[`https://bitbucket.org/zhb/iredmail/downloads/iRedMail-0.9.2.tar.bz2`](https://bitbucket.org/zhb/iredmail/downloads/iRedMail-0.9.2.tar.bz2)
`tar xjf iRedMail-0.9.2.tar.bz2 && cd iRedMail-0.9.2`
`bash iRedMail.sh`

Kör igenom den självförklarande guiden

`rm /root/iRedMail-0.9.2/config`
`reboot`

Administration
--------------

Domän och kontohantering görs med webgui.

[`https://192.168.0.10/iredadmin`](https://192.168.0.10/iredadmin)

Vanlig webbmail ligger på:

[`https://192.168.0.10`](https://192.168.0.10)

SPF
---

DKIM
----

Rsync
-----

Rsync kan användas för att ta backup på /mailroot

Loggar
------

Kolla sammanställning av din loggfil.

`pflogsumm /var/log/mail.log`