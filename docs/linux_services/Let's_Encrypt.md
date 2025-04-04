---
title: Let's Encrypt
permalink: /Let's_Encrypt/
---

Let’s Encrypt är en certificate authority som är gratis, automatiserad
och öppen. Det är ett initiativ av Internet Security Research Group som
backas upp av en mängd stora företag där målet är att tillhandahålla TLS
helt gratis. Underliggande säkra protokoll som används är nyutvecklat
och går under namnet ACME (Automated Certificate Management Environment)
och används för att underlätta verifiering av domännamn. Detta har varit
krångligt tidigare då E-post och dylikt har används för
SSL/TLS-certifikat.

Förberedelse
------------

-   Öppna port 80 mot servern.(Let's encrypt startar en python
    webbserver som används för att verifiera att du äger domänen)

Installation
------------

**BETA**. Denna guiden baseras på beta dokumentation och kan komma att
ändras när Let's encrypt släpps för alla.

`git clone `[`https://github.com/letsencrypt/letsencrypt`](https://github.com/letsencrypt/letsencrypt)` && cd letsencrypt`

Konfiguration
-------------

`./letsencrypt-auto --agree-dev-preview --server `[`https://acme-v01.api.letsencrypt.org/directory`](https://acme-v01.api.letsencrypt.org/directory)` auth`

Du kommer sedan få en fråga vilken mail som ska användas och vilka
domäner du vill skapa ett cert för. För att kunna signa ett cert under
**beta** perioden måste du fått din domän whitelistad. Certen skapas
under `/etc/letsencrypt`. I **live** mappen finns symlink till senaste
versionen av ett certifikat.

|               |                                                                        |
|---------------|------------------------------------------------------------------------|
| privkey.pem   | Din privata nykel, måste hållas hemlig så ingen kan komma åt den.      |
| cert.pem      | Server certifikatet.                                                   |
| chain.pem     | Alla certificat som en webbläsare behöver **utom** server certificate. |
| fullchain.pem | Samma som **chain.pem** fast med server certificate också.             |

### Webroot

Webroot är ett plugin som tillåter din server att validera din domän
utan att stoppa webbserverm. Plugin lägger en liten dold fil i document
root på webbservern, den kan sedan läsas av Let's Encrypt CA för att
verifiera domänen.

`./letsencrypt-auto certonly -a webroot --agree-tos --renew-by-default --webroot-path=/var/www/html -d hackernet.se -d www.hackernet.se`

### Auto-renewal

Finns inte inbyggt än.

Tips n Tricks
-------------

### Cipherlist

[Chiperlist](https://syslink.pl/cipherlist/) är en hemsida som har olika
konfigurations exemplar för olika tjänster med säkerhet i fokus.

### Signa bakom reverse proxy

Om du använder dig av en reverse proxy och vill signa med hjälp av
webroot kan man i [apache](/apache "wikilink") göra att Let's encrypts
anrop inte skickas vidare. Utan istället går till en lokal mapp där din
Let's encrypt klient lagt den dolda filen.

`Alias /.well-known /var/www/.well-known`
`ProxyPass /.well-known !`

[Category:Guider](/Category:Guider "wikilink")