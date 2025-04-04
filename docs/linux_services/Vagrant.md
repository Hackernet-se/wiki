---
title: Vagrant
permalink: /Vagrant/
---

Vagrant är program som skapar och konfigurerar virtuella
utvecklingsmiljöer. Det kan ses som en högre nivå av virtualisering än
VirtualBox, VMware, [KVM](/KVM "wikilink") och Linux Containers (LXC).
Sedan version 1.6 har Vagrant inbyggt stöd för Docker containers.

Installation
------------

Fedora

`dnf install vagrant `

Providers
---------

Vagrant gör ingen virtualisering utan det görs av en underliggande
provider, t.ex. virtualbox, vmware, AWS eller docker. Virtualbox är
default. En provider måste finnas tillgänglig på maskinen där vagrant
ska användas. Installera virtualbox:

[`http://www.if-not-true-then-false.com/2010/install-virtualbox-with-yum-on-fedora-centos-red-hat-rhel/`](http://www.if-not-true-then-false.com/2010/install-virtualbox-with-yum-on-fedora-centos-red-hat-rhel/)

Providers installeras som plugins och listas med. För virtualbox behövs
ingen plugin.

`vagrant plugin list`

##### VMware Workstation

vagrant-vmware-workstation är en kommersiell produkt och kräver licens.

Boxes
-----

Istället för att bygga en virtuell maskin från grunden varje gång
använder Vagrant en grundimage för att snabbt klona en virtuell maskin.
Dessa imagear kallas på Vagrantspråk för boxes. Att ange vilken box som
ska användas för din Vagrantmiljö är alltid det första steget när du ska
skapa en ny Vagrantfile. Tillgängliga boxes:
<https://atlas.hashicorp.com/boxes/search>

`vagrant box add ubuntu/trusty64 `

Boxes lagras i \~/.vagrant.d/boxes/

Konfiguration
-------------

Generera Vagrantfile

`mkdir vagrant && cd vagrant`
`vagrant init ubuntu/trusty64`

Starta environment. Detta kommando startar miljö utifrån den Vagrantfile
som finns det directory du kör kommandot i.

`vagrant up --provider virtualbox`

Anslut till den virtuella maskinen

`vagrant ssh`

Städa

`vagrant destroy`

Lista skapade vagrantmiljöer

`vagrant global-status`

Plugins
-------

Det finns många plugins till vagrant. <http://vagrant-lists.github.io/>

### vSphere

Se <https://github.com/nsidc/vagrant-vsphere>

[Category:Guider](/Category:Guider "wikilink")