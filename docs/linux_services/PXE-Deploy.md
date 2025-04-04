---
title: PXE-Deploy
permalink: /PXE-Deploy/
---

[Category:Guider](/Category:Guider "wikilink") Preboot Execution
Environment är en miljö som används för att boota datorer med hjälp av
ett nätverkskort helt oberoende av lagringsenheter som hårddiskar eller
installerade operativsystem. När du säger åt din maskin att
PXE/Nätverksboota kommer den att skicka en DHCP-begäran som DHCP-servern
kommer att svara på och det kommer att innehålla två speciella saker, en
"next-server" och ett filnamn. "Next-server " är din TFTP-server och
filen är det din server kommer att ladda ner och köra ifrån. Denna fil
är vanligtvis en bootloader såsom pxelinux eller pxegrub. Se även
[IPXE](/IPXE "wikilink")

Valfri DHCP-server kan användas, det som ska pekas ut är tftp-servern.
T.ex.

`next-server 192.168.0.100; filename "pxelinux.0";`

Valfri tftp-server kan användas, den ska endast hålla filer.

Installation
------------

Här följer ett exempel på en pxelinux-setup (ej [TFTP](/TFTP "wikilink")
eller [DHCP](/ISC_DHCP "wikilink")). Först gäller det att få tag på de
nödvändiga filerna.

`apt-get -y install syslinux`

Konfiguration
-------------

`mkdir -p /tftpboot/pxelinux.cfg`
`cp /usr/lib/syslinux/pxelinux.0 /tftpboot`
`cp /usr/lib/syslinux/vesamenu.c32 /tftpboot/pxelinux.cfg`
`cp /usr/lib/syslinux/pxechain.com /tftpboot/pxelinux.cfg`

Sedan ska huvudkonf-filen skapas, här bestämmer man hur pxe:n ska se ut.

`cat<<'__EOF__'>/tftpboot/pxelinux.cfg/default`
`default vesamenu.c32`
`background pxelinux.cfg/badass.png`
`prompt 0`
`timeout 0`

`label First label`
`       kernel firstkernel`

`label Second label`
`       kernel secondkernel`
`__EOF__`

Det som står efter kernel och initrd är sökvägar som är relativa till
tftpboot

Unattended
----------

Vill man automatisera sina installationer kan man göra det med
kickstart-filer. T.ex.

`label InstallServer1404`
`       kernel server1404/linux`
`       append ks=`[`http://192.168.0.100/ks.cfg`](http://192.168.0.100/ks.cfg)` vga=normal initrd=server1404/initrd.gz ramdisk_size=16432 root=/dev/rd/0 rw  --`

### Skapa ks-fil

I många distar kan man köra följande: (in graphical environment)

`system-config-kickstart`

### Kickstartfiler

<categorytree mode=pages hideroot=on>Kickstart</categorytree>

Liveboot
--------

Det går även att liveboota med PXE, då kan man använda en NFS-share.
T.ex.

`LABEL Kali Live`
`KERNEL kali/live/vmlinuz`
`APPEND boot=live netboot=nfs nfsroot=192.168.0.100:/mnt/tftpboot/kali initrd=kali/live/initrd.img quiet splash --`

Flera PXE-servrar
-----------------

Vill man hoppa till en annan PXE-server, t.ex. en windows.

`LABEL Jump to other PXE`
`KERNEL pxelinux.cfg/pxechain.com`
`APPEND 192.168.0.10::pxelinux.0`

Exempel på användbara verktyg att ha på en PXE
----------------------------------------------

`LABEL Auto ^Nuke! DBAN No Questions Asked!`
`KERNEL DBAN/DBAN.BZI`
`APPEND nuke="dwipe --autonuke" silent`


`label MemTest`
`kernel memtest/mt86plus`


`label GParted Live`
`kernel gparted/vmlinuz`
`append initrd=gparted/initrd.img boot=live config noswap noprompt nosplash netboot=nfs nfsroot=192.168.0.100:/mnt/tftpboot/gparted`