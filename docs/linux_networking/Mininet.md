---
title: Mininet
permalink: /Mininet/
---

An Instant Virtual Network on your computer.

Intro: <https://www.youtube.com/watch?v=jmlgXaocwiE>

Projektets hemsida: <http://mininet.org/>

Installation
------------

`wget `[`https://raw.github.com/mininet/mininet/master/util/vm/install-mininet-vm.sh`](https://raw.github.com/mininet/mininet/master/util/vm/install-mininet-vm.sh)
`bash -v install-mininet-vm.sh master`
`~/mininet/bin/mn --version`
`cd ~/mininet; git fetch --all; git checkout master; git pull --rebase origin master`
`sudo -n make install`
`sudo -n mn --test pingall`
`sudo sed -i -e 's/^GRUB_TERMINAL=serial/#GRUB_TERMINAL=serial/' /etc/default/grub; sudo update-grub`
`reboot`

### OVF

Ladda ned ovf:n och importera till ditt vmware-system. HWversion ligger
på 11 så det kanske du måste sänka i vmx-filen för att kunna starta
vm:n.
Credentials: mininet - mininet

Basic
-----

<http://mininet.org/walkthrough/>

Kör igenom kommandona för att komma igång.

`sudo mn`

Setups
------

<http://sdnhub.org/resources/useful-mininet-setups/>

Controller
----------

Det blir lite roligare om man har en controller till sitt virtuella
nätverk så man kan peka och klicka lite.

`sudo mn --controller=remote,ip=`<IP-to-controller>`,port=6633 --switch ovsk,protocols=OpenFlow13 --topo=tree,3`

<http://mininet.org/blog/2013/06/03/automating-controller-startup/>

### OpenDaylight

Se [OpenDaylight](/OpenDaylight "wikilink")

### Floodlight

**Installation**

`sudo apt-get update && sudo apt-get -y install build-essential default-jdk ant python-dev eclipse screen`
`git clone `[`git://github.com/floodlight/floodlight.git`](git://github.com/floodlight/floodlight.git)
`cd floodlight && git checkout fl-last-passed-build`
`ant;`
`sudo mkdir /var/lib/floodlight && sudo chmod 777 /var/lib/floodlight`
`screen`
`java -jar target/floodlight.jar`

**<http://IP:8080/ui/index.html>**

`sudo mn --controller=remote,ip=127.0.0.1,port=6633 --switch ovsk,protocols=OpenFlow13`

[Category:Network](/Category:Network "wikilink")