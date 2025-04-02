---
title: Fabric
permalink: /Fabric/
---

Fabric är ett bibliotek och command-line verktyg för att automatisera
deployment och diverse tasks via ssh.

I grunden följer det med en bibliotek av funktioner för antingen lokal
eller remote kommandon samt uppladdning / nerladdning av filer. Man kan
även bygga egna moduler för att utöka funktionerna av fabric.

Installation
============

`sudo apt-get install fabric `

Eller med hjälp av Python PIP.

`pip install -e git+https://github.com/paramiko/paramiko/#egg=paramiko`
`pip install -e git+https://github.com/fabric/fabric/#egg=fabric`

Konfiguration
=============

Exempel: Fabric fil

``` python
from __future__ import with_statement
from fabric.api import *
from fabric.utils import warn
from fabric.contrib.files import exists
from fabric.contrib.project import  rsync_project
from fabric.contrib.files import sed
from fabric.contrib.files import append
from fabric.colors import *
import os.path
import server
server.setup_fabric()
env.user = 'root'
def upgrade_packages():
    run('apt-get update && apt-get -y upgrade')

def pkg_list_backp():
    package_list = './backups/packageLists/%s.packagesList' % env.host_string
    run('dpkg --get-selections > /var/backups/packages.list')
    get('/var/backups/packages.list', package_list)

def conf_sshd():
    sed('/etc/ssh/sshd_config',
        '#PasswordAuthentication yes',
        'PasswordAuthentication no' )
    sed('/etc/ssh/sshd_config',
        'PasswordAuthentication yes',
        'PasswordAuthentication no' )
    sed('/etc/ssh/sshd_config',
        'X11Forwarding yes',
        'X11Forwarding no' )
    sed('/etc/ssh/sshd_config',
        'AllowTcpForwarding yes',
        'AllowTcpForwarding no' )
    run('echo "AllowTcpForwarding no" >> /etc/ssh/sshd_config')
    run ('echo "AllowUsers root op"  >> /etc/ssh/sshd_config')
    run ('service ssh restart')

def deploy_gluster():
    put('./upload/glusterfs/gluster.list','/etc/apt/sources.list.d/') #Lägger den lokala filen gluster.list i remote foldern
    dist = run('lsb_release -cs')
    sed('/etc/apt/sources.list.d/gluster.list', 'precise', (dist) ) #ersätter "precise" med versionen som körs
    run("apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3FE869A9")
    run("apt-get update")
    run("apt-get install -y glusterfs-client")

def doitall():
    upgrade_packages()
    pkg_list_backp()
    conf_sshd()
    deploy_gluster()
```

Server Lista
============

För att göra olika tasks enklare och överskådligare rekommenderas det
att skapa serverdeffinitioner med olika roller och platser. Exempel
server.py

``` python
from fabric.api import env
class Server:
   def __init__(self, name, rack, roles):
        self.name = name
        self.rack = rack
        if isinstance(roles, list):
            self.roles = roles
        else:
            self.roles = list(roles)
servers = [
    Server('upload1',      'A1', ['sr04', 'ipmi', 'metal',  'bm', 'upload']),
    Server('upload2',       'A2', ['sr04', 'ipmi', 'esxi',  'drz', 'upload']),
    Server('csgo1',       'A2', ['sr04', 'ipmi', 'kvm',  'drz', 'csgo']),
    Server('voip1',         'A3', ['sr04', 'ipmi', 'metal',  'drz', 'voip']),
```

För att sedan använda listan importerar du den bara i ditt huvudfabric
skript med import server server.setup_fabric()

Kör bara Kör!
=============

Med serverlista och roller

    fab -R Roll task

Med enskilda hostar

    fab -H host1,host2 task

[Category:Guider](/Category:Guider "wikilink")