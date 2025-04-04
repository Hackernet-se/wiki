---
title: Digitala Certifikat
permalink: /Digitala_Certifikat/
---

Ett digitalt certifikat är en datafil som består av kryptonycklar.
Certifikatet kan användas för kryptering, digitala signaturer och
autentisering (OBS ej SSH autentisering). Certifikat utfärdas av en
certifikatauktoritet, CA. Den senaste standarden är X.509 version 3
X509-certifikat används av alla sorts system och hur du hanterar dina
certifikat är plattformsoberoende. Här är kort läsning om
certifikatshantering på Windows och Red Hat:
<http://techworld.idg.se/2.2524/1.498006/windows-vs-linux---nu-avgors-kampen/sida/5/terminalfunktioner-och-certifikattjanster>

Om man inte litar på Microsoft CryptoAPI kan man använda t.ex. OpenSSL
för att generera nycklarna och sedan Windowsverktyg för att hantera och
signera certifikaten. Med OpenSSL kan du generera i princip hur stora
RSA-nycklar som helst förutsatt att du har en superdator alternativt
evigt liv. Hur stora nycklar som går att använda varierar från
applikation till applikation, t.ex. OpenVPN klarar inte större än
4096-bitar annars blir meddelandena "för långa".

Format
------

**DER** is a binary encoding of a certificate. Typically these use the
file extension of .crt or .cer.

**PEM** is a Base64 encoding of a certificate represented in ASCII
therefore it is readable as a block of text. This is very useful as you
can open it in a text editor work with the data more easily.

Let's Encrypt
-------------

Let’s Encrypt är en certificate authority som är gratis, automatiserad
och öppen. Det är ett initiativ av Internet Security Research Group som
backas upp av en mängd stora företag där målet är att tillhandahålla TLS
helt gratis.
Läs mer på [Let's Encrypt](/Let%27s_Encrypt "wikilink") hur du kan skapa
dina egna godkända certifikat.

Self-signed
-----------

Man kan skapa certifikat och signera dem själv med OpenSSL.

`openssl req -newkey rsa:4096 -nodes -keyout selfsigned.key -x509 -days 3650 -out selfsigned.crt`

XCA
---

XCA är ett smidigt och kompetent verktyg för certifikatshantering som
kör OpenSSL för den kryptografiska biten. Det jobbar mot en databasfil
som är viktig att hålla reda om du inte har backup på dina
kryptonycklar. Databasfilen måste också lösenordsskyddas.
<http://sourceforge.net/projects/xca/>

### Egen CA

Tänk igenom noggrant hur du vill ha det för när rootcertet är skapat och
du börjar rulla ut signerade certifikat till servrar och klienter går
det inte att ändra något i efterhand!

Starta xca.exe, skapa en ny databas med File -\> New DataBase. Lägg
databasen på lämpligt ställe och välj ett säkert lösenord. För att kunna
skapa ett certifikat måste man ha kryptonycklar. Dessa kan man importera
till databasen eller generera nya med det inbyggda verktyget, Private
Keys -\> New Key.

Börja med att skapa ett certifikat som ska vara rootcert för din CA.
Detta används för att signera dina certifikat och ska distribueras till
alla klienter som ska kunna verifiera dina certifikat.

Välj Certificates -\> New Certificate. Här ska all information om
rootcertet fyllas i.

#### Source

Ditt rootcert måste vara self signed men kan ha valfritt serienummer.
Signature algorithm: Valfritt (md5 ej rekommenderat)
Det följer med en CA-template som är en bra utgångspunkt, Apply all.

#### Subject

`Internal name: Används endast lokalt i din databas, sätt något informativt.`

Här kan du välja vad du vill. Nedan är exempel från GeoTrusts rootcert
som bland annat har signerat Googles hemsidecertifikat.

`countryName: US`
`stateOrProvinceName:`
`localityName:`
`organizationName: GeoTrust Inc.`
`organizationalUnitName`
`commonName: GeoTrust Global CA`
`emailAddress:`

Private key: Välj en befintlig nyckel eller generera en ny

#### Extensions

Det som följer med templaten fungerar bra. T.ex. 10 års validitet.

Det som är viktigt på denna sida är X509v3 Distribution Points och
Authority Information Access. Här behövs ett designval göras. Man kan
lämna dessa tomma och det fungerar ändå. Den klara nackdelen med det
blir att man aldrig någonsin kan göra ett signerat certifikat ogiltigt.
Dvs berätta för klienterna att ett certifikat inte ska litas på. Detta
kan göras på olika sätt med respektive för och nackdelar.

**CRL vs OCSP** (Arbete pågår, lämnar denna länk sålänge:
<https://www.fir3net.com/Security/Concepts-and-Terminology/certificate-revocation.html>)

#### Key usage

Certificate- och CRL sign fungerar bra. Detta är endast informationsfält
så man vet vad certifikatet är tänkt att användas till.

#### Netscape

Allt här kan tas bort. Finns endast med för bakåtkompabilitet med gamla
gamla standarder.

#### Advanced

Översikt över ditt certifikat. Kolla igenom så allt är korrekt.

OK = klart

#### Distribution

Nu kan ditt rootcert börja skickas ut. Du kan exempelvis lägga det på en
publik webbserver så kan vem som helst enkelt ladda ner det.

ECC
---

Elliptic Curve Cryptography erbjuder mindre nycklar med liknande
säkerhet som traditionell kryptering med öppen nyckel, vilket leder till
högre krypteringsprestanda. OpenSSL har stöd för Elliptic Curve
Cryptography-certifikat men tyvärr har inte XCA det.
Working directory

`sudo mkdir /etc/nginx/ssl`

Skapa privat nyckel

`sudo openssl ecparam -out /etc/nginx/ssl/nginx.key -name prime256v1 -genkey`

Skapa CSR

`sudo openssl req -new -key /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/csr.pem`

Nu kan du signera csr:n med ditt rootcert alternativt själv-signera med
följande:

`sudo openssl req -x509 -nodes -days 365 -key /etc/nginx/ssl/nginx.key -in /etc/nginx/ssl/csr.pem -out /etc/nginx/ssl/nginx.pem `

[Category:Guider](/Category:Guider "wikilink")