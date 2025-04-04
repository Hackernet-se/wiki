---
title: Certbot
permalink: /Certbot/
---

[Category:Guider](/Category:Guider "wikilink") Certbot används för att
enkelt kunna automatisera nya cert ifrån [Let's
Encrypt](/Let%27s_Encrypt "wikilink").

Installation
============

-   <btn data-toggle="tab" class="">\#tab1\|CentOS 7</btn>
-   <btn data-toggle="tab" class="">\#tab2\|Ubuntu 18.04</btn>

<div class="tab-content">
<div id="tab1" class="tab-pane fade in active">

Börja med att installera EPEL repot.

`yum -y install epel-release yum-utils`

Installera sedan Certbot

`yum install certbot python2-certbot-nginx`

</div>
<div id="tab2" class="tab-pane fade">

Börja med lägga till nya repon.

`apt-get update`
`apt-get install software-properties-common`
`add-apt-repository universe`
`add-apt-repository ppa:certbot/certbot`
`apt-get update`

Installera sedan certbot.

`apt-get install certbot python-certbot-nginx`
`  `

</div>
</div>

Konfiguration
-------------

Certbot körs första gången som en oneliner. Efter det skapas en config
fil under **/etc/certbot/renewal/** med alla inställningar du valde.

Certifikat sparas under **/etc/letsencrypt/live/<domän>**

Signera certifikat
------------------

### Renew

Om du en gång skapat ett certifikat och vill signa om det för att det är
på väg att gå ut kan du köra:

`certbot renew`

Om du vill göra en dry run gör du det med:

`certbot renew --dry-run`

Certifikat kommer inte renewas om det är mer än 30 dagar kvar tills dom
går ut by default .

### Webroot

Webroot signering fungerar genom att certbot lägger en fil i en viss
mapp som sedan Let's Encrypts ACME server kommer försöka hämta för att
validera att domänen du vill signa för pekar mot dig och att det är du.

Följande kommando kommer att signera ett cert för hackernet.se och
www.hackernet.se.

`certbot certonly --webroot --agree-tos --no-eff-email --email dinmail@hackernet.nu -w /path/to/webfolder -d hackernet.se, www.hackernet.se`

### DNS-01

Man kan använda sig av DNS record för att verifera sitt cert. Med DNS
challenge kan man också signa wildcard certifikat.

Börja med att skapa filen **/etc/letsencrypt/dns-01.ini** med följande
innehåll:

`# Target DNS server`
`dns_rfc2136_server = `<din dns server>
`# Target DNS port`
`dns_rfc2136_port = 53`
`# TSIG key name`
`dns_rfc2136_name = `<namnet på din ddns nykel>`.`
`# TSIG key secret`
`dns_rfc2136_secret = `<din hashade nykel>
`# TSIG key algorithm`
`dns_rfc2136_algorithm = HMAC-SHA512`

Kör sedan följande kommando:

`certbot certonly --agree-tos --no-eff-email --email dinmail@hackernet.nu --dns-rfc2136 --dns-rfc2136-credentials /etc/letsencrypt/dns-01.ini -d *.subdomain1.hackernet.se,*.subdomain2.hackernet.se,*.subdomain3.hackernet.se`

Automatisera certifikat
-----------------------

### Renew

Med hjälp av systemd timers kan man köra **certbot renew** med mellanrum
för att se till att alla ens certifikat är giltiga.

Börja med att skapa följande service fil:

<table>
<thead>
<tr class="header">
<th><p>/etc/systemd/system/certbot-renewal.service</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>[Unit] Description=Certbot Renewal</p>
<p>[Service]<br />
ExecStart=/usr/bin/certbot renew</p></td>
</tr>
</tbody>
</table>

Skapa sedan timer filen som kommer trigga servicen.

<table>
<thead>
<tr class="header">
<th><p>/etc/systemd/system/certbot-renewal.timer</p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>[Unit] Description=Timer for Certbot Renewal</p>
<p>[Timer]<br />
OnBootSec=300<br />
OnUnitActiveSec=1w</p>
<p>[Install]<br />
WantedBy=multi-user.target</p></td>
</tr>
</tbody>
</table>

Tjänsten kommer köras en gång i veckan och 300 sekunder efter boot.
Eftersom certbot by default inte signerar nya cert om dom det är mer än
30 dagar kvar så räcker det med 1 gång i veckan.

Starta sedan timern:

`systemctl start certbot-renewal.timer`

Enable timern så att den startas vid boot:

`systemctl enable certbot-renewal.timer`

För att visa alla aktiva timers körs:

`systemctl list-timers`

### Hooks

Certbot kan kalla på olika script före, under och efter en körning.

| Path                                  | Help                                              |
|---------------------------------------|---------------------------------------------------|
| /etc/letsencrypt/renewal-hooks/deploy | Körs enbart efter ett lyckat renewal av ett cert. |
| /etc/letsencrypt/renewal-hooks/pre    | Körs alltid före en renew.                        |
| /etc/letsencrypt/renewal-hooks/post   | Körs alltid efter en renew.                       |

Ett exempel på en fil under deploy för att starta om nginx:

``` bash
#!/bin/bash
systemctl reload nginx.service
```