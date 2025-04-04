---
title: Kickstart ESXi
permalink: /Kickstart_ESXi/
---

ESXi 6.0

`accepteula`
`install --firstdisk --overwritevmfs`
`#For USB install use below instead`
`#install --firstdisk --novmfsondisk`
`rootpw bueno`
`keyboard Swedish`
`reboot`

`network --bootproto=static --device=vmnic0 --hostname=esxi2.hackernet.se --ip=172.20.0.2 --netmask=255.255.255.0 --gateway=172.20.0.1 --nameserver=172.20.0.10 --addvmportgroup=false`

`%firstboot --interpreter=busybox`

`#SSH`
`vim-cmd hostsvc/enable_ssh`
`vim-cmd hostsvc/start_ssh`
`esxcli system settings advanced set -o /UserVars/SuppressShellWarning -i 1`

`vim-cmd hostsvc/datastore/rename datastore1 "LocalHDD"`
`vim-cmd vimsvc/license --set 11111-BBBBB-CCCCC-BH951-CAW3U`
`esxcli system module parameters set -m tcpip3 -p ipv6=0`

`cat > /etc/ntp.conf << __NTP_CONFIG__`
`restrict default kod nomodify notrap noquerynopeer`
`restrict 127.0.0.1`
`server 0.vmware.pool.ntp.org`
`server 1.vmware.pool.ntp.org`
`__NTP_CONFIG__`
`/sbin/chkconfig ntpd on`

`# EHC`
`esxcli software vib install -v `[`http://download3.vmware.com/software/vmw-tools/esxui/esxui_signed.vib`](http://download3.vmware.com/software/vmw-tools/esxui/esxui_signed.vib)

`#If planning on running nested ESXi, uncomment`
`#grep -i "vhv.enable" /etc/vmware/config || echo "vhv.enable = \"TRUE\"" >> /etc/vmware/config`

`# Mgmt`
`esxcli network vswitch standard portgroup set --portgroup-name "Management Network" --vlan-id 2`

`# vSwitch0`
`esxcli network vswitch standard set --mtu 9000 --cdp-status both --vswitch-name vSwitch0`
`esxcli network vswitch standard portgroup add --portgroup-name LAN --vswitch-name vSwitch0`

`# vSwitch1`
`esxcli network vswitch standard add --ports 256 --vswitch-name vSwitch1`
`esxcli network vswitch standard uplink add --uplink-name vmnic1 --vswitch-name vSwitch1`
`esxcli network vswitch standard set --cdp-status listen --vswitch-name vSwitch1`
`esxcli network vswitch standard portgroup add --portgroup-name WAN --vswitch-name vSwitch1`

`# vSwitch2 `
`esxcli network vswitch standard add --ports 256 --vswitch-name vSwitch2`
`esxcli network vswitch standard uplink add --uplink-name vmnic2 --vswitch-name vSwitch2`
`esxcli network vswitch standard set --mtu 9000 --cdp-status both --vswitch-name vSwitch2`
`esxcli network vswitch standard portgroup add --portgroup-name DMZ1 --vswitch-name vSwitch2`
`esxcli network vswitch standard portgroup set --portgroup-name DMZ1 --vlan-id 1`
`esxcli network vswitch standard portgroup add --portgroup-name DMZ2 --vswitch-name vSwitch2`
`esxcli network vswitch standard portgroup set --portgroup-name DMZ2 --vlan-id 2`

[Category:Kickstart](/Category:Kickstart "wikilink")
[Category:VMware](/Category:VMware "wikilink")