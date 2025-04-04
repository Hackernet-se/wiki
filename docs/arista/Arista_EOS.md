---
title: Arista EOS
permalink: /Arista_EOS/
---

Arista Extensible Operating System är ett Linux-based network operating
system. EOS levereras som en image som kan köras på alla plattformar,
även som virtuel maskin. EOS är väldigt Cisco IOS likt i sina kommandon.

vEOS
====

vEOS fungerar på de flesta virtualiseringsplattformar inklusive
[EVE-NG](/EVE-NG "wikilink"), [KVM](/KVM "wikilink"), VirtualBox,
[ESXi](/VMware_ESXi "wikilink") och Hyper-V. vEOS-lab har en drivrutin
som heter Elba, den emulerar hårdvara. En del features saknar vEOS-lab
stöd för, t.ex. storm-control och IPsec.

### Installation

För nyare vEOS (4.15) vill man ha 2GB RAM.

**ESXi**

[`https://eos.arista.com/running-veos-on-esxi-5-5/`](https://eos.arista.com/running-veos-on-esxi-5-5/)

**Virtualbox**

`vboxmanage createvm --name vEOS02 --ostype Fedora_64 --register`
`VBoxManage modifyvm vEOS02 --memory 2048`
`VBoxManage modifyvm vEOS02 --nic1 intnet`
`VBoxManage modifyvm vEOS02 --intnet1 Mgmt1`
`VBoxManage modifyvm vEOS02 --nicpromisc1 allow-vms`
`VBoxManage modifyvm vEOS02 --cableconnected1 on`
`VBoxManage storagectl vEOS02 --name "IDE Controller" --add ide`
`VBoxManage storageattach vEOS02 --storagectl "IDE Controller" --port 0 --device 0 --type hdd --medium /path/vEOS-lab-4.15.2.1F.vmdk`
`VBoxManage storageattach vEOS02 --storagectl "IDE Controller" --port 1 --device 0 --type dvddrive --medium /path/Aboot-veos-2.1.0.iso`

**Credentials**
admin: <no password>

Konfiguration
=============

Grundkonfiguration

`hostname vEOS-01`
`logging console notifications`
`logging monitor informational`
`logging synchronous`
`logging buffered 2000`
`username wizkid privilege 15 secret `<password>

`show user-account`

Management interface

`interface Management1`
` ip address 10.0.0.10/24`
` no shut`

`lldp management-address Management1`

### SSH

SSH är påslaget default, det som behöver konfas är användare och
IP-adress. Ska man använda EOS som scp-server måste det user-konto man
loggar in med ha "full access", dvs privilege 15.

`management ssh`
` idle-timeout 1800`

Autentisering med SSH-nyckel

`copy scp:user@jumphost/home/user/.ssh/id_rsa.pub flash:`
`username `*`user`*` sshkey file flash:id_rsa.pub`

### Management VRF

`vrf definition MGMT `
` rd 100:100`

Första porten är Ma1

`interface ma1 `
` vrf forwarding MGMT `
` ip address 10.0.0.10 255.255.255.0`

### eAPI

En user behövs för att kunna använda eAPI. URL till API sandbox:
<https://><mgmt-ip>:443

`management api http-commands`
` no shutdown`
` !`
` vrf MGMT`
`  no shutdown`

`show management api http-commands `

Det finns även stöd för netconf och restconf

`management api netconf`
`  transport ssh MGMT`
`!`
`management api restconf`
`  transport https MGMT`

Diverse
=======

Show the current running-config for this sub mode

`show active`

Show diff between running and startup

`show running diff`

Backa till startup-konfig

`configure replace startup-config`

CLI history

`show history`

Slå på loggmeddelanden i SSH terminal.

`terminal monitor`

**Syslog**

`logging buffered 10000 notifications`
`logging host 10.0.0.12`
`show logging`
`show logg last 10 min`

**NTP**

`ntp server 10.0.0.12`

**DNS**

`ip name-server 8.8.8.8`
`show hosts`

**SCP Server**

`aaa authorization exec default local`

### Port mirroring

`monitor session 1 source interface `<interface>` [ rx | tx | both ]`
`monitor session 1 destination `<interface>

Begränsa på IP vad som ska speglas.

`monitor session 1 ip access-group `<ACL name>

### Iperf

[Iperf](/Iperf "wikilink") finns inbyggt i EOS. Dock tillåts inte tcp
5001 default.

`bash`
`sudo iptables -I INPUT -p tcp -m tcp --dport 5001 -j ACCEPT`
`iperf -s`

Klient

`iperf -c 10.0.0.10`

### Yum

Yum finns inbyggt i EOS men det finns inga repos default.

`bash`
`sudo nano /etc/yum.repos.d/fedora.repo`
`[fedora]`
`name=Fedora 14 – i386`
`failovermethod=priority`
`baseurl=`[`http://dl.fedoraproject.org/pub/archive/fedora/linux/releases/14/Everything/i386/os/`](http://dl.fedoraproject.org/pub/archive/fedora/linux/releases/14/Everything/i386/os/)
`exclude=kernel,fedora-logos`
`enabled=1`
`gpgcheck=0`

`sudo yum install iftop`

### Maintenance Mode

Sätt hela switchen i maintenance mode, då graceful stängs allt utom
management.

`maintenance`
` unit System`
`  quiesce`
`show maintenance`

[Category:Arista](/Category:Arista "wikilink")