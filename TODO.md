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
- [ ] Review and process: arista\Arista_BGP.md
- [ ] Review and process: arista\Arista_EOS.md
- [ ] Review and process: arista\Arista_EVPN.md
- [ ] Review and process: arista\Arista_OSPF.md
- [ ] Review and process: arista\Arista_VXLAN.md
- [ ] Review and process: cisco\Cisco_ACI.md
- [ ] Review and process: cisco\Cisco_ASA.md
- [ ] Review and process: cisco\Cisco_ASA_VPN.md
- [ ] Review and process: cisco\Cisco_BFD.md
- [ ] Review and process: cisco\Cisco_BGP.md
- [ ] Review and process: cisco\Cisco_BIER.md
- [ ] Review and process: cisco\Cisco_CEF.md
- [ ] Review and process: cisco\Cisco_CSR.md
- [ ] Review and process: cisco\Cisco_DHCP.md
- [ ] Review and process: cisco\Cisco_DMVPN.md
- [ ] Review and process: cisco\Cisco_EIGRP.md
- [ ] Review and process: cisco\Cisco_EVPN.md
- [ ] Review and process: cisco\Cisco_EtherChannel.md
- [ ] Review and process: cisco\Cisco_FC.md
- [ ] Review and process: cisco\Cisco_FCoE.md
- [ ] Review and process: cisco\Cisco_FHRP.md
- [ ] Review and process: cisco\Cisco_FTD.md
- [ ] Review and process: cisco\Cisco_GRE.md
- [ ] Review and process: cisco\Cisco_HSRP.md
- [ ] Review and process: cisco\Cisco_IGMP.md
- [ ] Review and process: cisco\Cisco_IOS-XR.md
- [ ] Review and process: cisco\Cisco_IOS.md
- [ ] Review and process: cisco\Cisco_IPsec.md
- [ ] Review and process: cisco\Cisco_IS-IS.md
- [ ] Review and process: cisco\Cisco_L2VPN.md
- [ ] Review and process: cisco\Cisco_L2_Security.md
- [ ] Review and process: cisco\Cisco_L3_Security.md
- [ ] Review and process: cisco\Cisco_LISP.md
- [ ] Review and process: cisco\Cisco_Logging.md
- [ ] Review and process: cisco\Cisco_MPLS-TE.md
- [ ] Review and process: cisco\Cisco_MPLS.md
- [ ] Review and process: cisco\Cisco_MST.md
- [ ] Review and process: cisco\Cisco_MVPN.md
- [ ] Review and process: cisco\Cisco_Multicast.md
- [ ] Review and process: cisco\Cisco_NAT.md
- [ ] Review and process: cisco\Cisco_NetFlow.md
- [ ] Review and process: cisco\Cisco_Nexus.md
- [ ] Review and process: cisco\Cisco_OSPF.md
- [ ] Review and process: cisco\Cisco_OSPFv3.md
- [ ] Review and process: cisco\Cisco_OTV.md
- [ ] Review and process: cisco\Cisco_PCE.md
- [ ] Review and process: cisco\Cisco_PE-CE.md
- [ ] Review and process: cisco\Cisco_PIM.md
- [ ] Review and process: cisco\Cisco_PfR.md
- [ ] Review and process: cisco\Cisco_QoS.md
- [ ] Review and process: cisco\Cisco_RIP.md
- [ ] Review and process: cisco\Cisco_Routing.md
- [ ] Review and process: cisco\Cisco_SNMP.md
- [ ] Review and process: cisco\Cisco_SPAN.md
- [ ] Review and process: cisco\Cisco_SR.md
- [ ] Review and process: cisco\Cisco_STP.md
- [ ] Review and process: cisco\Cisco_Security.md
- [ ] Review and process: cisco\Cisco_Services.md
- [ ] Review and process: cisco\Cisco_TCLSH.md
- [ ] Review and process: cisco\Cisco_UDLD.md
- [ ] Review and process: cisco\Cisco_VLAN.md
- [ ] Review and process: cisco\Cisco_VSS.md
- [ ] Review and process: cisco\Cisco_VTP.md
- [ ] Review and process: cisco\Cisco_VXLAN.md
- [ ] Review and process: cisco\Cisco_WAN.md
- [ ] Review and process: cisco\Cisco_Wireless.md
- [ ] Review and process: cisco\Cisco_pyATS.md
- [ ] Review and process: cisco\Nexus_1000V.md
- [ ] Review and process: cisco\Nexus_FabricPath.md
- [ ] Review and process: cisco\Nexus_VDC.md
- [ ] Review and process: cisco\Nexus_vPC.md
- [ ] Review and process: cumulus\Cumulus_EVPN.md
- [ ] Review and process: cumulus\Cumulus_Linux.md
- [ ] Review and process: extreme\Extreme_VLAN.md
- [ ] Review and process: extreme\Extreme_XOS.md
- [ ] Review and process: f5\F5_Big-IP.md
- [ ] Review and process: gamla-General_disclaimer.md
- [ ] Review and process: gamla-mainpage.md
- [ ] Review and process: hardware\HPE_BL460c_G7.md
- [ ] Review and process: hardware\HPE_BL460c_Gen9.md
- [ ] Review and process: hardware\Lenovo_BIOS_update.md
- [ ] Review and process: index.md
- [ ] Review and process: juniper\Juniper_Aggregated_Ethernet.md
- [ ] Review and process: juniper\Juniper_JunOS.md
- [ ] Review and process: juniper\Juniper_VLAN.md
- [ ] Review and process: juniper\Juniper_VRRP.md
- [ ] Review and process: linux.md
- [ ] Review and process: linux_kickstart\Kickstart_Debian.md
- [ ] Review and process: linux_kickstart\Kickstart_Fedora.md
- [ ] Review and process: linux_kickstart\Kickstart_Ubuntu.md
- [ ] Review and process: linux_networking\BIRD.md
- [ ] Review and process: linux_networking\Bridge.md
- [ ] Review and process: linux_networking\ExaBGP.md
- [ ] Review and process: linux_networking\IPv6.md
- [ ] Review and process: linux_networking\Mininet.md
- [ ] Review and process: linux_networking\Netmiko.md
- [ ] Review and process: linux_networking\Netsim-tools.md
- [ ] Review and process: linux_networking\OpenDaylight.md
- [ ] Review and process: linux_networking\Open_vSwitch.md
- [ ] Review and process: linux_networking\Quagga.md
- [ ] Review and process: linux_networking\Suzieq.md
- [ ] Review and process: linux_networking\VPP.md
- [ ] Review and process: linux_networking\VyOS.md
- [ ] Review and process: linux_os\Debian.md
- [ ] Review and process: linux_os\Fedora.md
- [ ] Review and process: linux_os\Kali_Linux.md
- [ ] Review and process: linux_os\OS_X.md
- [ ] Review and process: linux_os\Security_Onion.md
- [ ] Review and process: linux_os\Ubuntu.md
- [ ] Review and process: linux_services\Ansible.md
- [ ] Review and process: linux_services\Apache.md
- [ ] Review and process: linux_services\AutoFS.md
- [ ] Review and process: linux_services\BIND.md
- [ ] Review and process: linux_services\Bcache.md
- [ ] Review and process: linux_services\Beeswarm.md
- [ ] Review and process: linux_services\Cacti.md
- [ ] Review and process: linux_services\Certbot.md
- [ ] Review and process: linux_services\Clogin.md
- [ ] Review and process: linux_services\Digitala_Certifikat.md
- [ ] Review and process: linux_services\Docker.md
- [ ] Review and process: linux_services\ELK.md
- [ ] Review and process: linux_services\EVE-NG.md
- [ ] Review and process: linux_services\Emby_Server.md
- [ ] Review and process: linux_services\Fabric.md
- [ ] Review and process: linux_services\Fail2Ban.md
- [ ] Review and process: linux_services\FastNetMon.md
- [ ] Review and process: linux_services\Flexget.md
- [ ] Review and process: linux_services\Foreman.md
- [ ] Review and process: linux_services\FreeIPA.md
- [ ] Review and process: linux_services\GNS3.md
- [ ] Review and process: linux_services\Gammu.md
- [ ] Review and process: linux_services\Git.md
- [ ] Review and process: linux_services\Gitlab.md
- [ ] Review and process: linux_services\GlusterFS.md
- [ ] Review and process: linux_services\Golang.md
- [ ] Review and process: linux_services\Google_Authenticator.md
- [ ] Review and process: linux_services\Grafana.md
- [ ] Review and process: linux_services\Graylog.md
- [ ] Review and process: linux_services\HashiCorp_Vault.md
- [ ] Review and process: linux_services\Hastebin.md
- [ ] Review and process: linux_services\IPXE.md
- [ ] Review and process: linux_services\IRedMail.md
- [ ] Review and process: linux_services\ISC_DHCP.md
- [ ] Review and process: linux_services\Icinga.md
- [ ] Review and process: linux_services\InspIRCd.md
- [ ] Review and process: linux_services\Jumpgate.md
- [ ] Review and process: linux_services\KVM.md
- [ ] Review and process: linux_services\Kea.md
- [ ] Review and process: linux_services\LAMP.md
- [ ] Review and process: linux_services\LUKS.md
- [ ] Review and process: linux_services\LXD.md
- [ ] Review and process: linux_services\Let's_Encrypt.md
- [ ] Review and process: linux_services\LibreNMS.md
- [ ] Review and process: linux_services\Logstash.md
- [ ] Review and process: linux_services\MEAN.md
- [ ] Review and process: linux_services\Mailserver.md
- [ ] Review and process: linux_services\MediaWiki.md
- [ ] Review and process: linux_services\ModSecurity.md
- [ ] Review and process: linux_services\Multiarch.md
- [ ] Review and process: linux_services\MySQL.md
- [ ] Review and process: linux_services\NFS.md
- [ ] Review and process: linux_services\NIPAP.md
- [ ] Review and process: linux_services\Netdisco.md
- [ ] Review and process: linux_services\Network.md
- [ ] Review and process: linux_services\Nginx.md
- [ ] Review and process: linux_services\Ntopng.md
- [ ] Review and process: linux_services\OSSEC.md
- [ ] Review and process: linux_services\Ookla_Speedtest_Mini.md
- [ ] Review and process: linux_services\OpenLDAP.md
- [ ] Review and process: linux_services\OpenShift.md
- [ ] Review and process: linux_services\OpenVPN.md
- [ ] Review and process: linux_services\Owncloud.md
- [ ] Review and process: linux_services\Oxidized.md
- [ ] Review and process: linux_services\PXE-Deploy.md
- [ ] Review and process: linux_services\Pagespeed.md
- [ ] Review and process: linux_services\PhpIPAM.md
- [ ] Review and process: linux_services\Pi-hole.md
- [ ] Review and process: linux_services\Piwik.md
- [ ] Review and process: linux_services\Pmacct.md
- [ ] Review and process: linux_services\PowerDNS.md
- [ ] Review and process: linux_services\Prometheus.md
- [ ] Review and process: linux_services\Puppet.md
- [ ] Review and process: linux_services\Python.md
- [ ] Review and process: linux_services\Quota.md
- [ ] Review and process: linux_services\Rancid.md
- [ ] Review and process: linux_services\Rar2fs.md
- [ ] Review and process: linux_services\RatticDB.md
- [ ] Review and process: linux_services\Realmd.md
- [ ] Review and process: linux_services\Roundcube.md
- [ ] Review and process: linux_services\Rsyslog.md
- [ ] Review and process: linux_services\SELinux.md
- [ ] Review and process: linux_services\SSH.md
- [ ] Review and process: linux_services\Shaltúre.md
- [ ] Review and process: linux_services\SmokePing.md
- [ ] Review and process: linux_services\Spacewalk.md
- [ ] Review and process: linux_services\Squid.md
- [ ] Review and process: linux_services\Sshttp.md
- [ ] Review and process: linux_services\Syntaxhighlight.md
- [ ] Review and process: linux_services\TFTP.md
- [ ] Review and process: linux_services\Tor.md
- [ ] Review and process: linux_services\Transmission.md
- [ ] Review and process: linux_services\Ulteo.md
- [ ] Review and process: linux_services\Vagrant.md
- [ ] Review and process: linux_services\Vsftpd.md
- [ ] Review and process: linux_services\Weechat.md
- [ ] Review and process: linux_services\Xming.md
- [ ] Review and process: linux_services\ZFS.md
- [ ] Review and process: linux_tools\Apt.md
- [ ] Review and process: linux_tools\Bash.md
- [ ] Review and process: linux_tools\Cron.md
- [ ] Review and process: linux_tools\DNF.md
- [ ] Review and process: linux_tools\Dd.md
- [ ] Review and process: linux_tools\Dialog.md
- [ ] Review and process: linux_tools\Dnstracer.md
- [ ] Review and process: linux_tools\Dumpcap.md
- [ ] Review and process: linux_tools\EFI.md
- [ ] Review and process: linux_tools\FirewallD.md
- [ ] Review and process: linux_tools\Frandom.md
- [ ] Review and process: linux_tools\Hdparm.md
- [ ] Review and process: linux_tools\IPMI.md
- [ ] Review and process: linux_tools\Iperf.md
- [ ] Review and process: linux_tools\Iproute2.md
- [ ] Review and process: linux_tools\Iptables.md
- [ ] Review and process: linux_tools\JQ.md
- [ ] Review and process: linux_tools\Keepalived.md
- [ ] Review and process: linux_tools\Mdadm.md
- [ ] Review and process: linux_tools\NTP.md
- [ ] Review and process: linux_tools\Nameif.md
- [ ] Review and process: linux_tools\Psql.md
- [ ] Review and process: linux_tools\Rsync.md
- [ ] Review and process: linux_tools\Scapy.md
- [ ] Review and process: linux_tools\System_storage_manager.md
- [ ] Review and process: linux_tools\Systemd.md
- [ ] Review and process: linux_tools\Tcpdump.md
- [ ] Review and process: linux_tools\Tmux.md
- [ ] Review and process: linux_tools\Tree.md
- [ ] Review and process: unifi\UniFi.md
- [ ] Review and process: vmware\Distributed_Switch.md
- [ ] Review and process: vmware\ESXi_Secure_Boot.md
- [ ] Review and process: vmware\ESXi_Security.md
- [ ] Review and process: vmware\ESXi_pktcap.md
- [ ] Review and process: vmware\Kickstart_ESXi.md
- [ ] Review and process: vmware\PSC.md
- [ ] Review and process: vmware\PowerCLI.md
- [ ] Review and process: vmware\Standard_vSwitch.md
- [ ] Review and process: vmware\VM_Encryption.md
- [ ] Review and process: vmware\VMware_ESXi.md
- [ ] Review and process: vmware\VMware_Vsphere_Client.md
- [ ] Review and process: vmware\VMware_vCenter.md
- [ ] Review and process: vmware\VSphere_Permissions.md
- [ ] Review and process: windows\Batch_script.md
- [ ] Review and process: windows\BitLocker.md
- [ ] Review and process: windows\Chocolatey.md
- [ ] Review and process: windows\InSSIDer.md
- [ ] Review and process: windows\Skärmsläckare.md
