---
title: Rsync
permalink: /Rsync/
---

Rsync är ett verktyg som skapats för att tillhandahålla smidig och
inkrementell filöverföring. Det är en ersättning för scp och rcp och är
ett bra sätt att ladda upp filer till en fjärrserver. Rsync kan köras
över 2 olika protokoll.

**SSH mode**
Detta är default och är vad som används om man inte anger någon växel.
All data skickas krypterat med SSH.

**Daemon mode**
Med detta skickas datan med ett eget rsync-protokoll som går mot TCP
873. Ingen kryptering av kommunikationen men funkar bra inom LAN
alternativt över VPN-tunnlar. Vissa NAS-servrar stödjer endast denna
variant.

Installation
------------

`sudo apt-get install rsync`
`sudo yum install rsync`

Kommando
--------

`rsync [options] [source directory] [target directory]`

Exempel

`rsync -Pavz /local/directory/ root@10.0.0.11:/remote/directory/`

Jämför source och destination och kopiera över det som inte finns i
remote directory.
OBS a trailing slash on the source directory means that the source
directory's contents are copied, not the directory itself.

-   **-h**, human-readable: Number outputs are human readable
-   **-v**, verbose: Displays more output
-   **-z**, compress: Compress file data during transfer
-   **-P**, show progress
-   **-a**, archive mode: En sammanslagning av options och består av
    följande:
-   **-r**, operate recursively
-   **-l**, preserve links
-   **-p**, preserve permissions
-   **-t**, preserve times
-   **-g**, preserve groups
-   **-o**, preserve owner
-   **-D**, preserve device files and special files

Cron
----

Vill man ha automatisk synkning kan man schemalägga rsync-jobb enkelt
med cron. Använd SSH-nycklar för smidig autentisering.

Link Destination
----------------

[Category:Tools](/Category:Tools "wikilink")