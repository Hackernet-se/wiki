---
title: MediaWiki
permalink: /MediaWiki/
---

[Category:Guider](/Category:Guider "wikilink")
[Category:Sparco](/Category:Sparco "wikilink") MediaWiki är en
open-source wiki application som driver två av dom största och bästa
wiki hemsidorna på nätet [Hackernet](http://hackernet.se) och
[Wikipedia](https://www.wikipedia.org/).

Förberedelser
-------------

För att kunna köra mediawiki krävs det att du har
[LAMP](/LAMP "wikilink").

### Valfria program

Man kan installera dom i efterhand också om man kommer på att man
behöver dom.

|             |                                                                                                                   |
|-------------|-------------------------------------------------------------------------------------------------------------------|
| php-apc     | Alternative PHP Cache.                                                                                            |
| php5-intl   | Unicode normalization.                                                                                            |
| ImageMagick | Image thumbnailing.                                                                                               |
| GD Library  | Alternative to ImageMagick. Install libgd2-xpm libgd2-xpm-dev php5-gd.                                            |
| phpmyadmin  | MySQL administration tool.                                                                                        |
| php5-cli    | Ability to run PHP commands from the command line, which is useful for debugging and running maintenance scripts. |

Exempel:

` sudo apt-get install php-apc php5-intl imagemagick phpmyadmin vsftpd php5-cli`

Installation
------------

Tanka hem senaste eller LTS versionen från deras hemsida, packa upp
filen och byt namn på foldern.

`wget `[`https://releases.wikimedia.org/mediawiki/1.25/mediawiki-1.25.1.tar.gz`](https://releases.wikimedia.org/mediawiki/1.25/mediawiki-1.25.1.tar.gz)` | tar -xvf mediawiki-1.25.1.tar.gz -C /var/www/ | mv /var/www/mediawiki-1.25.1/ /var/www/mediawiki`

Se till att användaren som kör din webbserver äger mappen `mediawiki` så
att du kan tex ladda upp filer.

Skapa sedan en databas som mediawiki kan ansluta till, surfa sedan in på
http://\<ip\>/mediawiki och följ wizarden.

När wizarden är klar ladda upp `LocalSettings.php` till `mediawiki`
mappen.

Konfiguration
-------------

All konfiguration av mediawiki och plugins görs i `LocalSettings.php`
filen.

### Plugins

[Plugins](https://www.mediawiki.org/wiki/Category:Extensions) finns på
mediawikis hemsida.

Några bra plugins som denna sidan använder är.

|                                                                                           |                                                                                                                                                   |
|-------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| [Visual Editor](https://www.mediawiki.org/wiki/Extension:VisualEditor)                    | Bra editor om man är nybörjare och inte förstår mediawikis syntax.                                                                                |
| [Google Analytics](https://www.mediawiki.org/wiki/Extension:Google_Analytics_Integration) | Enkelt att få Google analytics att fungera.                                                                                                       |
| [LDAP Authentication](https://www.mediawiki.org/wiki/Extension:LDAP_Authentication)       | För att kunna koppla sin wiki mot en LDAP server som OpenLDAP eller Active Directory.                                                             |
| [Wiki Editor](https://www.mediawiki.org/wiki/Extension:WikiEditor)                        | För att få en lite bättre source editor.                                                                                                          |
| [SyntaxHighlight](https://www.mediawiki.org/wiki/Extension:SyntaxHighlight_GeSHi)         | För att kunna få tex php,html,python kod på en sida mer lättläst.                                                                                 |
| [MsUpload](https://www.mediawiki.org/wiki/Extension:MsUpload)                             | Enkelt kunna ladda upp filer när man editerar.                                                                                                    |
| [Dynamic Page List](https://www.mediawiki.org/wiki/Extension:Intersection)                | För att kunna skapa dynamiska listor från tex kategorier eller namespaces. Tools på [Linux sidan](/Linux#Tools "wikilink") använder detta plugin. |
| [Contribution Scores](https://www.mediawiki.org/wiki/Extension:Contribution_Scores)       | För att få fram en tabel om vem som bidragit med mest på wikin.                                                                                   |

Backup
------

Vi använder ett script som gör en dump på databasen och packar ihop
dumpen med alla filer i mediawiki mappen. Backup filen sparas i samma
mapp som scriptet körs i.

<div class="panel-group" id="accordion">

<accordion parent="accordion" heading="Ändra under configuration så det passar dig.">

``` bash
#!/bin/bash
#
# fullsitebackup.sh V1.2
#
# Full backup of website files and database content.
#
# A number of variables defining file location and database connection
# information must be set before this script will run.
# Files are tar'ed from the root directory of the website. All files are
# saved. The MySQL database tables are dumped without a database name and
# and with the option to drop and recreate the tables.
#
# ----------------------
# 05-Jul-2007 - Quick adaptation for MediaWiki (currently testing)
# ----------------------
# March 2007 Updates - Version for Drupal
# - Updated script to resolve minor path bug
# - Added mysql password variable (caution - this script file is now a security risk - protect it)
# - Generates temp log file
# - Updated backup and restore scripts have been tested on Ubunutu Edgy server w/Drupal 5.1
#
# - Enjoy! BristolGuy
#-----------------------
#
## Parameters:
# tar_file_name (optional)
#
#
# Configuration
#

# Database connection information
dbname="wiki" # (e.g.: dbname=wikidb)
dbhost="localhost"
dbuser="wikidb" # (e.g.: dbuser=wikiuser)
dbpw="secretpassword" # (e.g.: dbuser password)

# Website Files
webrootdir="/var/www/wiki" # (e.g.: webrootdir=/home/user/public_html)

#
# Variables
#

# Default TAR Output File Base Name
tarnamebase=wiki_sitebackup-
datestamp=`date +'%m-%d-%Y'`

# Execution directory (script start point)
startdir=`pwd`
logfile=$startdir"/fullsite.log" # file path and name of log file to use

# Temporary Directory
tempdir=$datestamp

#
# Input Parameter Check
#

if test "$1" = ""
then
tarname=$tarnamebase$datestamp.tgz
else
tarname=$1
fi

#
# Begin logging
#
echo "Beginning mediawiki site backup using fullsitebackup.sh ..." > $logfile
#
# Create temporary working directory
#
echo " Creating temp working dir ..." >> $logfile
mkdir $tempdir

#
# TAR website files
#
echo " TARing website files into $webrootdir ..." >> $logfile
cd $webrootdir
tar cf $startdir/$tempdir/filecontent.tar .

#
# sqldump database information
#
echo " Dumping mediawiki database, using ..." >> $logfile
echo " user:$dbuser; database:$dbname host:$dbhost " >> $logfile
cd $startdir/$tempdir
mysqldump --user=$dbuser --password=$dbpw --add-drop-table $dbname > dbcontent.sql

#
# Create final backup file
#
echo " Creating final compressed (tgz) TAR file: $tarname ..." >> $logfile
tar czf $startdir/$tarname filecontent.tar dbcontent.sql

#
# Cleanup
#
echo " Removing temp dir $tempdir ..." >> $logfile
cd $startdir
rm -r $tempdir

#
# Exit banner
#
endtime=`date`
echo "Backup completed $endtime, TAR file at $tarname. " >> $logfile
```

</accordion>

### Cronjob

Scriptet funkar att köra som ett cronjob. Raden gör att det körs en
backup kl 05:00 varje dag.

`0 05 * * * cd /path/to/script && sh Backup_script.sh`

Sitemap
-------

Mediawiki har ett inbyggt script för att skapa sitemaps. Sitemaps
används av sökmotorer så att deras botar vet vilka URLs det finns att
indexera.

Scriptet finns under `maintenance` och heter `generateSitemap.php`.

Skapa en mapp att spara sitemapen i.

`mkdir /var/www/mediawiki/sitemap`

Kör kommandot,

`php generateSitemap.php --fspath /var/www/mediawiki/sitemap --server "`[`http://URLtillStartsidan`](http://URLtillStartsidan)`" --urlpath "`[`http://URLtill/sitemap`](http://URLtill/sitemap)`"`

Nu ska du säga till sökmotorn vart din sitemap finns så är det klart.

### Cronjob

Kör generateSitemap.php som ett cronjob var 45e minut.

`*/45 * * * * /usr/bin/php /var/www/wiki/maintenance/generateSitemap.php --fspath /var/www/mediawiki/sitemap --server "`[`http://URLtillStartsidan`](http://URLtillStartsidan)`" --urlpath "`[`http://URLtill/sitemap`](http://URLtill/sitemap)`"`

Upgrade
-------

Mediawiki använder semantic versioning där man namnger releases X.Y.Z
(Major.Minor.Patch). I skrivande stund så är Mediawiki uppe i major 1,
minor 26, patch 0.

Alla versioner av Mediawiki finns att ladda hem
[här!](https://releases.wikimedia.org/mediawiki/)

### Minor

Oftast är **LocalSettings.php** kompatibel mellan minor versioner, läs
release notes för att få reda på mer.

Ersätt dom gammla filerna med dom nya filerna. Via skalet kör sedan
maintenance script för att uppdatera databas tabeller och bygg om
filstrukturen för bla filer:

`php /var/www/mediawiki/maintenance/update.php`
`php /var/www/mediawiki/maintenance/rebuildall.php`

Gå in på din wiki sida och kolla *Special:Version* för att verifiera att
uppgraderingen.

### Patch

1.  Gå till din mediawiki mapp (den med localsettings.php i).
2.  Ladda ner och packa om patch filen.
3.  Kör **patch -p1 --dry-run -i *mediawiki stable release
    number.patch***
4.  Gick allt igenom utan problem kör samma kommando igen fast utan
    **--dry-run**.
5.  Surfa sedan in på din wiki sida och kolla *Special:Version* för att
    verifiera att patchen gått igenom.