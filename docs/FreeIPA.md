---
title: FreeIPA
permalink: /FreeIPA/
---

FreeIPA är ett open source projekt för centraliserad Identity, Policy
och Auditing (IPA) för unix/linux-system, likt Microsofts Active
Directory. I botten används 389 Directory Server för LDAP, MIT's
Kerberos 5 för authentication och single sign-on,
[BIND](/BIND "wikilink") för integrerad DNS och Samba för integration
mot Active Directory. Man sparar lösenord och SSH-nycklar centralt som
autentisering på övriga maskiner kan kolla mot. Man kan skapa
användargrupper och styra sudo policy centralt. Det är sponsrat av Red
Hat.

**DNS**
Namnuppslag måste fungera. T.ex. för en server måste man använda fqdn
och det ska vara resolvable. Det går att lösa med hosts-filen i en
testsetup.

Server
======

Installation
------------

**Fedora**

`sudo dnf -y install freeipa-server`

**CentOS**

`yum install ipa-server`

Konfiguration
-------------

Starta wizarden som automatiskt konfigurerar upp din FreeIPA med det
nödvändigaste.

`sudo ipa-server-install`

Kör kommandot **kinit admin** så får du en kerberos ticket som du
behöver för att kunna köra IPA tools tex ipa user-add.

### DNS records

Skapa följande records om du kör en DNS server som inte FreeIPA sköter.
Dessa records gör att autodiscovery fungerar och gör det mycket enklare
att konfigurera upp klienter.

`; ldap servers`
`_ldap._tcp              IN SRV 0 100 389        freeipa`

`;kerberos realm`
`_kerberos               IN TXT HACKERNET.SE`

`; kerberos servers`
`_kerberos._tcp          IN SRV 0 100 88         freeipa`
`_kerberos._udp          IN SRV 0 100 88         freeipa`
`_kerberos-master._tcp   IN SRV 0 100 88         freeipa`
`_kerberos-master._udp   IN SRV 0 100 88         freeipa`
`_kpasswd._tcp           IN SRV 0 100 464        freeipa`
`_kpasswd._udp           IN SRV 0 100 464        freeipa`

`;ntp server`
`_ntp._udp               IN SRV 0 100 123        freeipa`

`; CNAME for IPA CA replicas (used for CRL, OCSP)`
`ipa-ca                  IN A                    IP-to-FreeIPA`

### Brandväggsöppningar

Beroende på vilken dist du använder kanske du inte behöver öppna portar
i din egna brandvägg.

`firewall-cmd --permanent --add-service=ntp`
`firewall-cmd --permanent --add-service=http`
`firewall-cmd --permanent --add-service=https`
`firewall-cmd --permanent --add-service=ldap`
`firewall-cmd --permanent --add-service=ldaps`
`firewall-cmd --permanent --add-service=kerberos`
`firewall-cmd --permanent --add-service=kpasswd`
`firewall-cmd --reload`

### Skapa user

`ipa user-add`
`ipa passwd `<user>

### Web UI

Nås på <https://IP-to-FreeIPA>

### Replikering

Det går att replikera datan mellan servrar.

`ipa-replica-manage list`

### System account

Vissa LDAP tjänster behöver ett förkonfat konto tex LDAP Autofs och
sudo. Oftast så använder man en användares uppgifter när man bindar mot
en LDAP server men det är inte alltid möjligt. Anledningen till varför
man skapar ett service konto istället för ett vanligt användar konto är
att ett system kontot endast finns för att binda mot LDAP servern och är
alltså inget POSIX konto och kan därför inte logga in mot några system.

Skapa ett system account så här:

`ldapmodify -x -D 'cn=Directory Manager' -W`

`dn: uid=system,cn=sysaccounts,cn=etc,dc=hackernet,dc=se`
`changetype: add`
`objectclass: account`
`objectclass: simplesecurityobject`
`uid: 1337`
`userPassword: secret`
`passwordExpirationTime: 20380119031407Z`
`nsIdleTimeout: 0`
<blank line>
`^D(CTRL+D)`

### GroupOfUniqueNames

GroupOfUniqueNames är en objectclass som finns i grupper, vissa program
söker i LDAP databasen efter denna class. Bland annat [VMware
vCenter](/VMware_vCenter "wikilink").

Logga in på **IPA WebUI** gå till **IPA Server** ---\> **Configuration**
--\> **Group Options** --\> **Add** --\> Fyll i **GroupOfUniqueNames**
--\> **Save** --\> **Refresh**.

Skapa sedan en **Posix** grupp och lägg till användarna i gruppen.

Kör sedan följande kommando för varje användare.

`ipa group-mod `**<group_name>**` --addattr="uniqueMember=uid=`**`changeme`**`,cn=users,cn=accounts,dc=hackernet,dc=se"`

### Active directory trust

FreeIPA har stöd för att sätta upp en trust med ett AD.

Din FreeIPA domän och AD domän får inte vara samma för att det ska
fungera.

Installera AD trust paketet:

`yum install ipa-server-trust-ad`

Kör ipa ad trust install för att lägga till nödvändiga object och skapa
nya DNS records:

`ipa-adtrust-install --netbios-name=IPA_NETBIOS -a admin_password`

Ifall din freeipa inte kan uppdatera din DNS med nya records så behöver
du skapa följande annars kan du skippa detta steget:

`_ldap._tcp.dc._msdc.`<freeipa_domän>`. 3600 IN SRV 0 100 389 `<freeipa_server>
`_kerberos._tcp.dc._msdcs.`<freeipa_domän>`. 3600 IN SRV 0 100 88 `<freeipa_server>
`_kerberos._udp.dc._msdcs.`<freeipa_domän>`. 3600 IN SRV 0 100 88 `<freeipa_server>
`_ldap._tcp.Default-First-Site-Name._sites.dc._msdcs.`<freeipa_domän>`. 3600 IN SRV 0 100 389 `<freeipa_server>
`_kerberos._tcp.Default-First-Site-Name._sites.dc._msdcs.`<freeipa_domän>`. 3600 IN SRV 0 100 88 `<freeipa_server>
`_kerberos._udp.Default-First-Site-Name._sites.dc._msdcs.`<freeipa_domän>`. 3600 IN SRV 0 100 88 `<freeipa_server>

För att en trust ska fungera så måste AD servern kunna slå upp FreeIPA
domänen och tvärtom. Verifiera det med följande kommando.

**AD DC**

`C:\> nslookup`
`set type=srv`
`_ldap._tcp.ad_domain`
`_ldap._tcp.ipa_domain`

**IPA server**

`dig SRV _ldap._tcp.ipa_domain`
`dig SRV _ldap._tcp.ad_domain`

Om det inte fungerar så kan man behöva forwarda request direkt till
motsvarande domäns dns server.

**AD DC**

`C:\> dnscmd 127.0.0.1 /ZoneAdd ipa_domain /Forwarder ipa_ip_address`

**IPA server**

-   IPA v3.x:

`ipa dnszone-add ad_domain --name-server=ad_hostname.ad_domain --admin-email='hostmaster@ad_domain' --force --forwarder=ad_ip_address --forward-policy=only --ip-address=ad_ip_address`

-   IPA v4.x:

`ipa dnsforwardzone-add ad_domain --forwarder=ad_ip_address --forward-policy=only`

#### Skapa och verifiera cross-realm trust

`ipa trust-add --type=ad ad_domain --admin Administrator --password`

Vid prompt ange lösenordet till AD domänens Administrator konto eller
ett annat konto som är med i **Domain Admins** gruppen, om allt är
uppsatt korekt så kommer IPA att sätta upp en two-way forest trust med
AD och validera den.

Skapa sedan en external group och en POSIX group.

-   External group funkar som en container där dina trusted domän
    användare finns.
-   Lägg sedan till den den externa gruppen i en POSIX group så att dina
    AD domän användare får ett group id(gid) som kan användas som
    default group.

`ipa group-add --desc='ad_domain admins external map' ad_admins_external --external`
`ipa group-add --desc='ad_domain admins' ad_admins`
`ipa group-add-member ad_admins_external --external 'ad_netbios\Domain Admins'`

När den frågar om **member user** och **member group** så lämna det
blankt och tryck enter.

Lägg sedan till den externa gruppen i posix gruppen.

`ipa group-add-member ad_admins --groups ad_admins_external`

För att verifera att det fungerar så ska det gå att logga in på en IPA
ansluten server med ett AD konto. När du ansluter till en server måste
du ange **ad_user@ad_domain** som username.

### Let's Encrypt webui SSL

För att kunna använda Let's Encrypts certifikat med FreeIPA behöver man
importera deras root certifikat.

Börja med att clona följande repo.

`git clone `[`https://github.com/Hackernet-se/freeipa-letsencrypt`](https://github.com/Hackernet-se/freeipa-letsencrypt)` && cd freeipa-letsencrypt`

Importera root certen.

`ipa-cacert-manage install "DSTRootCAX3.pem" -n DSTRootCAX3 -t C,,`
`ipa-cacert-manage install "LetsEncryptAuthorityX3.pem" -n letsencryptx3 -t C,,`

Uppdatera sedan databasen.

`ipa-certupdate`

När dom två certifikaten är inlagda så kan man importera certifikaten
man fått från Let's Encrypt.

`ipa-server-certinstall -w fullchain.pem privkey.pem`

Starta sedan om http tjänsten och dirsrv.

`systemctl restart dirsrv@REALM.service`
`systemctl restart httpd.service`

Klient
======

Installation
------------

Varje klient måste ha ett fully qualified domain name. Default kerberos
domain är din domän, t.ex. hackernet.se.

**Ubuntu**

`apt-get install freeipa-client`

**Fedora**

`dnf install freeipa-client`

Enroll host till FreeIPA
------------------------

Kör följande kommando för att starta en wizard som enrollar din klient i
freeipa.

`sudo ipa-client-install`

Om autodiscovery fungerar som det ska så är alla fält i fyllda och det
enda du behöver ange är en användare som har behörighet att enrolla
klinter till freeipa.

Man kan fylla i användarnamn och lösenord i förväg så slipper svara på
frågor.

`sudo ipa-client-install -p admin -w secretpw --unattended --mkhomedir`

IPA Advise
----------

Med kommandot `ipa-advise` på servern kan du få konfigurations förslag
på hur du konfigurerar en klient mot freeipa om du inte har tillgång
till ipa klienten. [Category:Guider](/Category:Guider "wikilink")