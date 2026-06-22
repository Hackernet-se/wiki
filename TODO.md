# TODO List from Documentation
Vad som behöver göras för varje sida är typ:
### Kolla över alla bild länkar.
Bilderna funkar inte dom behöver länkas om.

Example
```
[<File:Cisco_BGP_Open.PNG>](/File:Cisco_BGP_Open.PNG "wikilink")
```
Till
```
![Cisco_BGP_Open.PNG](../img/Cisco_BGP_Open.PNG)
```
### Ta bort DIV taggar.
Flera sidor verkar fortfarande ha massa div taggar 
```
<div class="mw-collapsible-content">
```
### Ta bort Category
Mediawiki använde sig av följande för att kategorisera sidor
```
[Category:Cisco](/Category:Cisco "wikilink")
```
Det behöver vi ta bort. 
### Allmänt kolla över code block
Kolla över olika kod block så dom använder sig av ``` före och efter.
Många sidor har bara en ` för varje rad. 

Tex

`show flowspec summary `

`show bgp ipv4 flowspec `

Kan bli 
```
show flowspec summary
show bgp ipv4 flowspec
```
Om det är nån kod tex python, json, bash osv så kan man skriva tex ``` py för highlighta python kod. Se https://pygments.org/languages/ för fler språk. 



# Sidor Som är kvar att gå över.
Sätt ett X på en sida som är klar fixad så man vet vad som är kvar. 
- [x] Review and process: arista\Arista_BGP.md
- [x] Review and process: arista\Arista_EOS.md
- [x] Review and process: arista\Arista_EVPN.md
- [x] Review and process: arista\Arista_OSPF.md
- [x] Review and process: arista\Arista_VXLAN.md
- [x] Review and process: cisco\Cisco_ACI.md
- [x] Review and process: cisco\Cisco_ASA.md
- [x] Review and process: cisco\Cisco_ASA_VPN.md
- [x] Review and process: cisco\Cisco_BFD.md
- [x] Review and process: cisco\Cisco_BGP.md
- [x] Review and process: cisco\Cisco_BIER.md
- [x] Review and process: cisco\Cisco_CEF.md
- [x] Review and process: cisco\Cisco_CSR.md
- [x] Review and process: cisco\Cisco_DHCP.md
- [x] Review and process: cisco\Cisco_DMVPN.md
- [x] Review and process: cisco\Cisco_EIGRP.md
- [x] Review and process: cisco\Cisco_EVPN.md
- [x] Review and process: cisco\Cisco_EtherChannel.md
- [x] Review and process: cisco\Cisco_FC.md
- [x] Review and process: cisco\Cisco_FCoE.md
- [x] Review and process: cisco\Cisco_FHRP.md
- [x] Review and process: cisco\Cisco_FTD.md
- [x] Review and process: cisco\Cisco_GRE.md
- [x] Review and process: cisco\Cisco_HSRP.md
- [x] Review and process: cisco\Cisco_IGMP.md
- [x] Review and process: cisco\Cisco_IOS-XR.md
- [x] Review and process: cisco\Cisco_IOS.md
- [x] Review and process: cisco\Cisco_IPsec.md
- [x] Review and process: cisco\Cisco_IS-IS.md
- [x] Review and process: cisco\Cisco_L2VPN.md
- [x] Review and process: cisco\Cisco_L2_Security.md
- [x] Review and process: cisco\Cisco_L3_Security.md
- [x] Review and process: cisco\Cisco_LISP.md
- [x] Review and process: cisco\Cisco_Logging.md
- [x] Review and process: cisco\Cisco_MPLS-TE.md
- [x] Review and process: cisco\Cisco_MPLS.md
- [x] Review and process: cisco\Cisco_MST.md
- [x] Review and process: cisco\Cisco_MVPN.md
- [x] Review and process: cisco\Cisco_Multicast.md
- [x] Review and process: cisco\Cisco_NAT.md
- [x] Review and process: cisco\Cisco_NetFlow.md
- [x] Review and process: cisco\Cisco_Nexus.md
- [x] Review and process: cisco\Cisco_OSPF.md
- [x] Review and process: cisco\Cisco_OSPFv3.md
- [x] Review and process: cisco\Cisco_OTV.md
- [x] Review and process: cisco\Cisco_PCE.md
- [x] Review and process: cisco\Cisco_PE-CE.md
- [x] Review and process: cisco\Cisco_PIM.md
- [x] Review and process: cisco\Cisco_PfR.md
- [x] Review and process: cisco\Cisco_QoS.md
- [x] Review and process: cisco\Cisco_RIP.md
- [x] Review and process: cisco\Cisco_Routing.md
- [x] Review and process: cisco\Cisco_SNMP.md
- [x] Review and process: cisco\Cisco_SPAN.md
- [x] Review and process: cisco\Cisco_SR.md
- [x] Review and process: cisco\Cisco_STP.md
- [x] Review and process: cisco\Cisco_Security.md
- [x] Review and process: cisco\Cisco_Services.md
- [x] Review and process: cisco\Cisco_TCLSH.md
- [x] Review and process: cisco\Cisco_UDLD.md
- [x] Review and process: cisco\Cisco_VLAN.md
- [x] Review and process: cisco\Cisco_VSS.md
- [x] Review and process: cisco\Cisco_VTP.md
- [x] Review and process: cisco\Cisco_VXLAN.md
- [x] Review and process: cisco\Cisco_WAN.md
- [x] Review and process: cisco\Cisco_Wireless.md
- [x] Review and process: cisco\Cisco_pyATS.md
- [x] Review and process: cisco\Nexus_1000V.md
- [x] Review and process: cisco\Nexus_FabricPath.md
- [x] Review and process: cisco\Nexus_VDC.md
- [x] Review and process: cisco\Nexus_vPC.md
- [x] Review and process: cumulus\Cumulus_EVPN.md
- [x] Review and process: cumulus\Cumulus_Linux.md
- [x] Review and process: extreme\Extreme_VLAN.md
- [x] Review and process: extreme\Extreme_XOS.md
- [x] Review and process: f5\F5_Big-IP.md
- [ ] Review and process: gamla-General_disclaimer.md
- [x] Review and process: gamla-mainpage.md
- [x] Review and process: hardware\HPE_BL460c_G7.md
- [x] Review and process: hardware\HPE_BL460c_Gen9.md
- [x] Review and process: hardware\Lenovo_BIOS_update.md
- [x] Review and process: index.md
- [x] Review and process: juniper\Juniper_Aggregated_Ethernet.md
- [x] Review and process: juniper\Juniper_JunOS.md
- [x] Review and process: juniper\Juniper_VLAN.md
- [x] Review and process: juniper\Juniper_VRRP.md
- [x] Review and process: linux.md
- [x] Review and process: linux_kickstart\Kickstart_Debian.md
- [x] Review and process: linux_kickstart\Kickstart_Fedora.md
- [x] Review and process: linux_kickstart\Kickstart_Ubuntu.md
- [x] Review and process: linux_networking\BIRD.md
- [x] Review and process: linux_networking\Bridge.md
- [x] Review and process: linux_networking\ExaBGP.md
- [x] Review and process: linux_networking\IPv6.md
- [x] Review and process: linux_networking\Mininet.md
- [x] Review and process: linux_networking\Netmiko.md
- [x] Review and process: linux_networking\Netsim-tools.md
- [x] Review and process: linux_networking\OpenDaylight.md
- [x] Review and process: linux_networking\Open_vSwitch.md
- [x] Review and process: linux_networking\Quagga.md
- [x] Review and process: linux_networking\Suzieq.md
- [x] Review and process: linux_networking\VPP.md
- [x] Review and process: linux_networking\VyOS.md
- [x] Review and process: linux_os\Debian.md
- [x] Review and process: linux_os\Fedora.md
- [x] Review and process: linux_os\Kali_Linux.md
- [x] Review and process: linux_os\OS_X.md
- [x] Review and process: linux_os\Security_Onion.md
- [x] Review and process: linux_os\Ubuntu.md
- [x] Review and process: linux_services\Ansible.md
- [x] Review and process: linux_services\Apache.md
- [x] Review and process: linux_services\AutoFS.md
- [x] Review and process: linux_services\BIND.md
- [x] Review and process: linux_services\Bcache.md
- [x] Review and process: linux_services\Beeswarm.md
- [x] Review and process: linux_services\Cacti.md
- [x] Review and process: linux_services\Certbot.md
- [x] Review and process: linux_services\Clogin.md
- [x] Review and process: linux_services\Digitala_Certifikat.md
- [x] Review and process: linux_services\Docker.md
- [x] Review and process: linux_services\ELK.md
- [ ] Review and process: linux_services\EVE-NG.md
- [x] Review and process: linux_services\Emby_Server.md
- [x] Review and process: linux_services\Fabric.md
- [x] Review and process: linux_services\Fail2Ban.md
- [x] Review and process: linux_services\FastNetMon.md
- [x] Review and process: linux_services\Flexget.md
- [x] Review and process: linux_services\Foreman.md
- [x] Review and process: linux_services\FreeIPA.md
- [x] Review and process: linux_services\GNS3.md
- [x] Review and process: linux_services\Gammu.md
- [x] Review and process: linux_services\Git.md
- [x] Review and process: linux_services\Gitlab.md
- [x] Review and process: linux_services\GlusterFS.md
- [ ] Review and process: linux_services\Golang.md
- [x] Review and process: linux_services\Google_Authenticator.md
- [x] Review and process: linux_services\Grafana.md
- [x] Review and process: linux_services\Graylog.md
- [x] Review and process: linux_services\HashiCorp_Vault.md
- [x] Review and process: linux_services\Hastebin.md
- [x] Review and process: linux_services\IPXE.md
- [x] Review and process: linux_services\IRedMail.md
- [x] Review and process: linux_services\ISC_DHCP.md
- [x] Review and process: linux_services\Icinga.md
- [x] Review and process: linux_services\InspIRCd.md
- [x] Review and process: linux_services\Jumpgate.md
- [ ] Review and process: linux_services\KVM.md
- [x] Review and process: linux_services\Kea.md
- [x] Review and process: linux_services\LAMP.md
- [x] Review and process: linux_services\LUKS.md
- [x] Review and process: linux_services\LXD.md
- [x] Review and process: linux_services\Let's_Encrypt.md
- [x] Review and process: linux_services\LibreNMS.md
- [x] Review and process: linux_services\Logstash.md
- [x] Review and process: linux_services\MEAN.md
- [x] Review and process: linux_services\Mailserver.md
- [x] Review and process: linux_services\MediaWiki.md
- [x] Review and process: linux_services\ModSecurity.md
- [x] Review and process: linux_services\Multiarch.md
- [x] Review and process: linux_services\MySQL.md
- [x] Review and process: linux_services\NFS.md
- [x] Review and process: linux_services\NIPAP.md
- [x] Review and process: linux_services\Netdisco.md
- [x] Review and process: linux_services\Network.md
- [x] Review and process: linux_services\Nginx.md
- [x] Review and process: linux_services\Ntopng.md
- [x] Review and process: linux_services\OSSEC.md
- [x] Review and process: linux_services\Ookla_Speedtest_Mini.md
- [x] Review and process: linux_services\OpenLDAP.md
- [x] Review and process: linux_services\OpenShift.md
- [x] Review and process: linux_services\OpenVPN.md
- [x] Review and process: linux_services\Owncloud.md
- [x] Review and process: linux_services\Oxidized.md
- [x] Review and process: linux_services\PXE-Deploy.md
- [x] Review and process: linux_services\Pagespeed.md
- [x] Review and process: linux_services\PhpIPAM.md
- [x] Review and process: linux_services\Pi-hole.md
- [x] Review and process: linux_services\Piwik.md
- [x] Review and process: linux_services\Pmacct.md
- [x] Review and process: linux_services\PowerDNS.md
- [x] Review and process: linux_services\Prometheus.md
- [x] Review and process: linux_services\Puppet.md
- [ ] Review and process: linux_services\Python.md
- [x] Review and process: linux_services\Quota.md
- [x] Review and process: linux_services\Rancid.md
- [x] Review and process: linux_services\Rar2fs.md
- [x] Review and process: linux_services\RatticDB.md
- [x] Review and process: linux_services\Realmd.md
- [x] Review and process: linux_services\Roundcube.md
- [x] Review and process: linux_services\Rsyslog.md
- [x] Review and process: linux_services\SELinux.md
- [x] Review and process: linux_services\SSH.md
- [x] Review and process: linux_services\Shaltúre.md
- [x] Review and process: linux_services\SmokePing.md
- [x] Review and process: linux_services\Spacewalk.md
- [x] Review and process: linux_services\Squid.md
- [x] Review and process: linux_services\Sshttp.md
- [x] Review and process: linux_services\Syntaxhighlight.md
- [x] Review and process: linux_services\TFTP.md
- [x] Review and process: linux_services\Tor.md
- [x] Review and process: linux_services\Transmission.md
- [x] Review and process: linux_services\Ulteo.md
- [x] Review and process: linux_services\Vagrant.md
- [x] Review and process: linux_services\Vsftpd.md
- [x] Review and process: linux_services\Weechat.md
- [x] Review and process: linux_services\Xming.md
- [x] Review and process: linux_services\ZFS.md
- [x] Review and process: linux_tools\Apt.md
- [x] Review and process: linux_tools\Bash.md
- [x] Review and process: linux_tools\Cron.md
- [x] Review and process: linux_tools\DNF.md
- [x] Review and process: linux_tools\Dd.md
- [x] Review and process: linux_tools\Dialog.md
- [x] Review and process: linux_tools\Dnstracer.md
- [x] Review and process: linux_tools\Dumpcap.md
- [x] Review and process: linux_tools\EFI.md
- [x] Review and process: linux_tools\FirewallD.md
- [x] Review and process: linux_tools\Frandom.md
- [x] Review and process: linux_tools\Hdparm.md
- [x] Review and process: linux_tools\IPMI.md
- [x] Review and process: linux_tools\Iperf.md
- [x] Review and process: linux_tools\Iproute2.md
- [x] Review and process: linux_tools\Iptables.md
- [x] Review and process: linux_tools\JQ.md
- [x] Review and process: linux_tools\Keepalived.md
- [x] Review and process: linux_tools\Mdadm.md
- [x] Review and process: linux_tools\NTP.md
- [x] Review and process: linux_tools\Nameif.md
- [x] Review and process: linux_tools\Psql.md
- [x] Review and process: linux_tools\Rsync.md
- [x] Review and process: linux_tools\Scapy.md
- [x] Review and process: linux_tools\System_storage_manager.md
- [x] Review and process: linux_tools\Systemd.md
- [x] Review and process: linux_tools\Tcpdump.md
- [x] Review and process: linux_tools\Tmux.md
- [x] Review and process: linux_tools\Tree.md
- [x] Review and process: unifi\UniFi.md
- [x] Review and process: vmware\Distributed_Switch.md
- [x] Review and process: vmware\ESXi_Secure_Boot.md
- [x] Review and process: vmware\ESXi_Security.md
- [x] Review and process: vmware\ESXi_pktcap.md
- [x] Review and process: vmware\Kickstart_ESXi.md
- [x] Review and process: vmware\PSC.md
- [x] Review and process: vmware\PowerCLI.md
- [x] Review and process: vmware\Standard_vSwitch.md
- [x] Review and process: vmware\VM_Encryption.md
- [x] Review and process: vmware\VMware_ESXi.md
- [x] Review and process: vmware\VMware_Vsphere_Client.md
- [x] Review and process: vmware\VMware_vCenter.md
- [x] Review and process: vmware\VSphere_Permissions.md
- [x] Review and process: windows\Batch_script.md
- [x] Review and process: windows\BitLocker.md
- [x] Review and process: windows\Chocolatey.md
- [x] Review and process: windows\InSSIDer.md
- [x] Review and process: windows\Skärmsläckare.md
