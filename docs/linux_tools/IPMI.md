---
title: IPMI
permalink: /IPMI/
---

. Antingen
kan man kompilera det själv eller ladda ner färdig binär. Logga in på
server med SSH:

`wget `[`http://harsbo.se/filer/ipmitool`](http://harsbo.se/filer/ipmitool)
```
chmod +x ipmitool
```

För att lista kommandoalternativ kör kommandot utan parametrar.

Skapa användare

```
./ipmitool user set name 2 admin
```
`./ipmitool user set password 2 `<some passwd>
```
./ipmitool user priv 2 4 1
./ipmitool channel setaccess 1 2 callin=on ipmi=on link=on privilege=4
./ipmitool user list 
./ipmitool user enable 2
```

IPconfig

```
./ipmitool lan set 1 ipsrc static
./ipmitool lan set 1 ipaddr 10.0.0.45
./ipmitool lan set 1 defgw ipaddr 10.0.0.1
./ipmitool lan set 1 netmask 255.255.255.0
./ipmitool lan set 1 vlan id 5
./ipmitool lan print
```