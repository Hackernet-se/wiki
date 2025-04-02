---
title: Vsftpd
permalink: /Vsftpd/
---

[Category:Guider](/Category:Guider "wikilink") VSFTPD (Very secure FTP
daemon) Är en snabb och smidig FTP server för Unix system.

Installation
============

De flesta distar har vsftpd i sina standardrepos så vanligtvis är det
bara att köra en apt-get install vsftpd eller motsvarande med yum

Konfiguration
=============

I en Debianbaserad dist kommer du hitta konf filen i /etc/vsftpd.conf
Det finns 5 värden att titta på direkt

`anonymous_enable=(YES/NO) Om du vill tillåta anonyma inloggningar mot FTPN`
`local_enable=(YES/NO) Om lokala användare ska kunna använda FTP tjänsten`
`write_enable=(YES/NO) Om användarna ska kunna skriva data till FTPn eller inte`
`force_dot_files=(YES/NO) Om . filer ska visas i FTPn t.ex. .htaccess `
`hide_ids=(YES/NO) Om rättigheterna på filer ska synas på filerna. Om man tillåter anonyma inloggningar kan det vara en bra idé att köra på YES så de inte kan få ut information om vilka konton som finns på servern.`

Chroot
------

`chroot_local_user=(YES/NO) Om användarna ska vara låsta till sin hemfolder eller inte`
`chroot_list_enable=(YES/NO) Om du vill ange en lista av användare som ska vara tvärtemot vad du angav i chroot_local_user`

Om Chroot_list_enable=YES så får du skapa en lista i
/etc/vsftpd.chroot_list där du skriver in usernamn på användarena som
INTE ska följa chroot_local_user reglen.

Tillåtnade/nekade Användare
---------------------------

Om man har local_enable igång i konfen kan det vara en bra idé att inte
låta t.ex. root och servicekonton logga in på FTPn. Det kan vi lösa
genom att lägga till följande rader i konfen

`userlist_deny=YES`
`userlist_file=/etc/vsftpd.denied_users`

I userlist_file=/etc/vsftpd.denied_users skriver du sedan in
användarnamn som inte ska få logga in via ftpn t.ex. postfix och root.

SSL
---

Ganska straightforward conf här. Exemplet nedan är från en av Bats
servrar

`ssl_enable=YES`
`allow_anon_ssl=NO`
`force_local_data_ssl=YES`
`force_local_logins_ssl=YES`
`ssl_tlsv1=YES`
`ssl_sslv2=NO`
`ssl_sslv3=NO`

Virtuela Användare
------------------

Börja med att skapa en mapp för vsftpd om det inte finns i /etc/vftpd/
Skapa en fil med användare & Lösenord (nano users.txt) i stilen

`Användare1`
`Lösenord1`
`Användare2`
`Lösenord2 `
`etc`

Skapa sedan en databas med användarna db_load -T -t hash -f users.txt
vsftpd-virtual-user.db Glöm inte att sätta rättigheter och ta bort .txt
filen efteråt.

I /etc/vsftpd.conf så ska vi också göra några ändringar för att de
virtuela användarna ska funka

`virtual_use_local_privs=(YES/NO) Virtuella användare får samma rättigheter som vanliga användare annars får de anon rättigheter`
`pam_service_name=vsftpd.virtual Namnet på pam servicen vi vill använda`
`guest_enable=YES Tillåter virtuella användare`
`local_root=/home/vftp/$USER Vilken mapp de virtuela användarna ska ha access till`
`user_sub_token=$USER sätter deras användarnamn till chrooten`

Då ska vi bara fixa lite med PAM sen är vi good to go nano
/etc/pam.d/vsftpd.virtual

`#%PAM-1.0`
`auth       required     pam_userdb.so db=/etc/vsftpd/vsftpd-virtual-user`
`account    required     pam_userdb.so db=/etc/vsftpd/vsftpd-virtual-user`
`session    required     pam_loginuid.so`

Sen är det bara att skapa foldrarna för användarna i /home/vftp/
Foldrarna bör ägas av samma användare som tjänsten körs ifrån då
användarna använder tjänstens permissions.

LDAP
----

Kör med pam_ldap får skriva mer senare