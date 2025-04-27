---
title: Foreman
permalink: /Foreman/
---

Foreman är ett lifecycle management tool för on-premise VM's, bare-metal
eller i cloud hos Amazon, Google, Microsoft eller Rackspace. Foreman
klarar av provisioning och configuration till orchestration och
monitorering. Till hjälp har man en Foreman Smart-Proxy som managerar
TFTP, DHCP, DNS, Puppet, Puppet CA, Ansible, Salt och Chef.

Foreman styrs med hjälp av ett webbaserat GUI, CLI eller ett REST API
och klarar av allt från 1 server till 10 000 servrar.

Foremans arkitektur
===================

Foreman agerar frontend mot användarna. Smart-Proxyn förser tjänster med
ett API som foreman kan agera mot.
[790px](/File:Foreman_architecture.png "wikilink")

Installation
============
=== "CentOS 7"

  Börja med att lägga till Puppet 5.X repot som är det rekommenderade.
  
  `yum -y install `[`https://yum.puppetlabs.com/puppet5/puppet5-release-el-7.noarch.rpm`](https://yum.puppetlabs.com/puppet5/puppet5-release-el-7.noarch.rpm)
  
  Installera sedan EPEL (Extra Packages for Enterprise Linux) och Foreman
  repot.
  
  `yum -y install `[`http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm`](http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm)
  `yum -y install `[`https://yum.theforeman.org/releases/1.16/el7/x86_64/foreman-release.rpm`](https://yum.theforeman.org/releases/1.16/el7/x86_64/foreman-release.rpm)
  
  Ladda sedan hem Foreman.
  
  `yum -y install foreman-installer`

=== "Ubuntu 16.04"
  Börja med att lägga till Puppet 4.X repot som är det rekommenderade.
  
  `apt-get -y install ca-certificates`
  `wget `[`https://apt.puppetlabs.com/puppet5-release-xenial.deb`](https://apt.puppetlabs.com/puppet5-release-xenial.deb)
  `dpkg -i puppet5-release-xenial.deb`
  
  Lägg sedan till Foreman repot.
  
  `echo "deb `[`http://deb.theforeman.org/`](http://deb.theforeman.org/)` xenial 1.16" > /etc/apt/sources.list.d/foreman.list`
  `echo "deb `[`http://deb.theforeman.org/`](http://deb.theforeman.org/)` plugins 1.16" >> /etc/apt/sources.list.d/foreman.list`
  `apt-get -y install ca-certificates`
  `wget -q `[`https://deb.theforeman.org/pubkey.gpg`](https://deb.theforeman.org/pubkey.gpg)` -O- | apt-key add -`
  
  Ladda sedan hem Foreman.
  
  `apt-get update && apt-get -y install foreman-installer`

Kör sedan Foreman installer.

`foreman-installer -i \`
`--enable-foreman-compute-vmware \`
`--enable-foreman-plugin-templates \`
`--enable-foreman-plugin-setup \`
`--enable-foreman-cli \`
`--enable-foreman \`
`--enable-foreman-proxy \`
`--enable-puppet \`
`--foreman-proxy-tftp=true `

Installationen körs i en non-interactive läge som standard. Men
konfigurationen kan ändras genom att lägga till options från
**foreman-installer --help**. Eller så kan man välja att köra installern
i interaktivt läge med **foreman-installer -i**.

Installern här över är baserad på en miljö där DHCP och DNS sköts av sig
självt eller genom andra system. Och Foreman kommer bara att ta hand om
TFTP servern och provisionering med hjälp av Puppet. Installerar också
pluginet för att kunna skapa VM's på en vmware miljö.

När installern kört klart så ska man få upp liknande info ruta.

`* Foreman is running at `[`https://foreman.hackernet.se`](https://foreman.hackernet.se)
`       Initial credentials are admin / 3ekw5xtyXCoXxS29`
`* Foreman Proxy is running at `[`https://foreman.hackernet.se:8443`](https://foreman.hackernet.se:8443)
`* Puppetmaster is running at port 8140`
`The full log is at /var/log/foreman-installer/foreman-installer.log`