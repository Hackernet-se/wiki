---
title: Mailserver
permalink: /Mailserver/
---

[Category:Guider](/Category:Guider "wikilink")
[Category:Sparco](/Category:Sparco "wikilink") För att sätta upp en
mailserver snabbt kan man använda [IRedMail](/IRedMail "wikilink"). Om
man vill sätta upp en själv med [Dovecot](/Dovecot "wikilink") och
[Postfix](/Postfix "wikilink") och koppla allt till
[OpenLDAP](/OpenLDAP "wikilink") för att lättare hantera login och
skapandet av nya användare. Och sätta upp en
[Roundcube](/Roundcube "wikilink") för att hantera webmail.

Förberedelse
------------

Öppna portar i brandväggen.

-   25 (SMTP)
-   80 (HTTP)
-   110 (POP3)
-   143 (IMAP)
-   443 (HTTPS)

Skapa ett A och MX record i DNSen som spekar mot mailservern.

Importera postfix schema på
[OpenLDAP](/OpenLDAP#Postfix_Schema "wikilink") servern.

Postfix
=======

Installation
------------

`apt-get install postfix postfix-pcre postfix-ldap`

Om man vill kunna skicka testmails(swaks) och enkelt styra
mailboxen(mutt).

`apt-get install mutt swaks`

Konfiguration
-------------

Konfigurations filerna finns under `/etc/postfix`

<div class="toccolours mw-collapsible mw-collapsed" style="width:800px">

`main.cf` Detta är main konfigurations filen.

<div class="mw-collapsible-content">

``` bash
#!/bin/bash
###################################################################################################
### Base Settings ###
#####################

# Listen on all interfaces
inet_interfaces = all

# Use TCP IPv4
inet_protocols = ipv4

# Greet connecting clients with this banner
smtpd_banner = $myhostname ESMTP $mail_name (Ubuntu)

# Fully-qualified hostname
myhostname = mail.example.com

# Do not append domain part to incomplete addresses (this is the MUA's job)
append_dot_mydomain = no

# Trusted networks/hosts (these are allowed to relay without authentication)
mynetworks =
    # Local
    127.0.0.0/8
    # External
    1.2.3.4/32


###################################################################################################
### Local Transport ###
#######################

# Disable local transport (so that system accounts can't receive mail)
local_transport = error:Local Transport Disabled

# Don't use local alias maps
alias_maps =

# Local domain (could be omitted, since it is automatically derived from $myhostname)
mydomain = example.com

# Mails for these domains will be transported locally
mydestination =
    $myhostname
    localhost.$mydomain
    localhost


###################################################################################################
### Virtual Transport ###
#########################

# Deliver mail for virtual recipients to Dovecot
virtual_transport = dovecot

# Process one mail at one time
dovecot_destination_recipient_limit = 1

# Valid virtual domains
virtual_mailbox_domains = hash:/etc/postfix/virtual_domains

# Valid virtual recipients
virtual_mailbox_maps = proxy:ldap:/etc/postfix/ldap_virtual_recipients.cf

# Virtual aliases
virtual_alias_maps = proxy:ldap:/etc/postfix/ldap_virtual_aliases.cf


###################################################################################################
### ESMTP Settings ###
######################

### SASL ###

# Enable SASL (required for SMTP authentication)
smtpd_sasl_auth_enable = yes

# Enable SASL for Outlook-Clients as well
broken_sasl_auth_clients = yes

### TLS ###

# Enable TLS (required to encrypt the plaintext SASL authentication)
smtpd_tls_security_level = may

# Only offer SASL in a TLS session
smtpd_tls_auth_only = yes

# Certification Authority
smtpd_tls_CAfile = /etc/postfix/certs/example-cacert.pem

# Public Certificate
smtpd_tls_cert_file = /etc/postfix/certs/mail_public_cert.pem

# Private Key (without passphrase)
smtpd_tls_key_file = /etc/postfix/certs/mail_private_key.pem

# Randomizer for key creation
tls_random_source = dev:/dev/urandom

# TLS related logging (set to 2 for debugging)
smtpd_tls_loglevel = 0

# Avoid Denial-Of-Service-Attacks
smtpd_client_new_tls_session_rate_limit = 10

# Activate TLS Session Cache
smtpd_tls_session_cache_database = btree:/etc/postfix/smtpd_session_cache

# Deny some TLS-Ciphers
smtpd_tls_exclude_ciphers =
        EXP
        EDH-RSA-DES-CBC-SHA
        ADH-DES-CBC-SHA
        DES-CBC-SHA
        SEED-SHA

# Diffie-Hellman Parameters for Perfect Forward Secrecy
# Can be created with:
# openssl dhparam -2 -out dh_512.pem 512
# openssl dhparam -2 -out dh_1024.pem 1024
smtpd_tls_dh512_param_file = ${config_directory}/certs/dh_512.pem
smtpd_tls_dh1024_param_file = ${config_directory}/certs/dh_1024.pem


###################################################################################################
### Connection Policies ###
###########################

# Reject Early Talkers
postscreen_greet_action = enforce


###################################################################################################
### Session Policies ###
########################

# Recipient Restrictions (RCPT TO related)
smtpd_recipient_restrictions =
        # Allow relaying for SASL authenticated clients and trusted hosts/networks
        # This can be put to smtpd_relay_restrictions in Postfix 2.10 and later
        permit_sasl_authenticated
        permit_mynetworks
        reject_non_fqdn_recipient
        reject_unknown_recipient_domain
        reject_unauth_destination
        # Reject the following hosts
        check_sender_ns_access cidr:/etc/postfix/drop.cidr
        check_sender_mx_access cidr:/etc/postfix/drop.cidr
        # Additional blacklist
        reject_rbl_client ix.dnsbl.manitu.net
        # Finally permit (relaying still requires SASL auth)
        permit

# Reject the request if the sender is the null address and there are multiple recipients
smtpd_data_restrictions = reject_multi_recipient_bounce

# Sender Restrictions
smtpd_sender_restrictions =
        reject_non_fqdn_sender
        reject_unknown_sender_domain

# HELO/EHLO Restrictions
smtpd_helo_restrictions =
        permit_mynetworks
        check_helo_access pcre:/etc/postfix/identitycheck.pcre
        #reject_non_fqdn_helo_hostname
        reject_invalid_hostname

# Deny VRFY recipient checks
disable_vrfy_command = yes

# Require HELO
smtpd_helo_required = yes

# Reject instantly if a restriction applies (do not wait until RCPT TO)
smtpd_delay_reject = no

# Client Restrictions (IP Blacklist)
smtpd_client_restrictions = check_client_access cidr:/etc/postfix/drop.cidr
```

</div>
</div>
<div class="toccolours mw-collapsible mw-collapsed" style="width:800px">

`virtual_domains` Innehåller vilka domäner server tar emot mail för.

<div class="mw-collapsible-content">

``` bash
#!/bin/bash
# Domain        Anything
example.com     OK
```

</div>
</div>
<div class="toccolours mw-collapsible mw-collapsed" style="width:800px">

`ldap_virtual_recipients.cf` LDAP fråga för att validera mottagaren.

<div class="mw-collapsible-content">

``` bash
#!/bin/bash
bind = yes
bind_dn = uid=postfix,ou=services,dc=example,dc=com
bind_pw = secret
server_host = ldap://127.0.0.1:389
search_base = ou=people,dc=example,dc=com
domain = example.com
query_filter = (&(mail=%s)(mailEnabled=TRUE))
result_attribute = mail
```

</div>
</div>
<div class="toccolours mw-collapsible mw-collapsed" style="width:800px">

`ldap_virtual_aliases.cf` LDAP fråga för att få fram aliases och
forwarding adress.

<div class="mw-collapsible-content">

``` bash
#!/bin/bash
bind = yes
bind_dn = uid=postfix,ou=services,dc=example,dc=com
bind_pw = secret
server_host = ldap://127.0.0.1:389
search_base = ou=people,dc=example,dc=com
domain = example.com
query_filter = (&(mailAlias=%s)(mailEnabled=TRUE))
result_attribute = mail, email
```

</div>
</div>
<div class="toccolours mw-collapsible mw-collapsed" style="width:800px">

`identitycheck.pcre` Regexp för att blocka klienter som använder ditt
hostnamn.

<div class="mw-collapsible-content">

``` bash
#!/bin/bash
# Identity (RegEx)      Action

/^(mail\.example\.com)$/    REJECT Hostname Abuse: $1
/^(1\.2\.3\.4)$/        REJECT Hostname Abuse: $1
/^(\[1\.2\.3\.4\])$/        REJECT Hostname Abuse: $1
```

</div>
</div>
<div class="toccolours mw-collapsible mw-collapsed" style="width:800px">

`drop.cidr` Innehåller svartlistade IP-adresser.

<div class="mw-collapsible-content">

``` bash
#!/bin/bash
# IP/CIDR           Action

1.2.3.0/24          REJECT Blacklisted
```

</div>
</div>

Temporärt kommentera ut följande rader eftersom att
[Dovecot](/Dovecot "wikilink") och TLS inte är konfigurerat i main.cf:

-   dovecot_destination_recipient_limit = 1
-   smtpd_tls_security_level = may
-   smtpd_tls_auth_only = yes
-   smtpd_tls_CAfile = /etc/postfix/certs/example-cacert.pem
-   smtpd_tls_cert_file = /etc/postfix/certs/mail_public_cert.pem
-   smtpd_tls_key_file = /etc/postfix/certs/mail_private_key.pem

Skapa en postmap db fil för din domän.

`postmap hash:/etc/postfix/virtual_domains`

Starta postfix och anslut mot servern med telnet mot port 25. Prova att
skicka `EHLO client`, då ska du få följande svar:

``` text
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
220 mail.example.com ESMTP Postfix (Ubuntu)
EHLO client
250-mail.example.com
250-PIPELINING
250-SIZE 10240000
250-ETRN
250-AUTH DIGEST-MD5 NTLM CRAM-MD5 LOGIN PLAIN
250-AUTH=DIGEST-MD5 NTLM CRAM-MD5 LOGIN PLAIN
250-ENHANCEDSTATUSCODES
250-8BITMIME
250 DSN
QUIT
221 2.0.0 Bye
```

Testa att ställa en LDAP fråga.

`postmap -q user@example.com `[`ldap:/etc/postfix/ldap_virtual_recipients.cf`](ldap:/etc/postfix/ldap_virtual_recipients.cf)
`postmap -q postmaster@example.com `[`ldap:/etc/postfix/ldap_virtual_aliases.cf`](ldap:/etc/postfix/ldap_virtual_aliases.cf)

Båda frågorna bör ge user@example.com som svar.

Dovecot
=======

Installation
------------

`apt-get install dovecot-core dovecot-imapd dovecot-pop3d dovecot-lmtpd dovecot-ldap`

Konfiguration
-------------

Stäng av protocol som du inte behöver i filen
`/etc/dovecot/conf.d/10-master.conf` genom att sätta porten på **0**.
Och sätt permissions, användare och grupp för **authentication-userdb**
i samma fil:

``` php
inet_listener imaps {
    port = 0
    #port = 993
    #ssl = yes
}
```



``` php
inet_listener pop3s {
    port = 0
    #port = 995
    #ssl = yes
}
```



``` php
unix_listener auth-userdb {
    mode = 0600
    user = vmail
    group = vmail
}
```

Stäng av system-based authentication och sätt på LDAP-based
authentication istället i `/etc/dovecot/conf.d/10-auth.conf`:

``` php
auth_mechanisms = plain login
#!include auth-system.conf.ext
!include auth-ldap.conf.ext
```

Sätt dom LDAP relaterade inställningarna i
`/etc/dovecot/dovecot-ldap.conf.ext`:

``` bash
hosts = 127.0.0.1
dn = uid=dovecot,ou=services,dc=example,dc=com
dnpass = secret
ldap_version = 3
base = ou=people,dc=example,dc=com
user_attrs = mailHomeDirectory=home,mailUidNumber=uid,mailGidNumber=gid,mailStorageDirectory=mail
user_filter = (&(objectClass=PostfixBookMailAccount)(uniqueIdentifier=%n))
pass_attrs = uniqueIdentifier=user,userPassword=password
pass_filter = (&(objectClass=PostfixBookMailAccount)(uniqueIdentifier=%n))
default_pass_scheme = CRYPT
```

Aktivera loggning i `/etc/dovecot/conf.d/10-logging.conf`:

`log_path = syslog`
`syslog_facility = mail`
`auth_debug = yes`

Sätt SSL cert i `/etc/dovecot/conf.d/10-ssl.conf`:

`ssl_cert = `</etc/dovecot/mail_public_cert.pem
 ssl_key = </etc/dovecot/private/mail_private_key.pem

Skapa en användare och en grupp som heter '''vmail''' med uid och gid 5000:
 addgroup --system --gid 5000 vmail
 adduser --system --home /srv/vmail --uid 5000 --gid 5000 --disabled-password --disabled-login vmail

Starta dovecot och gör ett IMAP connection & authentication test med hjälp av telnet. Om du inte vill starta dovecot i bakgrunden använd <code>`dovecot -f`</code>`.`

`telnet 127.0.0.1 143` och skicka `1 login user@example.com secret`

``` bash
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
* OK [CAPABILITY IMAP4rev1 LITERAL+ SASL-IR LOGIN-REFERRALS ID ENABLE IDLE STARTTLS AUTH=PLAIN AUTH=LOGIN] Dovecot (Ubuntu) ready.
1 login user@example.com secret
1 OK [CAPABILITY IMAP4rev1 LITERAL+ SASL-IR LOGIN-REFERRALS ID ENABLE IDLE SORT SORT=DISPLAY THREAD=REFERENCES THREAD=REFS THREAD=ORDEREDSUBJECT MULTIAPPEND URL-PARTIAL CATENATE UNSELECT CHILDREN NAMESPACE UIDPLUS LIST-EXTENDED I18NLEVEL=1 CONDSTORE QRESYNC ESEARCH ESORT SEARCHRES WITHIN CONTEXT=SEARCH LIST-STATUS SPECIAL-USE BINARY MOVE] Logged in
2 logout
* BYE Logging out
```

Aktivera Dovecot deliver i Postfix genom att lägga till följande rad i
`/etc/postfix/master.cf`:

``` bash
dovecot   unix  -       n       n       -       -       pipe
        flags=ODRhu user=vmail:vmail argv=/usr/lib/dovecot/deliver -e -f ${sender} -d ${recipient}
```

Sätt en postmaster adress i `/etc/dovecot/conf.d/15-lda.conf`:

`postmaster_address = postmaster@example.com`

Starta om **Dovecot** och **Postfix** och gör sedan ett deliver test.

`swaks --from user1@example.com --to user2@example.com --server 127.0.0.1:25`

Kolla i log filerna eller i user2 mailbox

`mutt -f /srv/vmail/user2@example.com/Maildir/`

SASL
====

Installation
------------

`apt-get install libsasl2-2 sasl2-bin`

Konfiguration
-------------

Skapa **"smtpd.conf"** i `/etc/postfix/sasl/`:

`log_level: 3`
`pwcheck_method: saslauthd`
`mech_list: PLAIN LOGIN`

Sätt på autostart välj LDAP som mekanism och sätt options för en
chrootad Postfix i `/etc/default/saslauthd`:

`START=yes`
`MECHANISMS="ldap"`
`OPTIONS="-c -m /var/spool/postfix/var/run/saslauthd"`

Skapa LDAP konfigurationen i `/etc/saslauthd.conf`:

`ldap_servers: `[`ldap://127.0.0.1/`](ldap://127.0.0.1/)
`ldap_bind_dn: uid=saslauthd,ou=services,dc=example,dc=com`
`ldap_bind_pw: secret`
`ldap_timeout: 10`
`ldap_time_limit: 10`
`ldap_scope: sub`
`ldap_search_base: ou=people,dc=example,dc=com`
`ldap_auth_method: bind`
`ldap_filter: (&(uniqueIdentifier=%u)(mailEnabled=TRUE))`
`ldap_debug: 0`
`ldap_verbose: off`
`ldap_ssl: no`
`ldap_starttls: no`
`ldap_referrals: yes`

Sätt sedan rätt permissions på filen.

`chown root:sasl /etc/saslauthd.conf`
`chmod 640 /etc/saslauthd.conf`

Lägg till Postfix användaren i sasl gruppen.

`adduser postfix sasl`

Starta sedan SASL och gör ett auth test:

`testsaslauthd -u user -p secret -f /var/spool/postfix/var/run/saslauthd/mux`

Om det funkar är svaret **0: OK “Success.”**

För att testa så att SASL fungerar med SMTP måste vi göra om username
och password till base64.

`perl -MMIME::Base64 -e 'print encode_base64("user\@example.com");'`
`perl -MMIME::Base64 -e 'print encode_base64("secret");'`

Öppna sedan en telnet session och skicka `EHLO test.local` följt av
`AUTH LOGIN`. Servern kommer då att fråga efter username och password,
skicka det som base64 encoded.

``` bash
telnet localhost 25

Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
220 mail.example.com ESMTP Postfix (Ubuntu)
EHLO test.local
250-mail.example.com
250-PIPELINING
250-SIZE 10240000
250-ETRN
250-STARTTLS
250-AUTH PLAIN LOGIN
250-AUTH=PLAIN LOGIN
250-ENHANCEDSTATUSCODES
250-8BITMIME
250 DSN
AUTH LOGIN
334 VXNlcm5hbWU6
YWxpY2VAZXhhbXBsZS5jb20=
334 UGFzc3dvcmQ6
c2VjcmV0
235 2.7.0 Authentication successful
QUIT
221 2.0.0 Bye
```

Om allt fungera ska du få svaret **235 2.7.0 Authentication
successful**. Om det inte fungera titta i log filerna. Om log filerna
inte hjälpte slå på extended logging genom att lägga till -v i smtpd
kommandot i `/etc/postfix/master.cf`:

`smtp      inet  n       -       -       -       -       smtpd -v`

Prova att skicka ett test mail med authentication.

`swaks --from user1@example.com --to user2@example.com --server 127.0.0.1:25 --auth plain --auth-user=user1@example.com`

TLS(Postfix)
============

Just nu så skickas lösenorden i plaintext. För att kryptera dom skapa
certifikat och lägg dom i `/etc/postfix/certs`. Kolla i **main.cf**
vilket filnamn dom ska ha. Skapa även 2st Diffie-Hellman filer i samma
map.

`openssl dhparam -2 -out dh_512.pem 512`
`openssl dhparam -2 -out dh_1024.pem 1024`

Sätt rätt permissions på mappen.

`chown -R root:root /etc/postfix/certs/`
`chmod -R 600 /etc/postfix/certs/`

Ta bort dom 6 kommentarerna du gjorde i `/etc/postfix/main.cf` filen i
början av guiden och starta om Postfix.

Om du nu telnetar till Postfix servern och skickar **EHLO client** så
ska det stå **STARTTLS** istället för **LOGIN PLAIN**.

Med följande kommando kan du prova att ansluta med **STARTTLS**.

`openssl s_client -CAfile certs/example-cacert.pem -starttls smtp -connect localhost:25`

Tips'N'Trix
===========

Säkra upp Dovecot och Postfix med TLS conf ifrån
[chiperlist](https://syslink.pl/cipherlist/).

Testa säkerheten på mailservern med [starttls](https://starttls.info)
eller [ssl-tools](https://ssl-tools.net/mailservers).

Klient
======

Du kan nu ansluta nån mail klient tex Thunderbird eller Outlook mot
servern och autentisera med ditt [OpenLDAP](/OpenLDAP "wikilink") login.

Man kan också sätta upp [Roundcube](/Roundcube "wikilink") för att
enkelt skicka och läsa din mail från en dator med en webbläsare.

[Category:Guider](/Category:Guider "wikilink")
[Category:Sparco](/Category:Sparco "wikilink")