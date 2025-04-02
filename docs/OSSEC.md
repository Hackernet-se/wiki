---
title: OSSEC
permalink: /OSSEC/
---

[Category:Guider](/Category:Guider "wikilink") OSSEC är ett host
intrusion detection system. OSSEC monitorerar aktivt dina filer, logar,
processer och letar efter rootkit's. OSSEC använder agenter för att
övervaka system, det går också att köra agentless och via remote syslog.

Supportade OS
=============

Agent
-----

-   GNU/Linux (all distributions, including RHEL, Ubuntu, Slackware,
    Debian, etc)
-   Windows XP, 2003, Vista, 2008, 2012
-   VMWare ESX 3.0,3.5 (including CIS checks)
-   FreeBSD (all current versions)
-   OpenBSD (all current versions)
-   NetBSD (all current versions)
-   Solaris 2.7, 2.8, 2.9 and 10
-   AIX 5.2 and 5.3
-   Mac OS X 10.x
-   HP-UX 11

Syslog
------

-   Cisco PIX, ASA and FWSM (all versions)
-   Cisco IOS routers (all versions)
-   Juniper Netscreen (all versions)
-   SonicWall firewall (all versions)
-   Checkpoint firewall (all versions)
-   Cisco IOS IDS/IPS module (all versions)
-   Sourcefire (Snort) IDS/IPS (all versions)
-   Dragon NIDS (all versions)
-   Checkpoint Smart Defense (all versions)
-   McAfee VirusScan Enterprise (v8 and v8.5)
-   Bluecoat proxy (all versions)
-   Cisco VPN concentrators (all versions)
-   VMWare ESXi 4.x

Agentless
---------

-   Cisco PIX, ASA and FWSM (all versions)
-   Cisco IOS routers (all versions)
-   Juniper Netscreen (all versions)
-   SonicWall firewall (all versions)
-   Checkpoint firewall (all versions)
-   All operating systems specified in the “operating systems” section

Installation
============

OSSEC är uppdelat i server/manager som sedan pratar med agenter som
installeras på varje host. Webuit får man installera separat om man vill
använda det.

Server/Manager & Agent
----------------------

### Debian/Ubuntu

Lägg till repo nyklarna.

`apt-key adv --fetch-keys `[`http://ossec.wazuh.com/repos/apt/conf/ossec-key.gpg.key`](http://ossec.wazuh.com/repos/apt/conf/ossec-key.gpg.key)

Följande Debian distar finns det stöd för
**jessie**,**wheezy**,**strectch** och **sid**.

`echo "deb `[`http://ossec.wazuh.com/repos/apt/debian`](http://ossec.wazuh.com/repos/apt/debian)` wheezy main" >> /etc/apt/sources.list`

Om du istället kör Ubuntu så finns det stöd för **xenial**, **precise**,
**trusty**, **vivid** eller **wily**.

`echo "deb `[`http://ossec.wazuh.com/repos/apt/ubuntu`](http://ossec.wazuh.com/repos/apt/ubuntu)` precise main" >> /etc/apt/sources.list`

Uppdatera repot.

`apt-get update`

För att installera **Server/Manager**.

`apt-get install ossec-hids`

Eller installera **agenten**.

`apt-get install ossec-hids-agent`

### RPM based

Lägg till yum repo.

`wget -q -O - `[`https://updates.atomicorp.com/installers/atomic`](https://updates.atomicorp.com/installers/atomic)` |sh`

Installera sedan servern/managern.

`yum install ossec-hids ossec-hids-server`

Eller agenten.

`yum install ossec-hids ossec-hids-client`

WEBui
-----

För att köra webui krävs:

-   Apache/Nginx med PHP (\>= 4.1 or \>= 5.0) installerat.
-   OSSEC (version \>= 0.9-3)

`git clone `[`https://github.com/ossec/ossec-wui.git`](https://github.com/ossec/ossec-wui.git)` /var/www/ossec`
`cd /var/www/ossec && ./setup.sh`

Om man har selinux på gör det att man inte kan nå visa ossec log filer.
För att fixa kan man lägga till en policy.

Skapa en TE fil: `/etc/seliinux/targeted/ossec-wui/ossec-wui.te` med
följande innehåll.

`module ossec-wui 1.0;`

`   require {`
`       type var_log_t;`
`       type httpd_t;`
`       type var_t;`
`       class file { read getattr open };`
`   }`

`   #============= httpd_t ==============`
`   allow httpd_t var_log_t:file read;`
`   allow httpd_t var_t:file { read getattr open };`

Kör sedan följande kommandon som root:

`checkmodule -M -m ossec-wui.te -o ossec-wui.mod`
`semodule_package -o ossec-wui.pp -m ossec-wui.mod`
`semodule -i ossec-wui.pp`

Försök nå ossec via <http://><host>/ossec

Konfiguration
=============

Agent
-----

Agent är att rekommendera på dom system det finns stöd för.

### Lägga till

Det finns 2 sätt att lägga till en agent i ossec.

-   **manage_agents**
    -   Manuellt men ett säkrare och mer kontrollerat sätt att lägga
        till agenter.
-   **ossec-authd**
    -   Smidigt för att det går snabbt att lägga till nya agenter.
        Osäkert för att alla som kan nå porten kommer att få en nykel
        och bli inlagd i OSSEC systemet. Går att blocka med hjälp av
        brandväggen.

#### manage_agents

Kör följande kommando på servern och välj **(A)dd an agent**.

`/var/ossec/bin/manage_agents`

När man ska fylla i ett IP kan du också skriva en IP range (10.0.0.0/24)
eller **any** ifall hosten byter IP ofta.

Välj sedan **(E)xtract key for an agent** och fyll sedan i ID numret du
valde i sista steget.

Kopiera nykeln och kör följande kommando på agenten.

`/var/ossec/bin/manage_agents`

Välj **(I)mport key from the server** och kopiera in nykeln. Starta
sedan OSSEC agenten.

#### ossec-authd

Kör följande på **servern**.

`/var/ossec/bin/ossec-authd -p 1515`

På **agenten** kör du.

`/var/ossec/bin/agent-auth -m `<ossec server ip>` -p 1515`

### Konfiguration

Det finns redan en default konfiguration som fungerar bra för agenter.
Om man vill ändra något som berör ossec globalt tex ändra vilken alert
nivå det måste vara för att skicka mail, lägga till nya regler så görs
det i `/var/ossec/etc/ossec.conf`.

Om man vill ändra i en regel tex höja o sänka alert nivån för en
speciell output, eller skriva en egen regel för en tjänst kollar man i
följande mapp: `/var/ossec/rules`

Agentless
---------

Agentless körs på system som inte har stöd för en agent men har stöd för
SSH. Tex brandväggar, switchar, routrar.

### Lägga till

Börja med att aktivera agentless stödet på ossec servern.

`/var/ossec/bin/ossec-control enable agentless`

För att lägga till en agentless host så behöver sätta SSH lösenord eller
använda SSH nykel. På Cisco saker (PIX, routers) behöver du ange en
extra parameter för **enable lösenordet**. Samma gäller om du vill lägga
till **su** stöd för linux.

`/var/ossec/agentless/register_host.sh add root@test.hackernet.se sshpass supass`
`/var/ossec/agentless/register_host.sh add pix@pix.fw.hackernet.se pixpass enablepass`

Om du vill använda SSH nykel så anger du **NOPASS** som lösenord. Skapa
sedan nycklar åt ossec.

`sudo -u ossec ssh-keygen`

Nykeln sparas i `/var/ossec/.ssh`, kopiera sedan över den publika nykeln
till dina enheter.

### Konfigurera

När man använder agentless finns det ingen default test som körs och
därför behöver man lägga till vad som ska övervakas manuellt per host i
`/var/ossec/etc/ossec.conf`.

Exempel övervakning som kollar ifall nån fils checksumma ändrats i
mapparna **/bin, /etc, /sbin** var 10h. Och en PIX övervakning som
kollar ifall configen ändrats varje timme.

<ossec_config>
`...`
<agentless>
`   `<type>`ssh_integrity_check_linux`</type>
`   `<frequency>`36000`</frequency>
`   `<host>`root@test.hackernet.se`</host>
`   `<state>`periodic`</state>
`   `<arguments>`/bin /etc/ /sbin`</arguments>
</agentless>

<agentless>
`   `<type>`ssh_pixconfig_diff`</type>
`   `<frequency>`3600`</frequency>
`   `<host>`pix@pix.fw.hackernet.se`</host>
`   `<state>`periodic_diff`</state>
</agentless>
`...`
</ossec_config>

**<type>**

Default finns det 6st olika types script att välja mellan.

-   **ssh_integrity_check_bsd**
    -   Kollar ifall nån fil ändrat SHA1 eller MDA5 checksum i BSD.
-   **ssh_integrity_check_linux**
    -   Kollar ifall nån fil ändrat SHA1 eller MDA5 checksum i Linux.
-   **ssh_pixconfig_diff**
    -   Kollar om configen ändrats på en Cisco PIX brandvägg. Behöver
        inget **arguments** i configen.
-   **ssh_asa-fwsmconfig_diff**
    -   Kollar om configen ändrats på en Cisco ASA brandvägg. Behöver
        inget **arguments** i configen.
-   **ssh_generic_diff**
    -   Används för att kolla vad som helst som har SSH stöd. Man
        skriver kommandona man vill jämföra i **arguments**.

**<frequency>**

Hur ofta en check ska köras. Skriv i sekunder.

**<host>**

Vilken host scriptet ska köras mot. Om man behöver köra su lösenordet så
skriver man **use_su**, ex:

<host>`use_su user@test.hackernet.se`</host>

**<state>**

Det finns 2 olika states.

-   **periodic**
    -   Skickar en kontrollerad output mot OSSEC agentless processen och
        jämför sedan mot tidigare körningar. Om det är någon skillnad så
        kommer OSSEC larma. Används för att kolla så inte checksumman
        ändrats.
-   **periodic_diff**
    -   Skickar output mot OSSEC agentless processen och jämför sedan
        mot tidigare körningar. periodic_diff används när det är en
        type som jämför 2 en fil/config mot varandra.

**<arguments>**

Fyll i dom kommandona du vill jämföra. För flera kommandon kan man
separera med ett **;**.

`...`
<arguments>`ls -la /etc; cat /etc/passwd`</arguments>
`...`

#### Prova manuellt

Man kan köra scripten manuellt för att prova att det fungerar. Krävs att
lösenordet/nykeln blivit inlagd.

`cd /var/ossec && ./agentless/ssh_integrity_check_linux root@test.hackernet.se /bin`