---
title: BitLocker
permalink: /BitLocker/
---

”Krypterar du dina data går de inte att läsa utan att knäcka
krypteringen. Det kräver betydligt mer av den som är ute efter dina
data, och har du en stark kryptering är det möjligen organisationer som
svenska FRA eller amerikanska NSA som kan knäcka den.” – Stiftelsen för
internetinfrastruktur

BitLocker Drive Encryption (BDE) är en Microsoft-produkt och erbjuder
datakryptering på volymnivå för Windowsklienter och servrar.

OBS Endast BitLocker för Windows Server 2008 R2/Windows 7 behandlas i
denna artikel.

Krypteringsnivåer
-----------------

BitLocker har stöd för två olika krypteringsnivåer, AES med 128-bitars
nyckel och AES med 256-bitars nyckel (AES är ett blockschiffer och för
ökad säkerhet används CBC). NSA klassar AES-128 som ”SECRET” och AES-256
som ”TOP SECRET”.

<https://www.nsa.gov/ia/programs/suiteb_cryptography/>

**Diffuser** En Diffuser-algoritm hjälper till att skydda mot
manipulation av skiffertexten. Dessa typer av attacker används för att
försöka hitta mönster eller svagheter i den krypterade datan. BitLocker
har stöd för Elephant-Diffuser-algoritmen och AES-128 med Diffuser är
default.

Begreppsförklaring: TPM
-----------------------

Trusted Platform Module är en öppen standard. En tpm-krets är en liten
processor på moderkortet med eget minne. Den kan bland annat generera
och lagra egna nycklar, skapa och verifiera signaturer med publika
nycklar. En nackdel med en separat kryptoprocessor som en tpm-krets är
att informationen till och från kretsen inte är skyddad. Den senaste
versionen (1.2) kom för första gången år 2006 (Version 2.0 är i
skrivande stund i draft-stadie). BitLocker stödjer endast version 1.2
och högre.

Upplåsningsmetod
================

Det finns tre metoder att välja på för att låsa upp krypteringen och
därmed kunna starta operativsystemet:

**TPM:** Använder funktionerna i TPM-hårdvara (1.2) för att ge en
transparent användarupplevelse. Nyckeln som används för diskkryptering
är krypterad i TPM-kretsen och kommer endast att släppas till
bootloadern om bootfilerna verkar vara omodifierade. Denna metod kan
knäckas med en så kallad ”cold boot”-attack.
<http://en.wikipedia.org/wiki/Cold_boot_attack>

**Användarautentisering:** Detta läge kräver att användaren matar in en
PIN-kod för att kunna starta operativsystemet. Denna metod måste
användas i kombination med någon annan upplåsningsmetod.

**USB-nyckel:** Användaren måste sätta i ett USB-minne innehållandes
kryptonyckeln i datorn för att kunna boota från den skyddade hårddisken.
Denna metod kan förbipasseras om en angripare får tillgång till
USB-minnet.

**Kombinationer** TPM only är default men dessa varianter kan kombineras
för att öka säkerheten, t.ex. TPM + PIN, TPM + USB, TPM + PIN + USB.

**Best Practice** Microsoft rekommenderar TPM + PIN.
<https://technet.microsoft.com/en-us/library/ee706531(v=ws.10>).aspx

Återställningsstrategi
======================

Ett krypteringsverktyg som BitLocker kräver en solid
återställningsstrategi, och BitLocker tvingar dig att definiera en metod
under installationen. Detta gör att du kan komma åt data på en krypterad
enhet när enheten inte kan låsas upp med någon metod i föregående
avsnitt. På en operativsystemenhet behöver du en återställningsmetod när
en användare glömmer PIN-koden, förlorar USB-minnet eller om TPM
registrerar integritetsändringar i systemfilerna. Hur vanligt det är att
TPM registrerar integritetsändringar vet jag inte men har aldrig hört
talas om det. BitLocker stödjer tre återställningsmetoder: lösenord,
nyckel och en dataräddningsagent (DRA).

Ett återställningslösenord är ett numeriskt lösenord på 48-bitar som
genereras under installationen av BitLocker. Man kan spara lösenordet
till en fil, som sedan lagras på ett säkert ställe eller konfigurera att
det sparas automatiskt i AD:t. Om man vill spara lösenordet i AD:t måste
man se till att datorerna kan ansluta till domänkontrollanten när man
aktiverar BitLocker. Lagring av BitLocker-lösenord i AD:t är baserad på
ett tillägg som skapar ett extra attribut till varje datorobjekt i AD:t,
däri lagras lösenordet. Domänkontrollanter på Server 2008 och Server
2008 R2 inkluderar detta tillägg som standard.

För lösenordshantering i AD:t tillhandahåller Microsoft en MMC-snapin
som tillför en BitLocker-flik på datorobjekt. Fliken visar alla lösenord
för datorobjektet. För Server 2008 R2 är BitLocker Active Directory
Recovery Password Viewer ett verktyg som ingår i Remote Server
Administration Toolkit (RSAT). Den andra metoden använder en 256-bitars
återställningsnyckel som man kan spara på ett USB-minne eller annan
plats. Precis som ett återställningslösenord, möjliggör en
återställningsnyckel att användare kan avkryptera den systemdisken utan
ingripande från administratörer, förutsatt att användaren har tillgång
till nyckeln. När man använder en återställningsnyckel måste man sätta i
ett USB-minne eller peka ut en annan plats där nyckeln finns. Den tredje
metoden är med hjälp av en dataåterställningsagent (DRA) och kräver
ingripande av IT-avdelningen. Denna metod utnyttjar ett särskilt intyg
som utfärdas till en dedikerad DRA-administratör i organisationen.
DRA-certifikatets signatur distribueras till alla BitLocker-krypterade
enheter med GPO-inställningar. Detta för att säkerställa att endast
administratören med ett matchande DRA-certifikat och privat nyckel kan
avkryptera disken. Man använder GPO-inställningar för att konfigurera
vilka metoder som krävs, är otillåtna, eller kan göras frivilligt.

Group Policy
============

Följande inställningar bedömer författaren vara relevanta att titta på
för en implementation.

Generella BitLocker-inställningar

`Choose drive encryption method and cipher strength`
`Provide the unique identifiers for your organization`

TPM-inställningar

`Turn on TPM backup to Active Directory Domain Services`

Specifika inställningar för systemdiskkryptering.

`Choose how BitLocker-protected operating system drives can be recovered`
`Configure TPM platform validation profile`
`Require additional authentication at startup`

Författarens rekommendationer: Ställ in GPO så att det automatiskt tas
backup på kryptonycklarna till AD:t, samt kryptera inte datorer som inte
har nyckeln sparad i AD:t.

Utrullningsmetod
================

I större IT-miljöer kan man automatisera utrullning och konfiguration
med ett script som Microsoft tillhandahåller. Scriptet heter
EnableBitLocker.vbs och finns på:
<https://gallery.technet.microsoft.com/scriptcenter/780d167f-2d57-4eb7-bd18-84c5293d93e3>
Man kan använda scriptet som det är, eller skräddarsy det för att bättre
möta organisationens behov. För att köra scriptet kan man använda ett
startscript som appliceras med hjälp av GPO-inställningar eller ett
distributionsverktyg som till exempel System Center Configuration
Manager (SCCM).

Före systemdiskkrypteringen kan man behöva kontrollera partitionerna på
målsystemen. På en systemdisk kräver BitLocker en separat och aktiv
systempartition. Detta är en okrypterad partition som innehåller de
filer som behövs för att starta operativsystemet. I Windows 7, skapas en
sådan systempartition automatiskt som en del utav installationen av
Windows. På system som har uppgraderat från en tidigare Windows-version
eller på system som kommer förkonfigurerade med en enda partition,
kommer inställningsguiden automatiskt att konfigurera om målenheten för
BitLocker genom att skapa en separat och aktiv systempartition. Att
använda manuell handläggning på varje dator blir snabbt opraktiskt när
man ska förbereda hundratals eller tusentals system med en partition för
BitLocker. Vi vill använda Microsofts WMI- script för att aktivera
BitLocker.

**Prestandapåverkan**

Verkar inte finnas någon nämnvärd prestandapåverkan:
<http://lanoe.dyndns.org/index.php/howto1/bitlocker/2395-performance-hit-of-full-disk-encryption>

**Övriga tankar**

Har användarna möjlighet att stänga av systemdiskkrypteringen utan
administratörernas kännedom?

En diskkryptering kan ta flera timmar, kan datorn stängas av och sättas
på under tiden utan att det förstör något?

[Category:Windows](/Category:Windows "wikilink")