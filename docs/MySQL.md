---
title: MySQL
permalink: /MySQL/
---

MySQL är en relational database management system(RDBMS). MySQL var den
näst största RDBMS databasen och den den mest använda open-source RDBMS
databasen förr. MySQL är en av programmen du får när du installerar
[LAMP](/LAMP "wikilink").

Installation
------------

`apt-get install mysql-server`

Konfiguration
-------------

Konfiguration av MySQL görs i `/etc/mysql/my.cnf`.

By default så lyssnar MySQL enbart på 127.0.0.1, för att fixa det kan
man ändra i my.cnf till,

`bind-address = 0.0.0.0`

Då kommer MySQL lyssna på alla interface.

Skapa en databas
----------------

Logga in som root.

`mysql -u root -p`

Skapa en databas.

`create database `<namn>`;`

Skapa en användare.

`grant usage on *.* to `<dbuser>`@localhost identified by '`<password>`';`

Ge en användare alla rättigheter på en databas.

`grant all privileges on `<databas>`.* to `<dbuser>`@localhost;`

Backup/Dumpa databas
--------------------

Dumpa en databas till en fil för att göra en backup på den.

`mysqldump --user=[username] --password=[password] [databas] > dbcontent.sql`

Importera en databas
--------------------

För att importera en databas dump.

`mysql -u [username] -p[password] [databas] < dumpfilename.sql`

[Category:Guider](/Category:Guider "wikilink")
[Category:Sparco](/Category:Sparco "wikilink")