---
title: Flexget
permalink: /Flexget/
---

Flexget är ett avancerat automatiserings program för att tanka hem
torrents, serier, filmer mm. Det kan ta RSS-feeds, html sidor, csv-filer
eller sökmotorer som källa för att ladda hem. Det finns även plugins för
vissa sidor som inte har någon bra feed att följa.

Installation
------------

För att installera Flexget verifera att du har Python*' 2.6.x - 2.7.x.*'

`python -v`

Sedan behöver du pip.

`apt-get update && apt-get install python-pip`

Installera sedan Flexget med kommandot.

`pip install flexget`

Verifera att Flexget är installerat med

`flexget -V`

Konfiguration
-------------

Flexget använder sig av en configurations fil som man skriver i YAML.

Se [Flexgets Cookbook](http://flexget.com/wiki/Cookbook) för flera olika
exempel på hur man kan skriva.

Tips n Trix
-----------

Har du conf filen i din hemmapp måste du använda växeln `-c` tex,
`flexget -c /home/user/flexget.yml`

För att validera din conf fil att den fungerar använd kommandot.

`flexget -c flexget.yml check`

För att köra flexget använd kommandot

`flexget -c flexget.yml execute`

### Crontab

Flexget kan både köras som en deamon och använda ett inbyggt schema för
när den ska kolla efter saker eller så kan man använda crontab.

För att köra Flexget var 30e minut.

`*/30 * * * * /usr/local/bin/flexget -c /root/flexget.yml execute`

### Pushover

[Pushover](https://pushover.net/) är en tjänst för att kunna skicka
pushnotiser till din Android, IOS eller webbläsare. Man kan få Flexget
att skicka en pushnotis varje gång den laddar hem något för att inte
missa nerladdningen.

Enda man behöver är några få rader i din YAML fil och ett konto hos
pushover.

`pushover:`
`userkey:`
`- uasdfVQ`
`apikey: aasdf6`
`title: Downloading {{series_name}}`
`message: Episode {{series_id}}`

[Category:Guider](/Category:Guider "wikilink")