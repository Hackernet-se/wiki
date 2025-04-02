---
title: SSH
permalink: /SSH/
---

SSH kan användas för mer än bara SSHa till en server. Du kan använda det
för att tunnla trafik till saker du inte har direkt åtkomst mot och köra
program med hjälp av tex [Xming](/Xming "wikilink").

Fingerprint
-----------

Första gången man SSHar till en maskin kan man inte vara säker på
äktheten för att man inte har något fingerprint cacheat. Man kan
manuellt kolla fingerprint för att säkerställa att man inte blir mitmad.
Kolla först på servern, detta bör alltid göras med konsolen, för att
sedan jämföra det med vad din SSH-klient själv räknar ut utifrån nyckeln
den får.

`cd /etc/ssh`
`for file in *sa_key.pub`
`do   ssh-keygen -lf $file`
`done`

### SSHFP

SSHFP är ett resource record i DNS som man använder för att svara
klienter som väljer att fråga DNS om nycklarna klienten får är äkta.
Såhär kan det se ut i din zon.

`sshserver    IN      A       1.2.3.4`
`             IN      SSHFP   1 1 b4b8f2e051a16f57f69590c7c06aeaad019a3882`
`             IN      SSHFP   2 1 ea35c2064a5fb2ec9f51da2e7c790967f9844e59`

Reverse SSH Tunnel
------------------

Kan användas om en server sitter bakom en brandvägg som du inte kan SSHa
igenom.

Skriv detta på servern bakom brandväggen.

`ssh -fN -R 7000:localhost:22 username@ip`

Anslut sedan till servern över tunnel med kommandot.

`ssh -p 7000 username@localhost`

Tunnla trafik
-------------

För att tunnla trafik och tex kunna RDPa eller VNC en maskin bakom din
SSH host.

### RDP Trafik

`ssh -N -L 13389:RDPhost:3389 username@ip`

Starta sedan din RDP klient och anslut mot localhost:13389.

`rdesktop localhost:13389`

### HTTP trafik

`ssh -N -D 8080 username@ip`

Ändra sedan din webbläsares socks proxy till localhost port 8080.

`export HTTPS_PROXY=socks5://127.0.0.1:8080`

### Tunnel i en reverse tunnel

Man kan skapa tunnlar i en reverse ssh tunnel.

`ssh -p 7000 -N -L 13389:IPtillRDPhost:3389 username@ip`

Och anslut på samma sätt localhost:13389.

Autossh
-------

Om man vill att SSH-tunneln ska klara reboots och disconnects kan man
autostarta autossh. Detta förutsätter att man gör autentiseringen med
RSA-nycklar.

`sudo apt-get -y install autossh`
`sudo nano /etc/rc.local`
`autossh -M 10984 -N -f -o "PubkeyAuthentication=yes" -o "PasswordAuthentication=no" -i /home/$USER/.ssh/id_rsa -R 7000:localhost:22 username@ip -p 22 &`

SSH-Key
-------

Läs följande del hur man kan autentisera sig med RSA nykel utan att
behöva skriva lösenord, [SSH
Autentisering](/Jumpgate#SSH_Autentisering "wikilink").
[Category:Guider](/Category:Guider "wikilink")