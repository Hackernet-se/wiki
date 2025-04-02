---
title: Python
permalink: /Python/
---

Python är ett objektorienterat programspråk som siktar på att vara
funktionellt och lättläst.

Installation
------------

Python följer med de flesta linux-distar.

`python -V`

**Pydoc**
Läsa hjälpfiler om moduler, klasser och funktioner.

`pydoc `<namn>
`pydoc open`
`pydoc file`
`pydoc os`

Manuellt ta reda på möjliga funktioner/methods i ett library.

`dir()`
`dir(`*`library`*`)`

Virtualenv
----------

Virtualenv är ett verktyg för att skapa isolerade Python environments.
Det skapar ett directory som innehåller alla nödvändiga executables för
att köra Python-projektet. Man kan sedan installera python-paket
oberoende av övriga system. Virtualenvwrapper tillhandahåller ett gäng
verktyg för att enklare jobba med virtualenv.

Setup

`sudo pip install virtualenvwrapper`
`echo '. /usr/local/bin/virtualenvwrapper.sh' >> .bashrc && source .bashrc`

Jobba med virtualenv

`mkvirtualenv test`
`deactivate`
`lsvirtualenv`
`workon test`

PIP
---

PIP är ett package management system som används för att installera
software packages skrivna i Python.

`sudo pip install `<package>

Eller för att installera ett pip paket i din egen home folder kan du
skriva

`pip install `<package>` --user`

**Exempel HTTP Server**
Det finns flera olika webbservrar skrivna i python.

`sudo pip install lpthw.web`
`import web`

Referenslista
-------------

Här följer en lista på hur man gör diverse vanliga saker för den ovane.
Detta utgår från python 2.7.

Variabel

`nummer = 102`

Output, print från variabel

`print "The name is %s and %d." % (namn, nummer)`

Input

`x = raw_input(">> ")`
`x = int(raw_input(">> "))`

Läsa fil

`filnamn = raw_input(">> ")`
`fil = open(filnamn)`
`print fil.read()`

Skriva till fil

`fil = open(filename, 'w')`
`line1 = raw_input("line 1: ")`
`fil.write(line1)`
`fil.close()`

Definiera funktion och kalla på den.

`def funk1():`
`   print "Detta ar en funktion"`

`funk1()`

Return value

`def funk1(x):`
`   return x + 4`

`value = funk1(20)`

Avsluta, ctrl + d

`exit(0) # i script`
`quit() # i cli`

**If_then_else**

`print "Valj 1 eller 2"`
`valet = raw_input(">> ")`

`if valet == "1":`
`   print "You is 1"`
`elif valet == "2":`
`   print "You is 2"`
`else:`
`   print "You die"`

**For-loop**

`the_count = [1, 2, 3, 4, 5]`
`for number in the_count:`
`   print "This is %d" % number`

**Lista**

`lista = [1, 2, 3, 4, 5, 6, "hest" ];`
`print lista[0:2]`
`lista[2] = 20;`

Append

**Dictionary**

`dict = {'Name': 'Sara', 'Age': 20, 'Class': 'No'};`
`print dict['Name']`
`dict['Age'] = 21;`

Add new entry

`dict['School'] = "Yes";`

**Password**
Get password, hidden

`import getpass`
`secretx = getpass.getpass("Enter password:")`

**Grundläggande sanitetscheckar**

`pip install pep8 pylint pyflakes`

`pep8 the_script.py`
`pylint the_script.py`
`pyflakes the_script.py`

netaddr
-------

netaddr är ett network address manipulation library. Man kan jobba med
IP-adresser och nät.

`sudo pip install netaddr`

Usage

`from netaddr import *`
`cidr = IPNetwork(raw_input("CIDR-notation: "))`
`firstip = cidr[1]`
`netmask = cidr.netmask`

OOP
---

Python är ett Object Oriented Programming Language vilket innebär att
man har stöd för att bygga objekt. Python är designat så att allting är
ett objekt vilket t.ex. innebär att datatypen "string" i python också är
ett objekt. Exempel på hur man skapar en class och instansierar ett
objekt.

`class VLAN:`
`    def __init__(self, id, name):`
`        self.id = id`
`        self.name = name`

`vlan10 = VLAN(10, "Test")`

HTTP server
-----------

Om man behöver sätta upp en http server snabbt o enkelt kan man göra det
med Python.

Börja med att gå till det directory du vill dela ut.

`cd /home/sparco/secret-hackernet-stuff`

Kör sedan följande kommando för att starta en python webserver som
lyssnar på port 8000 på alla interface:

**Python 2.7**

`python -m SimpleHTTPServer`

**Python 3.X**

`python -m http.server`

[Category:Guider](/Category:Guider "wikilink")