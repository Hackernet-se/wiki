---
title: Owncloud
permalink: /Owncloud/
---

[Category:Guider](/Category:Guider "wikilink")
[Category:Sparco](/Category:Sparco "wikilink") Owncloud är precis som
namnet antyder ett eget cloud. Funkar precis som Dropbox och liknande
tjänster bara att du själv måste hosta filerna på en egen server och på
så sätt ha full kontroll på dom.

För att komma åt dina filer i owncloud kan du använda ett webinterface
eller deras Owncloud client som finns till Windows, Linux, MacOSX, IOS,
Android.

##### Features

Nämner bara några features owncloud har som jag tycker är bra, fler
features listas [här](https://owncloud.org/features/).

-   Revisionshantering av filer.

<!-- -->

-   Undelete om du råkar ta bort fel fil.
-   Skapa en temporär URL till en fil som man kan dela med andra.
-   Kryptering av filer, AES 128 eller 256 bits.
-   LDAP/AD stöd.
-   Lägg till external storage(Dropbox, Google Drive, Amazon S3,
    SMB/CIFS, FTP, SFTP)
-   Synca kontakter och kalender från tex mobilen.
-   Plugins.

Installation
------------

För att installera Owncloud krävs en webbserver med PHP och
[MySQL](/MySQL "wikilink") förkonfat. Man kan använda sig av MariaDB,
SQLite och PostgreSQL också.

Gå till <https://owncloud.org/install/#instructions-server> för att få
tag på senaste tar.bz2 filen.

Tanka hem filen till roten av din webbfolder och packa upp den.

`wget `[`https://download.owncloud.org/community/owncloud-8.0.2.tar.bz2`](https://download.owncloud.org/community/owncloud-8.0.2.tar.bz2)` && tar xvf owncloud-8.0.2.tar.bz2`

Konfiguration
-------------

Surfa sedan in på <http://><IP>/owncloud

Följ anvisningarna som kommer.

### NFS

För att lagra data på en NFS share. Mounta sharen till en mapp i
owncloud foldern eller till en annan mapp på servern. Se till att samma
användare och grupp med samma GID som kör webbservern äger mappen på NFS
serverns sida. Peka sedan data folder mot den nya mappen under
installationen eller genom att ändra på parametern datadirectory i
<owncloud>`/config/config.php` filen. Glöm inte flytta över index.html
och .htaccess filen till NFS sharen så att inte obehöriga kan läsa dina
filer.

### Kryptering

För att sätta på kryptering.

Logga in som en admin.

Uppe till vänster välj Apps.

Leta upp appen `Server-Side encryption` och tryck enable.

Logga sedan ut och logga in igen. Har du redan sparat filer så kan
inloggningen ta en stund eftersom att den börjar kryptera dina filer
efter första inloggingen efter att du satt kryptering.