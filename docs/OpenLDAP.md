---
title: OpenLDAP
permalink: /OpenLDAP/
---

[Category:Guider](/Category:Guider "wikilink")
[Category:Sparco](/Category:Sparco "wikilink") OpenLDAP är en central
inloggnings server precis som Active directory är. Det ökar
användarvänligheten om man kan använda samma lösenord till flera
platser. OBS det är viktigt att klockorna är synkade på maskinerna som
ska använda LDAP och att namnuppslag för LDAP-servern kan göras på alla
klienter.

Installera
----------

`apt-get update && apt-get install slapd ldap-utils`

Slå in ett lösenord.

Kör sedan,

`dpkg-reconfigure slapd`

Svara följande på frågorna som kommer.

|                                       |            |                                                                                    |
|---------------------------------------|------------|------------------------------------------------------------------------------------|
| Omit OpenLDAP server configuration?   | No         | Detta kommer starta wizarden.                                                      |
| DNS domain name:                      | example.se | Namnet på din LDAP domän. (Detta namnet kommer skapa ditt BaseDN dc=example,dc=se) |
| Organization name:                    | example    | Ett namn på din organisation                                                       |
| Administrator password:               | secret     | Nytt lösenord för din LDAP administratör. (cn=admin,dc=example,dc=se)              |
| Database backend to use:              | HDB        | Bygger på Oracle Berkeley databas(BDB) men är mer effektiv.                        |
| Remove database when slapd is purged? | No         | Spara databasen även om OpenLDAP avinstalleras.                                    |
| Move old database?                    | Yes        | Ta bort den gammla databasen så att den inte stör den nya.                         |
| Allow LDAPv2 protocol?                | No         | Om du inte måste ha LDAPv2 men det är rekommenderat att ha det avstängt.           |

Gör en test query och kolla att LDAP servern fungerar.

`ldapsearch -x -W -D cn=admin,dc=example,dc=se -b dc=example,dc=se -LLL `

`# x = simple bind/authentication`
`# W = ask for password`
`# D = user DN`
`# b = search base`
`# LLL = omit comments`

Konfigurera
-----------

Det finns tre olika sätt att konfigurera OpenLDAP.

-   Man ändrar i själv i mappen `/etc/ldap/slapd.d`. Detta är inte
    rekommenderat att göra.
-   Man använder ldap-utils(ldapadd, ldapdelete, ldapmodify, etc).
-   Eller så använder man ett GUI för att skapa användare, grupper eller
    importera LDIF.
    [phpLDAPadmin](http://phpldapadmin.sourceforge.net/wiki/index.php/Main_Page),
    [Apache Directory
    Studio](https://directory.apache.org/studio/download/download-linux.html),
    [LDAP Admin](http://www.ldapadmin.org).

**LDIF** är text filer som används för att skapa användare, grupper
eller för att göra ändringar på din LDAP server. För att importera en
LDIF fil kör kommandot,

`ldapadd -W -D "cn=admin,dc=example,dc=se" -f filename.ldif`

### Skapa en organizational unit

Skapa en ldif fil med följande info i och importera till OpenLDAP.

`dn: ou=users,dc=example,dc=se`
`changetype: add`
`objectClass: organizationalUnit`
`objectClass: top`
`ou: users`

### Skapa en användare

`dn: uid=user1,ou=users,dc=example,dc=se`
`objectClass: inetOrgPerson`
`objectClass: posixAccount`
`objectClass: top`
`cn: user1`
`givenName: User`
`sn: Usersson`
`homeDirectory: /home/user1`
`loginshell: /bin/bash`
`uidNumber: 51397`
`gidNumber: 0`
`uid: user1`
`userPassword: secret`

Om du vill kryptera lösenordet skriv

`slappasswd -s secret`

Och kopiera in SSHA nykeln i ldif filen efter `userPassword:`

### Skapa grupper

Den finns olika sorters grupper man kan skapa.

-   posixGroup - Lik en vanlig Unix grupp och har ett gidNumber.
-   groupOfNames - Används default av
    [memberOf](/OpenLDAP#memberOf "wikilink") overlayen och sparar varje
    användares FDN.
-   groupOfUniqueNames - Samma som groupOfNames fast man kan skilja på
    användare som har samma uid genom att lägga till en extra unique
    identifier.

#### posixGroup

Denna sortens grupp syns om du har LDAP kopplat dina användare på en
Linux maskin.

`dn: cn=sudo,dc=hackernet,dc=se`
`objectclass: posixGroup`
`objectclass: top`
`cn: sudo`
`description: Group description`
`memberUid: user1`

#### groupOfNames

`dn: cn=groupname,dc=hackernet,dc=se`
`objectclass: groupofnames`
`cn: groupname`
`description: Group desc`
`member: uid=user1,ou=users,dc=example,dc=se`

#### groupOfUniqueNames

Om du har LDAP kopplat din [vCenter](/VMware_vCenter "wikilink") så
behöver användarna ligga i en sån här grupp.

`dn: cn=vcenter,dc=example,dc=se`
`objectclass: groupOfUniqueNames`
`objectclass: top`
`cn: vcenter`
`description: vcenter group`
`uniqueMember: cn=user1,ou=users,dc=example,dc=se`

### memberOf

För enkelt göra ställa frågor och se vilken grupp en användare är med i
så behöver man aktivera `memberOf`.

Skapa tre filer med följande kod i. **memberof.ldif**

`dn: cn=module,cn=config`
`cn: module`
`objectClass: olcModuleList`
`olcModuleLoad: memberof`
`olcModulePath: /usr/lib/ldap`

`dn: olcOverlay={0}memberof,olcDatabase={1}hdb,cn=config`
`objectClass: olcConfig`
`objectClass: olcMemberOf`
`objectClass: olcOverlayConfig`
`objectClass: top`
`olcOverlay: memberof`
`olcMemberOfDangling: ignore`
`olcMemberOfRefInt: TRUE`
`olcMemberOfGroupOC: groupOfNames`
`olcMemberOfMemberAD: member`
`olcMemberOfMemberOfAD: memberOf`

**refint1.ldif**

`dn: cn=module{1},cn=config`
`add: olcmoduleload`
`olcmoduleload: refint`

**refint2**

`dn: olcOverlay={1}refint,olcDatabase={1}hdb,cn=config`
`objectClass: olcConfig`
`objectClass: olcOverlayConfig`
`objectClass: olcRefintConfig`
`objectClass: top`
`olcOverlay: {1}refint`
`olcRefintAttribute: memberof member manager owner`

Ladda sedan in filerna i OpenLDAP servern med följande kommandon.

`ldapadd -Q -Y EXTERNAL -H ldapi:/// -f memberof.ldif`
`ldapmodify -Q -Y EXTERNAL -H ldapi:/// -f refint1.ldif`
`ldapadd -Q -Y EXTERNAL -H ldapi:/// -f refint2.ldif`

Skapa sedan en grupp och lägg till användare.

**add_group.ldif**

`dn: cn=testgrupp,dc=example,dc=se`
`objectClass: groupofnames`
`cn: testgrupp`
`description: All users`
`member: uid=testuser,ou=users,dc=example,dc=se`

`ldapadd -x -D cn=admin,dc=example,dc=se -W -f add_group.ldif`

För att testa att det funkar kan du ställa denna frågan.

`ldapsearch -h `<ip>` -x -b "dc=example,dc=se" '(uid=testuser)' memberOf`

### RootDN

För att göra ändringar i `cn=config` som innehåller själva LDAP
konfigurationen behöver man skapa ett admin konto med lösenord.

Under cn=config kan man sätta bland annat ACLer för vilka användare som
får läsa och skriva så man inte behöver använda cn=admin kontot varje
gång.

`dn: olcDatabase={0}config,cn=config`
`changetype: modify`
`add: olcRootDN`
`olcRootDN: cn=admin,cn=config`

`dn: olcDatabase={0}config,cn=config`
`changetype: modify`
`add: olcRootPW`
`olcRootPW: secret`

`ldapadd -Y EXTERNAL -H ldapi:/// -f rootconfig.ldif`

För att nå cn=config med Apache Directory Studio.

<File:openldap_04.png> <File:openldap_05.png> <File:openldap_06.png>

### Postfix Schema

För att styra en mailserver med LDAP behövs postfix schemat för att få
fler object klasser.

`cd /etc/ldap/schema`
`wget `[`http://www.postfix-buch.com/download/postfix-book.schema.gz`](http://www.postfix-buch.com/download/postfix-book.schema.gz)` && gunzip postfix-book.schema.gz`
`mkdir ldif_output`

``` bash
cat <<'__EOF__'>>schema_convert.conf
include /etc/ldap/schema/core.schema
include /etc/ldap/schema/cosine.schema
include /etc/ldap/schema/nis.schema
include /etc/ldap/schema/inetorgperson.schema
include /etc/ldap/schema/postfix-book.schema
__EOF__
```

`slapcat -f schema_convert.conf -F ./ldif_output/ -n0`
`cp /etc/ldap/schema/ldif_output/cn\=config/cn\=schema/cn\=\{4\}postfix-book.ldif /etc/ldap/schema/postfix-book.ldif`

Öppna och ändra följande i `postfix-book.ldif`

-   dn: cn=postfix-book,cn=schema,cn=config
-   cn: postfix-book
-   Ta bort allt från structuralObjectClass och neråt.

Importera ldif filen och starta om slapd.

`ldapadd -Y EXTERNAL -H ldapi:/// -f postfix-book.ldif`

<div class="toccolours mw-collapsible mw-collapsed" style="width:800px">

Exempel LDIF på hur en mail användare kan se ut.

<div class="mw-collapsible-content">

``` bash
#!/bin/bash
dn: uid=user,ou=users,dc=hackernet,dc=se
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: person
objectClass: top
objectClass: PostfixBookMailAccount
objectClass: extensibleObject
cn: user
givenName: User
sn: Usersson
mail: user@hackernet.se
homeDirectory: /home/user
loginShell: /bin/bash
uidNumber: 51397
gidNumber: 0
mailEnabled: TRUE
mailGidNumber: 5000
mailUidNumber: 5000
mailHomeDirectory: /srv/vmail/user@hackernet.se
mailQuota: 10240
mailStorageDirectory: maildir:/srv/vmail/user@hackernet.se/Maildir
uid: user
userPassword: secret
```

</div>
</div>

Client
------

### Nslcd

Enklaste sättet att autha mot en LDAP server är att använda nslcd.

`apt-get install nslcd`

Lägg sedan till följande i `/etc/nslcd.conf`

`...`
`uri ldapserver.hackernet.se`
`base dc=hackernet,dc=se`
`...`

Öppna `/etc/nsswitch.conf` och lägg till följande:

`passwd: compat ldap`
`group: compat ldap`
`shadow: compat ldap`
`netgroup:ldap`

Starta sedan om tjänsten **nslcd** och **nscd**

`service nscd restart`
`service nslcd restart`

### Libnss-ldap

Autentisera login mot LDAP servern. Veriferat på Debian 7 (Wheezy)

`apt-get update && apt-get install libnss-ldap libpam-ldap ldap-utils`

1.  Specifera URL till din ldap server.
2.  Skriv in din base dn. Samma som BASE i `/etc/ldap/ldap.conf`
3.  Välj V3.
4.  Fyll i hela suffixen till adminkontot.
5.  Lösenordet för adminkontot.
6.  Välj ok. Vi ska ändra i den filen senare.
7.  Välj vad du vill.
8.  Välj vad du vill.
9.  Fyll i hela suffixen till ditt LDAP adminkonto. Oftast samma som i
    steg 4.
10. Lösenordet för adminkontot.

Öppna sedan filen,

`vim /etc/nsswitch.conf`

På linje \#7 lägg till,

`passwd: compat ldap`
`group: compat ldap`
`shadow: compat ldap`

På linje \#19 ändra till,

`netgroup:ldap`

Öppna sedan filen,

`vim /etc/pam.d/common-password`

På linje \#26 ta bort `use_authtok` och lägg till,

`password     [success=1 user_unknown=ignore default=die]     pam_ldap.so try_first_pass`

I filen /etc/pam_ldap.conf. Leta upp kommandot pam_password och ändra
till exop. Om du byter lösenord med passwd så väljer Debian default att
skicka över lösenordet krypterat med Crypt. Crypt klarar max 8 tecken
och är inte säkert. Väljer man exop så sköter OpenLDAP krypteringen av
lösenordet.

`pam_password exop`

Man kan skippa detta steget om man inte vill att en hemmapp ska skapas
automatiskt lokalt på datorn,

`vim /etc/pam.d/common-session`

Och lägga till denna raden i slutet.

`session optional        pam_mkhomedir.so skel=/etc/skel umask=077`

Starta sedan om datorn och prova att logga in med ett domänkonto.

Styr Sudo med LDAP grupp
------------------------

Skapa en [posixGroup](/OpenLDAP#posixGroup "wikilink") som heter sudo.
Lägg sedan till användarna som du vill ska få sudo rättigheter i den.
Verifiera att din användare finns med i sudo gruppen genom att logga in
och skriva groups.

`sparco@jumpoff:~$ groups`
`root wiki sudo`

Lägg sedan till denna raden i `/etc/sudoers` på din server.

`%sudo   ALL=(ALL:ALL) ALL`

Troubleshoot
------------

### Getent

Getent står för get entries och används för att visa rader i databaser
som supportas av Name Service Switch libraries(nsswitch.conf).

**passwd** visar alla användare som servern hittar.

`getent passwd`

**group** visar alla grupper som hittas.

`getent group`

Förslag på möjliga rubriker
---------------------------

#### LDAP med TLS

#### LDAP-replikering