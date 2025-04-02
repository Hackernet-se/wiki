---
title: VMware ESXi
permalink: /VMware_ESXi/
---

ESXi är en type 1 hypervisor utvecklad och såld av VMware.

Förberedelser
-------------

VMware uppdaterar ESXi med jämna mellanrum, var 1-3 månad, och din iso
blir snabbt utdaterad. Det smidigaste sättet att tanka hem den senaste
iso:n är med ett powershell-script. Inget VMware-konto behövs heller!

[<http://vibsdepot.v-front.de/tools/ESXi-Customizer-PS-v2.5.ps1>](http://vibsdepot.v-front.de/tools/ESXi-Customizer-PS-v2.5.ps1)

OBS Requirements: VMware PowerCLI version 5.1 or newer

`.\ESXi-Customizer-PS-v2.5.ps1 -v65`

Planerar du att köra ESXi på ett konsumentmoderkort är det inte säkert
att nätverkskortet fungerar med standard-iso:n. Vill du ha en iso med
mer drivrutiner kör istället följande kommando:

`.\ESXi-Customizer-PS-v2.5.ps1 -v60 -vft -load net-e1000e,net55-r8168,net-r8169,sata-xahci`

Patchhantering
--------------

Detta är generell patchhantering.

**Online**

Börja med att kolla vad senaste imagen heter på [patch
tracker](https://esxi-patches.v-front.de/)

`esxcli network firewall ruleset set -e true -r httpClient`
`esxcli software profile update -d `[`https://hostupdate.vmware.com/software/VUM/PRODUCTION/main/vmw-depot-index.xml`](https://hostupdate.vmware.com/software/VUM/PRODUCTION/main/vmw-depot-index.xml)` -p ESXi-5.X.X-2015XXXXXXX-standard [--allow-downgrades]`
`reboot`

**Offline**

Ladda ner zip från VMwares hemsida och lägg in på datastore

`esxcli software profile update -d /vmfs/volume/your_datastore/ESXi550-2015XXX.zip -p ESXi-5.5.0-2015XXX-standard `
`reboot`

Detta fungerar även mellan versioner, 5.1 -\> 5.5 -\> 6.0

**vCenter**

Har man vCenter bör man använda VMware Update Manager.

`.\ESXi-Customizer-PS-v2.5.ps1 -v55 -ozip`

Output an ESXi Offline Bundle that you can use for importing into Update
Manager

Logghantering
-------------

Loggar berättar mycket om din miljö, samla dem. Det finns olika
varianter för central ESXi-logghantering.

-   vCenter builtin syslog service
-   VMware vRealize Log Insight
-   <http://www.sexilog.fr/>

Peka loggarna i ESXi: Advanced Settings -\> Syslog.global.logHost -\>
<udp://%5BIP%5D:514>

Verify

`esxcli system syslog config get`

Embedded Host Client
--------------------

Webgui till enskilda ESXi-hostar, likt vCenters. Detta är standard sedan
ESXi 6.0u2.

[`https://[ESXI-HOST]/ui`](https://%5BESXI-HOST%5D/ui)

SSH
---

Varningsmeddelande kan stängas av med:

`esxcli system settings advanced set -o /UserVars/SuppressShellWarning -i 1`

Nyckelautentisering
OBS med -O skriver man över existerande nycklar

`wget `[`http://website/id_dsa.pub`](http://website/id_dsa.pub)` -O /etc/ssh/keys-root/authorized_keys`

DCUI
Skriv följande för att starta Direct Console direkt från din
SSH-session:

`dcui`

SNMP
----

För att slå på SNMP och sätta communitys kan man göra det via CLI.

`esxcli system snmp set --communities `**`community`**

Enable SNMP Service:

`esxcli system snmp set --enable true`

Öppna upp i den interna brandväggen:

`esxcli network firewall ruleset set --ruleset-id snmp --allowed-all true`
`esxcli network firewall ruleset set --ruleset-id snmp --enabled true`

Om du vill öppna upp i brandväggen på ett säkert sätt och endast tillåta
IP's ifrån 10.0.0.0/24:

`esxcli network firewall ruleset set --ruleset-id snmp --allowed-all false`
`esxcli network firewall ruleset allowedip add --ruleset-id snmp --ip-address 10.0.0.0/24`
`esxcli network firewall ruleset set --ruleset-id snmp --enabled true`

Starta sedan om SNMP tjänsten:

`/etc/init.d/snmpd restart`

VIB
---

VIB paket kan vara drivrutiner, third party software eller
uppdateringar.

**Installera**

`esxcli software vib install -d “/vmfs/volumes/Datastore/DirectoryName/PatchName.zip“`

**Updatera**

`esxcli software vib update -d “/vmfs/volumes/Datastore/DirectoryName/PatchName.zip”`

**Lista installerade VIB's**

`esxcli software vib list`

Network
-------

Undrar du vilket nätverkskort t.ex. vmnic2 är fysiskt kan du köra
följande kommando om du loggar in med SSH på hosten. Porten börjar
blinka i 60 sekunder förutsatt att det inte sitter någon kabel i.

`ethtool -p vmnic2 60`

Lista NetStack-instanser (VRF)

`esxcfg-vmknic -l`
`esxcli network ip interface list `
`ping -S `<netstackname>` 10.0.0.10`

**CDP**
Slå på CDP på en vSwitch

`esxcli network vswitch standard set --cdp-status both|listen --vswitch-name vSwitch1`

**Iperf**
Fr.o.m. ESXi 6.0 finns iperf inbyggt. Se även
[Iperf](/Iperf "wikilink").

Server

`cp /usr/lib/vmware/vsan/bin/iperf /usr/lib/vmware/vsan/bin/iperf.copy`
`/usr/lib/vmware/vsan/bin/iperf.copy -s`

Klient

`/usr/lib/vmware/vsan/bin/iperf -c `<server-ip>

**PXE**
Använd Ventoy.

Tips n Tricks
-------------

### NTP

NTP via SSH

`cat > /etc/ntp.conf << __EOF__`
`restrict default kod nomodify notrap noquery nopeer`
`restrict 127.0.0.1`
`driftfile /etc/ntp.drift`
`server 0.se.pool.ntp.org`
`__EOF__`
`/sbin/chkconfig ntpd on`

### Nested Hypervisor

För att kunna köra en nested hypervisor (t.ex. Hyper-V, ESXi) på din
ESXi-host måste det finns EPT/RVI-stöd i CPUn. Ett enkelt sätt att kolla
det på din ESXi-host:

`vim-cmd hostsvc/advopt/update Config.HostAgent.plugins.solo.enableMob bool true`
[`https://[esxi-ip-address]/mob/?moid=ha-host&doPath=capability`](https://%5Besxi-ip-address%5D/mob/?moid=ha-host&doPath=capability)

logga in och kolla raden: nestedHVSupported

Sedan måste hosten VHV enableas.

`grep -i "vhv.enable" /etc/vmware/config || echo "vhv.enable = \"TRUE\"" >> /etc/vmware/config`
`reboot`

### Initializing ACPI

Om uppstarten fastnar på detta steg, dubbelkolla att det inte bootar med
UEFI och i så fall ta bort UEFI från boot-menyn.

### Rollback

För att backa en ESXi-uppgradering kan man göra en rollback. Starta om
hosten, under boot när progressbaren kommer tryck: Shift+R
*OBS bootbanken skrivs över var 60:e minut så man har en timme på sig*

`Current hypervisor will permanently be replaced`
`with build: X.X.X-XXXXXX. Are you sure? [Y/n]`
`Shift+Y`
`Enter to boot`

### Lista maskiner

Lista virtuella maskiner som är på

`/usr/sbin/localcli vm process list`

### Lämna tillbaka oanvända blocks

Om du har ett san, där du kör med tjocka diskar mot så kommer du behöva
lämna tillbaka blocks ibland. för att enkelt göra detta kan du köra
kommandot:

`for i in $(ls /vmfs/volumes/ | grep datastorename) ; do echo "Reclaiming on: " $i ; time esxcli storage vmfs unmap -l $i ; done `

Byt ut datastorename mot namnstandarden på dina datastores. tex ssd_ds
om dina datastores heter ssd_ds001-8

Detta behövs göra om du kör vmfs 5 och tjocka diskar. Har du 512kb
blocksize och vmfs 6 så sköts det automagiskt på DELL compellant

### G5-G7 HP ProLiant

Ladda ner från:
<http://www8.hp.com/us/en/products/servers/solutions.html?compURI=1499005#tab=TAB4>

`.\ESXi-Customizer-PS-v2.4.ps1 -v55 -izip .\VMware-ESXi-5.5.0-Update2-2403361-HP-550.9.2.27-Mar2015-depot.zip -update -remove hp-ams`

### LSI RAID

Vill du monitorera ditt raidkort i vsphereklienten gör följande:
Ladda upp följande fil till datastore

[`http://ds.karen.hj.se/~cameljoe/resources/VMW-ESX-5.5.0-lsiprovider-500.04.V0.55-0006-offline_bundle-2626932.zip`](http://ds.karen.hj.se/~cameljoe/resources/VMW-ESX-5.5.0-lsiprovider-500.04.V0.55-0006-offline_bundle-2626932.zip)

`esxcli software vib install -d /vmfs/volumes/[DATASTORE]/VMW-ESX-5.5.0-lsiprovider-500.04.V0.55-0006-offline_bundle-2626932.zip`
`reboot`

[Category:VMware](/Category:VMware "wikilink")
[Category:Guider](/Category:Guider "wikilink")