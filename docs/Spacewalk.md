---
title: Spacewalk
permalink: /Spacewalk/
---

Spacewalk är ett management system för Red Hat baserade system som
CentOS, Fedora. Allt sköts i ett snyggt web interface.

##### Features

-   Inventera system (Hård och mjukvara).
-   Installera och uppdatera program.
-   Kickstarta dina servrar.
-   Skicka ut konfigurations filer till servrar.
-   Starta/stoppa/konfigurera virtuella gäster (KVM & XEN).

Förberedelse
------------

Lägg till lite nya repositories som behövs.

**EPEL repository:**

`yum install epel-release`

**JPackage repository:**

`cat > /etc/yum.repos.d/jpackage-generic.repo << EOF`
`[jpackage-generic]`
`name=JPackage generic`
`#baseurl=`[`http://mirrors.dotsrc.org/pub/jpackage/5.0/generic/free/`](http://mirrors.dotsrc.org/pub/jpackage/5.0/generic/free/)
`mirrorlist=`[`http://www.jpackage.org/mirrorlist.php?dist=generic&type=free&release=5.0`](http://www.jpackage.org/mirrorlist.php?dist=generic&type=free&release=5.0)
`enabled=1`
`gpgcheck=1`
`gpgkey=`[`http://www.jpackage.org/jpackage.asc`](http://www.jpackage.org/jpackage.asc)
`EOF`

**Spacewalk repository:**

Beror på vilket dist du kommer köra. I skrivande stund är version
**2.4** den senaste.

**Red Hat Enterprise Linux 6, Scientific Linux 6, CentOS 6**

`rpm -Uvh `[`http://yum.spacewalkproject.org/2.4/RHEL/6/x86_64/spacewalk-repo-2.4-3.el6.noarch.rpm`](http://yum.spacewalkproject.org/2.4/RHEL/6/x86_64/spacewalk-repo-2.4-3.el6.noarch.rpm)

**Red Hat Enterprise Linux 7, Scientific Linux 7, CentOS 7**

`rpm -Uvh `[`http://yum.spacewalkproject.org/2.4/RHEL/7/x86_64/spacewalk-repo-2.4-3.el7.noarch.rpm`](http://yum.spacewalkproject.org/2.4/RHEL/7/x86_64/spacewalk-repo-2.4-3.el7.noarch.rpm)

**Fedora 21**

`rpm -Uvh `[`http://yum.spacewalkproject.org/2.4/Fedora/21/x86_64/spacewalk-repo-2.4-3.fc21.noarch.rpm`](http://yum.spacewalkproject.org/2.4/Fedora/21/x86_64/spacewalk-repo-2.4-3.fc21.noarch.rpm)

**Fedora 22**

`rpm -Uvh `[`http://yum.spacewalkproject.org/2.4/Fedora/22/x86_64/spacewalk-repo-2.4-3.fc22.noarch.rpm`](http://yum.spacewalkproject.org/2.4/Fedora/22/x86_64/spacewalk-repo-2.4-3.fc22.noarch.rpm)

Uppdatera repona.

`yum repolist && yum update`

Installera
----------

Spacewalk använder en databas för att spara sin data. Default så används
en inbyggd PostgreSQL databas. Det går också att använda en Oracle RDBMS
version 10g eller högre.

Denna guiden använder den inbyggda databasen:

`yum install spacewalk-setup-postgresql`

Installera sedan Spacewalk:

`yum install spacewalk-postgresql`

För att kunna nå web interfacet och kunna använda andra tjänster behöver
man sätta på några portar.

`firewall-cmd --add-service=https --permanent`
`firewall-cmd --add-service=http --permanent`

För att kunna pusha saker till dina klienter behöver man enabla port
**5222**. Om man tänkt använda Spacewalk proxy behöver man porten
**5269**. Port **69 UDP** behövs om man tänkt använda tftp.

Ladda sedan om brandväggen.

`firewall-cmd --reload`

Spacewalk måste kunna resolva sitt FQDN. Går inte det så lägg in det i
host filen **/etc/hosts**

Kör följande kommando och svara på frågorna.

`spacewalk-setup --disconnected`

Surfa sedan in på din spacewalk server **<https://hostname/>** och skapa
ett inlogg.

[Category:Guider](/Category:Guider "wikilink")