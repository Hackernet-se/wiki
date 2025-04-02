---
title: Gitlab
permalink: /Gitlab/
---

[Category:Guider](/Category:Guider "wikilink") Gitlab är ett webbaserad
git repositry manager med bland annat en inbyggd wiki. Gitlab fungerar
som Github gör och dom erbjuder att så man kan hosta sin egna lösning på
sin egen server. Se även [Git](/Git "wikilink").

Det finns 2 version av Gitlab:

-   Gitlab CE: Community Edition.
-   Gitlab EE: Enterprise Edition.

Installation
============

Installera dom nödvändiga paketen. Postfix kan man skippa om man har en
annan mailserver.

`sudo apt-get install curl openssh-server ca-certificates postfix`

Lägg till Gitlab's repo och installera sedan Gitlab CE.

`curl -sS `[`https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh`](https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh)` | sudo bash`
`sudo apt-get install gitlab-ce`

Konfigurera sedan Gitlab och starta det.

`sudo gitlab-ctl reconfigure`

Konfiguration
=============

Att konfigurera är väldigt enkelt. Man gör sina ändringar i
`/etc/gitlab/gitlab.rb` efter det kör man `sudo gitlab-ctl reconfigure`
för att dom ska börja gälla.

HTTPS
-----

Ändra följande rad:

`external_url "`[`https://git.hackernet.se`](https://git.hackernet.se)`"`

Eftersom hostnamnet är **git.hackernet.se** så kommer gitlab leta efter
private key och certificate filen som heter **git.hackernet.se.key/crt**
under `/etc/gitlab/ssl/`.

Om du behöver ändra vart cert filerna finns och vad dom heter ändra
dessa 2 rader.

`nginx['ssl_certificate'] = "/opt/cert/fullchain.pem"`
`nginx['ssl_certificate_key'] = "/opt/cert/privkey.pem"`

**Redirect HTTP till HTTPS**
Ändra följande rad till true.

`nginx['redirect_http_to_https'] = true`

LDAP authentication
-------------------

För mer info kolla [Gitlab LDAP
document](https://gitlab.com/gitlab-org/omnibus-gitlab/blob/master/doc/settings/ldap.md)

`gitlab_rails['ldap_enabled'] = true`
`gitlab_rails['ldap_servers'] = YAML.load <<-'EOS' # remember to close this block with 'EOS' below`
`main: # 'main' is the GitLab 'provider ID' of this LDAP server`
`     label: 'Hackernet'`
`     host: 'openldap.hackernet.se'`
`     port: 389`
`     uid: 'uid'`
`     method: 'plain'`
`     bind_dn: '>ldap bind username>'`
`     password: '`<ldap bind password>`'`
`     active_directory: false`
`     allow_username_or_email_login: true`
`     block_auto_created_users: false`
`     base: '`<base DN>`'`
`     user_filter: ''`
`     attributes:`
`       username: ['uid', 'userid', 'sAMAccountName']`
`       email:    ['mail', 'email', 'userPrincipalName']`
`       name:       'cn'`
`       first_name: 'givenName'`
`       last_name:  'sn'`
`     ## EE only`
`     group_base: 'dc=hackernet,dc=se'`
`     admin_group: 'cn=wiki'`
`     sync_ssh_keys: false`
` EOS`

**Gör LDAP användare till admin**
För att göra en LDAP användare till admin kör följande kommando i shell:

`sudo gitlab-rails console`
`u = User.find_by_username("LDAPadmin")`
`u.admin = true`
`u.save`
`exit`

Schemalagd backup
-----------------

Simpel backup görs mha crontab och /var/opt/gitlab/backups kan sedan
<rsync:as> iväg till remote site.

`0 4 * * 7 /opt/gitlab/bin/gitlab-backup create CRON=1`
`1 4 * * 7 cp /etc/gitlab/gitlab-secrets.json /var/opt/gitlab/backups/ >/dev/null`
`1 4 * * 7 cp /etc/gitlab/gitlab.rb /var/opt/gitlab/backups/ >/dev/null`

Limit backup lifetime to 60 days, /etc/gitlab/gitlab.rb.

`gitlab_rails['backup_keep_time'] = 5184000`

CI/CD
=====

I ditt gitlab repo kan du skapa en fil som heter **.gitlab-ci.yml**.

Det är i denna filen som du specificerar vad din pipeline ska göra.

YAML Lint
---------

Pipeline som kollar att du har skrivit rätt YAML syntax i ditt repo.
Funkar bra tillsammans med tex [Puppet](/Puppet#Hiera "wikilink") hiera
config.

``` json
stages:
 - lint

lint-yaml:
  stage: lint
  image:
    name: cytopia/yamllint:latest
    entrypoint: ["/bin/ash", "-c"]
  script:
   - yamllint -f colored .
```

Om du vill att pipelinen ska skippa vissa filer eller du vill ändra
configen så kan du skapa en fil i rooten på ditt repo som heter
**.yamllint.yml**:

``` yaml
extends: default

ignore: |
  .yamllint.yml
  .gitlab-ci.yml

rules:
  # 80 chars should be enough, but don't fail if a line is longer
  line-length:
    max: 80
    level: warning

  # accept both     key:
  #                   - item
  #
  # and             key:
  #                 - item
  indentation:
    indent-sequences: whatever
```