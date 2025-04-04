---
title: SELinux
permalink: /SELinux/
---

Security-Enhanced Linux, SELinux är en säkerhetsmodul i linuxkärnan som
gör det möjligt att säkra upp både hård- och mjukvara. Kärnan i SELinux
är labels. Man sätter SELinux labels på allt ifrån filer till portar,
sedan applyar man policy på labels. Detta är en standardmodul sedan
kernel 2.6 och går t.ex. att konfigurera med
[Ansible](/Ansible "wikilink") eller [Puppet](/Puppet "wikilink").

Det är rekommenderat att alltid ha SELinux påslaget för att sedan
whitelista de avstängda funktioner du vill åt. För att modifiera SELinux
kan man använda sig av det enkla verktyget: semanage.

`# semanage (# yum install policycoreutils-python)`

Slå av och på SELinux manuellt

`setenforce 0/1`
`getenforce`

Byt SELinux-läge till nästa reboot (persistent)

`sudo sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config`

Status

`sestatus -v`

Show labels, exempelkommandon

`ls -lhZ`
`ps -eZ`
`ss -Z`
`semanage fcontext --list`

### Exempel på funktioner som är satta och avstängda av SELinux

**httpd_can_network_connect** - Ser till så att din httpd-tjänst inte
kan få tillgång till nät. Denna kan vara bra att ha igång om du tex har
en webbtjänst som hämtar information via tex http externt.
**ssh_port_t** - Denna är satt till 22. Om du vill köra ssh på annan
port måste du byta eller lägga till din nya port i SELinux.

Setroubleshoot
==============

Det finns ett paket som heter **setroubleshoot-server** som är till stor
hjälp om man valt att använda SElinux. Paketet gör att loggar från
SELinux hamnar i **/var/log/messages** och att dom blir väldigt enkla
att läsa. Paketet kan också hjälpa dig att lösa problemet med hjälp av
kommandot **sealert**

För att installera:

`yum -y install setroubleshoot-server`

Starta sedan om audit

`systemctl restart audit`

Loggar från SELinux ska nu hamna i **/var/log/messages**.

Om du redan har en fil med loggar du vill analysera kan du använda dig
av **sealert**.

`sealert -a /var/log/audit/audit.log > /var/log/audit/audit_human_readable.log`

#### Skapa egna selinux med grep och audit2allow.

Kommando

`cat /var/log/audit/audit.log |grep postgres_expo |grep denied |audit2allow`

Resultat som visar vad det är du skapar en regel på

`#============= init_t ==============`
`allow init_t postgresql_port_t:tcp_socket name_connect;`

Kommando

`cat /var/log/audit/audit.log |grep postgres_expo |grep denied |audit2allow -M postgres`

Resultat som bara visar vad du skall köra för att implementera selinux
regeln ovan

`******************** IMPORTANT ***********************`
`To make this policy package active, execute:`
`semodule -i postgres.pp`

kommando

`semodule -i postgres.pp`