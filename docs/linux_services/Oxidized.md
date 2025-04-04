---
title: Oxidized
permalink: /Oxidized/
---

[Oxidized](https://github.com/ytti/oxidized) är ett backup tool för
nätverk devices. Alltså en ersättare till [Rancid](/Rancid "wikilink").
Oxidized bygger också på perl men är lite mer modernare än Rancid.
Oxidized har ett eget webinterface med REST API stöd för att kunna söka,
diffa och visa config. Medans [Rancid](/Rancid "wikilink") enbart kan
använda en csv fil som source vad den ska backupa kan Oxidized även
använda samma sorts fil, en SQL databas eller en websida med JSON tex
[LibreNMS](/LibreNMS "wikilink") API.

Supportade OS
=============

-   A0 Networks
    -   ACOS
-   Alcatel-Lucent
    -   AOS
    -   AOS7
    -   ISAM
    -   TiMOS
    -   Wireless
-   Arista
    -   EOS
-   Arris
    -   C4CMTS
-   Aruba
    -   AOSW
-   Brocade
    -   FabricOS
    -   Ironware
    -   NOS (Network Operating System)
    -   Vyatta
-   Ciena
    -   SOAS
-   Cisco
    -   AireOS
    -   ASA
    -   IOS
    -   IOSXR
    -   NXOS
    -   SMB (Nikola series)
-   Citrix
    -   NetScaler (Virtual Applicance)
-   Cumulus
    -   Linux
-   DataCom
    -   DmSwitch 3000
-   DELL
    -   PowerConnect
    -   AOSW
-   Ericsson/Redback
    -   IPOS (former SEOS)
-   Extreme Networks
    -   XOS
    -   WM
-   F5
    -   TMOS
-   Force0
    -   DNOS
    -   FTOS
-   FortiGate
    -   FortiOS
-   HP
    -   Comware (HP A-series, H3C, 3Com)
    -   Procurve
-   Huawei
    -   VRP
-   Juniper
    -   JunOS
    -   ScreenOS (Netscreen)
-   Mikrotik
    -   RouterOS
-   Motorola
    -   RFS
-   MRV
    -   MasterOS
-   Netonix
    -   WISP Switch (As Netonix)
-   Opengear
    -   Opengear
-   Palo Alto
    -   PANOS
-   Supermicro
    -   Supermicro
-   Ubiquiti
    -   AirOS
    -   Edgeos
    -   EdgeSwitch
-   Zyxel
    -   ZyNOS

Installation
============

*requires Ruby version \>= 2.0*

-   <btn data-toggle="tab" class="">\#tab1\|CentOS 7</btn>
-   <btn data-toggle="tab" class="">\#tab2\|Ubuntu 16.04</btn>

<div class="tab-content">
<div id="tab1" class="tab-pane fade in active">

Skapa Oxidized användaren

`useradd -d /opt/oxidized oxidized`

Installera EPEL och SCL

`yum install epel-release centos-release-scl-rh centos-release-scl`

Installera Ruby samt extra paket för att kompilera Oxidized.

`yum install make cmake which sqlite-devel openssl-devel libssh2-devel gcc libicu-devel gcc-c++ rh-ruby26-ruby-devel rh-ruby26-ruby git`

Installera Oxidized

`scl enable rh-ruby26 bash`
`gem install oxidized`
`gem install oxidized-script oxidized-web`

Skapa en systemd fil åt Oxidized.

<div class="panel-group" id="accordion">

<accordion parent="accordion" heading="/etc/systemd/system/oxidized.service">

    #For debian 8 put it in /lib/systemd/system/
    #To set OXIDIZED_HOME instead of the default:
    # ~${oxidized_user}/.config/oxidized in debian 8, then uncomment
    #(and modify as required) the "Environment" variable below so
    #systemd sets the correct environment. Tested only on Debian 8.8.
    #YMMV otherwise.
    #
    #For RHEL / CentOS 7 put it in /etc/systemd/system/
    #and call it with systemctl start oxidized.service

    [Unit]
    Description=Oxidized - Network Device Configuration Backup Tool
    After=network-online.target multi-user.target
    Wants=network-online.target

    [Service]
    ExecStart=/bin/scl enable rh-ruby26 /opt/rh/rh-ruby26/root/usr/local/bin/oxidized
    User=oxidized
    KillSignal=SIGKILL
    Restart=always
    RestartSec=20
    #Environment="OXIDIZED_HOME=/etc/oxidized"

    [Install]
    WantedBy=multi-user.target

</accordion>

</div>
</div>
<div id="tab2" class="tab-pane fade">

`sudo add-apt-repository universe`
`sudo apt-get -y install ruby ruby-dev libsqlite3-dev libssl-dev pkg-config cmake libssh2-1-dev libicu-dev zlib1g-dev g++`
`sudo gem install oxidized`
`sudo gem install oxidized-script oxidized-web`

</div>
</div>

Konfiguration
=============

Konfigurationen är på YAML-format. Default-konf finns i:
**/etc/oxidized/config** och sedan används**\~/.config/oxidized/config**

För att initiera oxidized i ditt home directory kör:

`mkdir -p ~/.config/oxidized`
`oxidized`
`nano ~/.config/oxidized/config`

Man kan ändra var man vill att oxidized ska lägga sig genom att ändra
environment variable

`OXIDIZED_HOME=/etc/oxidized`

Logging

`log: "/home/$USER/.config/oxidized/oxidized.log"`

Input
-----

Input hämtar konfiguration från enheterna.

`input:`
`  default: ssh, telnet`
`  debug: false`
`  ssh:`
`    secure: false`

Source
------

Source läser vilka enheter som ska konfigbackas. Oxidized har stöd för
CSV, SQLite, MySQL och HTTP som source backends.

### CSV

CSV backend läser vilka enheter som det ska tas backup på från en
rancid-kompatibel fil.

``` yaml
 source:
   default: csv
   csv:
     file: "/home/$USER/.config/oxidized/router.db"
     delimiter: !ruby/regexp /:/
     map:
       name: 0
       model: 1
       username: 2
       password: 3
     vars_map:
       enable: 4
```

**router.db**
Format: 0:1:2:3:4

`router01.example.com:ios:user:pw:enablepw`
`172.20.0.1:ios:user:pw:enablepw`

### HTTP

HTTP backend behöver läsa en JSON hemsida.

``` yaml
source:
  default: http
  debug: false
  http:
    url: https://url
    scheme: https
    map:
      name: hostname
      model: os
```

Exempel på JSON formatet om Oxidized behöver.

``` json
]
  {
    "group": "default",
    "hostname": "switch1",
    "ip": "192.168.1.11",
    "os": "junos"
  },
  {
    "group": "default",
    "hostname": "switch2",
    "ip": "192.168.1.12",
    "os": "xos"
  }
]
```

Output
------

Output lagrar konfigurationen. Man måste köra git för att få
versionshantering på konfig-filerna.

`output:`
`  default: file`
`  file:`
`    directory: "/home/$USER/.config/oxidized/configs"`

GIT

`output:`
`  default: git`
`  git:`
`      user: Oxidized`
`      email: oxidized@example.com`
`      repo: "/home/$USER/.config/oxidized/oxidized.git"`

**Exceptions**
Man kan lägga in egna undantag för rader som ej borde vara med i
konfigen, t.ex. rader med tidsstämplar som ändras ofta.

Exempel IOS, edit
/var/lib/gems/2.3.0/gems/oxidized-0.21.0/lib/oxidized/model/ios.rb

``` php
  cmd 'show running-config' do |cfg|
    cfg = cfg.each_line.to_a[3..-1]
    cfg = cfg.reject { |line| line.match /^ntp clock-period / }.join
    cfg.gsub! /^Current configuration : [^\n]*\n/, ''
    cfg.gsub! /^! Last configuration change at [^\n]*\n/, ''
    cfg.gsub! /^! NVRAM config last updated at [^\n]*\n/, ''
    cfg.gsub! /^\ tunnel\ mpls\ traffic-eng\ bandwidth[^\n]*\n*(
                  (?:\ [^\n]*\n*)*
                  tunnel\ mpls\ traffic-eng\ auto-bw)/mx, '\1'
    cfg
  end
```

Hooks
-----

Hooks kan användas för att kalla på script, skicka mail eller pusha mot
git när något specifikt har hänt. Mer info om Hooks samt fler exempel
finns på deras
[hemsida](https://github.com/ytti/oxidized/blob/master/docs/Hooks.md)

### Events

-   `node_success:` triggas när en lyckad backup har tagits och precis
    före configen sparas i oxidized.
-   `node_fail:` triggas efter en node har failat.
-   `post_store:` triggas efter en node config har sparats. Körs endast
    om configen har ändrats.
-   `nodes_done:` triggas efter oxidized gått igenom alla nodes.

### Push to GIT

För att pusha till git måste man skapa en hook för det. Där man anger
vilket repo samt en ssh key.

``` yaml
hooks:
  push_to_remote:
    type: githubrepo
    events: [post_store]
    remote_repo: ssh://oxidized@github.com/hackernet-oxidized.git
    publickey: /opt/oxidized/.ssh/id_rsa.pub
    privatekey: /opt/oxidized/.ssh/id_rsa
```

### Maila om en node failar

Om en node skulle faila med backupen skicka då ett mail.

``` yaml
  email_output:
    type: exec
    events: [node_fail]
    cmd: '/opt/oxidized/.config/oxidized/extra/oxidized-report-git-commits | mail -s "Oxidized updates for ${OX_NODE_NAME}" hackernet@hackernet.se'
    async: true
    timeout: 120
```

Execute
-------

För att starta oxidized och ta en första backup

`oxidized`

RESTful web API

`rest: `<IP>`:8888`

Service
-------

Skapa en service med hjälp av [Systemd](/Systemd "wikilink"). Om du
installera Oxidized enligt denna guiden för CentOS använd isåfall
systemd filen som angetts där.

`sudo cat <<'__EOF__'>> /lib/systemd/system/oxidized.service`
`[Unit]`
`Description=Oxidized - Network Device Configuration Backup Tool`

`[Service]`
`ExecStart=/usr/local/bin/oxidized`
`User=oxidized`

`[Install]`
`WantedBy=multi-user.target`
`__EOF__`

`sudo systemctl enable oxidized`
`sudo systemctl start oxidized`
`sudo systemctl status oxidized`

[Category:Guider](/Category:Guider "wikilink")