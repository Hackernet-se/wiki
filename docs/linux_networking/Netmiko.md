---
title: Netmiko
permalink: /Netmiko/
---

Netmiko är ett open-source [Python](/Python "wikilink") library som
används för att SSHa till nätverksenheter. Det är baserat på paramiko
och har stöd för flera olika plattformar från olika tillverkare. Målet
är att förenkla användandet av show och conf-kommandon mot
nätverksutrustning från script.

Exempel på device types som stöds

-   cisco_ios
-   cisco_xe
-   cisco_xr
-   cisco_asa
-   cisco_nxos
-   juniper
-   arista_eos
-   hp_procurve

Installation
============

`sudo pip install netmiko`

Getting started
===============

[Python](/Python "wikilink")

`from netmiko import ConnectHandler`

Connect

`R1 = {'device_type': 'cisco_xe', 'ip': '10.0.0.10', 'username': 'cisco', 'password': 'cisco', 'secret': 'cisco'}  `
`net_connect = ConnectHandler(**R1)`

Byt mellan olika prompts

`net_connect.find_prompt()`
`net_connect.enable()`
`net_connect.find_prompt()`
`net_connect.config_mode()`
`net_connect.find_prompt()`
`net_connect.disconnect()`

**Skicka kommandon**
Send command down the SSH channel, return output back

`net_connect.send_command(arguments)`

Send a set of configuration commands to remote device

`net_connect.send_config_set(arguments)`

Send a set of configuration commands loaded from a file

`net_connect.send_config_from_file(arguments)`

Exempel

`IPintbrief = net_connect.send_command("show ip int brief")`
`print IPintbrief`

**SSHDetect**
Netmiko kan även gissa vad det är för device type.

`from netmiko.ssh_autodetect import SSHDetect`
`remote_device = {'device_type': 'autodetect','host': '10.0.0.10','username': 'cisco','password': 'cisco'}`
`guesser = SSHDetect(**remote_device)`
`best_match = guesser.autodetect()`
`print(best_match)`

### Skapa VLAN

`from netmiko import ConnectHandler`
`import getpass`

`SW1 = {'device_type': 'cisco_ios', 'ip': '10.0.0.11', 'username': 'cisco', 'password': 'cisco', 'secret': 'cisco'}`
`SW2 = {'device_type': 'cisco_ios', 'ip': '10.0.0.12', 'username': 'cisco'}`

`pw = getpass.getpass("Enter password:")`
`SW02['password'] = pw`

`all_devices = [SW1, SW2]`

`config_commands = [ 'vlan 100', 'name NewVLAN', 'exit' ]`

`for a_device in all_devices:`
`    net_connect = ConnectHandler(**a_device)`
`    net_connect.enable()`
`    output = net_connect.send_config_set(config_commands)`
`    print output`
`    net_connect.disconnect()`

[Category:Network](/Category:Network "wikilink")