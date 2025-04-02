---
title: HashiCorp Vault
permalink: /HashiCorp_Vault/
---

Vault är ett system som centralt säkrar, lagrar och kontrollerar access
till tokens, passwords, certificates och API keys. Allt är krypterat by
default, både offline och vid transit (TLS). Vault är server/client och
har CLI, web UI samt REST JSON/HTTP API. För att accessa Vault så finns
ett auth-lager med backend, t.ex. LDAP eller AD. ACLer styr vem som får
accessa vad och allt loggas i en audit-logg. Det finns stöd för Dynamic
secrets (short-lived).

Installation
------------

Ubuntu

``` Bash
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install vault
```

Server
------

Starta server

`vault server`
`vault status`

Klient
------

`export VAULT_ADDR='`[`http://127.0.0.1:8200`](http://127.0.0.1:8200)`'`
`export VAULT_TOKEN="s.Va50wjIqgl6zHReb4aLDb"`

Write simple secret

`vault kv put secret/hello foo=world`

Read secret

`vault secrets list`
`vault kv get secret/hello`
`vault kv get -format=json secret/hello | jq .`

Konfiguration
-------------

### LDAP/AD login

Enable LDAP login

`vault auth enable ldap`

Konfa LDAP pluginet

`vault write auth/ldap/config \`
`    url="`[`ldaps://ad.hackernet.se`](ldaps://ad.hackernet.se)`" \`
`    userattr="sAMAccountName" \`
`    userdn="OU=users,DC=hackernet,DC=se" \`
`    groupdn="OU=groups,DC=hackernet,DC=se" \`
`    groupattr="cn" \`
`    binddn="CN=`<binduser>`,DC=hackernet,DC=se" \`
`    bindpass='`<secret password>`' \`
`    insecure_tls=false \`
`    starttls=true`

Ge en AD/LDAP grupp login rättigheter samt default policyn.

`vault write auth/ldap/groups/`<GRUPP NAMN>` policies=default`