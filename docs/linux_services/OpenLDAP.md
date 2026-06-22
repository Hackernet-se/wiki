---
title: OpenLDAP
permalink: /OpenLDAP/
---

 så
behöver användarna ligga i en sån här grupp.

```
dn: cn=vcenter,dc=example,dc=se
objectclass: groupOfUniqueNames
objectclass: top
cn: vcenter
description: vcenter group
uniqueMember: cn=user1,ou=users,dc=example,dc=se
```

### memberOf

För enkelt göra ställa frågor och se vilken grupp en användare är med i
så behöver man aktivera `memberOf`.

Skapa tre filer med följande kod i. **memberof.ldif**

```
dn: cn=module,cn=config
cn: module
objectClass: olcModuleList
olcModuleLoad: memberof
olcModulePath: /usr/lib/ldap
```

```
dn: olcOverlay={0}memberof,olcDatabase={1}hdb,cn=config
objectClass: olcConfig
objectClass: olcMemberOf
objectClass: olcOverlayConfig
objectClass: top
olcOverlay: memberof
olcMemberOfDangling: ignore
olcMemberOfRefInt: TRUE
olcMemberOfGroupOC: groupOfNames
olcMemberOfMemberAD: member
olcMemberOfMemberOfAD: memberOf
```

**refint1.ldif**

```
dn: cn=module{1},cn=config
add: olcmoduleload
olcmoduleload: refint
```

**refint2**

```
dn: olcOverlay={1}refint,olcDatabase={1}hdb,cn=config
objectClass: olcConfig
objectClass: olcOverlayConfig
objectClass: olcRefintConfig
objectClass: top
olcOverlay: {1}refint
olcRefintAttribute: memberof member manager owner
```

Ladda sedan in filerna i OpenLDAP servern med följande kommandon.

```
ldapadd -Q -Y EXTERNAL -H ldapi:/// -f memberof.ldif
ldapmodify -Q -Y EXTERNAL -H ldapi:/// -f refint1.ldif
ldapadd -Q -Y EXTERNAL -H ldapi:/// -f refint2.ldif
```

Skapa sedan en grupp och lägg till användare.

**add_group.ldif**

```
dn: cn=testgrupp,dc=example,dc=se
objectClass: groupofnames
cn: testgrupp
description: All users
member: uid=testuser,ou=users,dc=example,dc=se
```

```
ldapadd -x -D cn=admin,dc=example,dc=se -W -f add_group.ldif
```

För att testa att det funkar kan du ställa denna frågan.

`ldapsearch -h `<ip>` -x -b "dc=example,dc=se" '(uid=testuser)' memberOf`

### RootDN

För att göra ändringar i `cn=config` som innehåller själva LDAP
konfigurationen behöver man skapa ett admin konto med lösenord.

Under cn=config kan man sätta bland annat ACLer för vilka användare som
får läsa och skriva så man inte behöver använda cn=admin kontot varje
gång.

```
dn: olcDatabase={0}config,cn=config
changetype: modify
add: olcRootDN
olcRootDN: cn=admin,cn=config
```

```
dn: olcDatabase={0}config,cn=config
changetype: modify
add: olcRootPW
olcRootPW: secret
```

```
ldapadd -Y EXTERNAL -H ldapi:/// -f rootconfig.ldif
```

För att nå cn=config med Apache Directory Studio.

<File:openldap_04.png> <File:openldap_05.png> <File:openldap_06.png>

### Postfix Schema

För att styra en mailserver med LDAP behövs postfix schemat för att få
fler object klasser.

```
cd /etc/ldap/schema
```
`wget `[`http://www.postfix-buch.com/download/postfix-book.schema.gz`](http://www.postfix-buch.com/download/postfix-book.schema.gz)` && gunzip postfix-book.schema.gz`
```
mkdir ldif_output
```

``` bash
cat <<'__EOF__'>>schema_convert.conf
include /etc/ldap/schema/core.schema
include /etc/ldap/schema/cosine.schema
include /etc/ldap/schema/nis.schema
include /etc/ldap/schema/inetorgperson.schema
include /etc/ldap/schema/postfix-book.schema
__EOF__
```

```
slapcat -f schema_convert.conf -F ./ldif_output/ -n0
cp /etc/ldap/schema/ldif_output/cn\=config/cn\=schema/cn\=\{4\}postfix-book.ldif /etc/ldap/schema/postfix-book.ldif
```

Öppna och ändra följande i `postfix-book.ldif`

-   dn: cn=postfix-book,cn=schema,cn=config
-   cn: postfix-book
-   Ta bort allt från structuralObjectClass och neråt.

Importera ldif filen och starta om slapd.

```
ldapadd -Y EXTERNAL -H ldapi:/// -f postfix-book.ldif
```

<div class="toccolours mw-collapsible mw-collapsed" style="width:800px">

Exempel LDIF på hur en mail användare kan se ut.



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




Client
------

### Nslcd

Enklaste sättet att autha mot en LDAP server är att använda nslcd.

```
apt-get install nslcd
```

Lägg sedan till följande i `/etc/nslcd.conf`

```
...
uri ldapserver.hackernet.se
base dc=hackernet,dc=se
...
```

Öppna `/etc/nsswitch.conf` och lägg till följande:

```
passwd: compat ldap
group: compat ldap
shadow: compat ldap
netgroup:ldap
```

Starta sedan om tjänsten **nslcd** och **nscd**

```
service nscd restart
service nslcd restart
```

### Libnss-ldap

Autentisera login mot LDAP servern. Veriferat på Debian 7 (Wheezy)

```
apt-get update && apt-get install libnss-ldap libpam-ldap ldap-utils
```

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

```
vim /etc/nsswitch.conf
```

På linje \#7 lägg till,

```
passwd: compat ldap
group: compat ldap
shadow: compat ldap
```

På linje \#19 ändra till,

```
netgroup:ldap
```

Öppna sedan filen,

```
vim /etc/pam.d/common-password
```

På linje \#26 ta bort `use_authtok` och lägg till,

```
password     [success=1 user_unknown=ignore default=die]     pam_ldap.so try_first_pass
```

I filen /etc/pam_ldap.conf. Leta upp kommandot pam_password och ändra
till exop. Om du byter lösenord med passwd så väljer Debian default att
skicka över lösenordet krypterat med Crypt. Crypt klarar max 8 tecken
och är inte säkert. Väljer man exop så sköter OpenLDAP krypteringen av
lösenordet.

```
pam_password exop
```

Man kan skippa detta steget om man inte vill att en hemmapp ska skapas
automatiskt lokalt på datorn,

```
vim /etc/pam.d/common-session
```

Och lägga till denna raden i slutet.

```
session optional        pam_mkhomedir.so skel=/etc/skel umask=077
```

Starta sedan om datorn och prova att logga in med ett domänkonto.

Styr Sudo med LDAP grupp
------------------------

Skapa en [posixGroup](/OpenLDAP#posixGroup "wikilink") som heter sudo.
Lägg sedan till användarna som du vill ska få sudo rättigheter i den.
Verifiera att din användare finns med i sudo gruppen genom att logga in
och skriva groups.

```
sparco@jumpoff:~$ groups
root wiki sudo
```

Lägg sedan till denna raden i `/etc/sudoers` på din server.

```
%sudo   ALL=(ALL:ALL) ALL
```

Troubleshoot
------------

### Getent

Getent står för get entries och används för att visa rader i databaser
som supportas av Name Service Switch libraries(nsswitch.conf).

**passwd** visar alla användare som servern hittar.

```
getent passwd
```

**group** visar alla grupper som hittas.

```
getent group
```

Förslag på möjliga rubriker
---------------------------

#### LDAP med TLS

#### LDAP-replikering