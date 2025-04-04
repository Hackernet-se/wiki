---
title: Cisco Security
permalink: /Cisco_Security/
---

[Cisco IOS](/Cisco_IOS "wikilink") har stöd för många
säkerhetsmekanismer och protokoll. Se även [L2
Security](/Cisco_L2_Security "wikilink"), [L3
Security](/Cisco_L3_Security "wikilink"),
[DMVPN](/Cisco_DMVPN "wikilink") och [Cisco
IPsec](/Cisco_IPsec "wikilink").

Device Security
===============

Login enhancements

`login block-for [seconds] attempts [attempts] within [seconds]`
`login on-failure log every 3`

`show login`
`show login failures`

Lägg till undantag

`ip access-list standard TRUSTED_HOSTS`
` permit host 10.0.0.10`
`login quiet-mode access-class TRUSTED_HOSTS`

Default genereras det ett syslog-meddelande om det görs 8 misslyckade
inloggningsförsök inom en minut. Detta tröskelvärde går att konfigurera.

`security authentication failure rate 8 log `

Password recovery är på default men går att stänga av.

`no service password-recovery`

### SSH

`ip ssh version 2`
`crypto key generate rsa modulus 2048`

`line vty 0 15`
` transport input ssh`

Verify

`show ssh`
`show ip ssh`
`show users`

**Public key SSH authentication**
Ens SSH-nyckel får inte plats på en rad utan man får lägga in det på
flera rader och avsluta med exit.

`ip ssh pubkey-chain`
` username cisco`
`  key-string`
`   AAAAB3NzaC1yc2EAAAADAQABAAABAQDLf...`
`   VPrV/fn35p1xq5Pc7b2oTxhe2sPEssVM7...`
`   exit`

Enable key based authentication only. Ordning på authentication methods
är default: publickey, keyboard-interactive, password.

`ip ssh server algorithm authentication publickey`

### Control Plane

Det är viktigt att skydda CPU i sina enheter, man kan styra accessen
(Control-Plane Policing) och man kan överbelastningsskydda
(Control-Plane Protection). CoPP skyddar route processor genom att
behandla det som en separat enhet med eget ingress interface. Man kan
styra trafik till control plane med hjälp av ACL:er och
[QoS](/Cisco_QoS "wikilink")-filter.

`class-map match-all COPP-IN-IP`
` match protocol ip`

`policy-map COPP-INBOUND`
` class COPP-IN-IP`
`  police rate 10 pps conform-action transmit  exceed-action drop `

`control-plane`
` service-policy input COPP-INBOUND`

`show policy-map control-plane`

Default CoPP

`cpp system-default `

Management Plane Protection

`control-plane host`
` management-interface GigabitEthernet 0/1 allow ssh https`

`show management-interface`

**AutoSecure**
AutoSecure finns i två modes, Interactive och Noninteractive där det
senare "Automatically executes the recommended Cisco default settings"
vilket bland annat stänger av ICMP redirects, unreachables och Proxy-ARP
på alla interface.

`auto-secure no-interact`
`show auto secure config`

AAA
===

AAA authentication på IOS kan konfigureras att använda upp till fyra
olika metoder för autentisering. Enheten kommer att använda metoderna i
ordning och det är endast vid error som nästa metod används, detta gör
att man kan ha fallbacks. *aaa new-model* gör att lokala usernames och
passwords på enheten används vid avsaknad av andra AAA statements.

`aaa new-model`
`aaa authentication username-prompt "Enter Username:"`
`aaa authentication password-prompt "Enter Password:"`

`aaa authentication enable default group tacacs+ enable`
`aaa authentication login default group tacacs+ local`

Debug

`debug aaa authentication`

Fallback user account ifall AAA-server är unreachable

`username fallback privilege 15 secret SECRETS`

Max failed attempts to lock the user

`aaa local authentication attempts max-fail 10`
`show aaa local user lockout`
`clear aaa local user locked`

### TACACS

TACACS+ är Ciscoproperitärt och all trafik är krypterad. Tacacs
kommunicerar på TCP port 49.

`aaa group server tacacs+ `
` server-private 10.0.0.20 key 7 078905478...`
` server-private 10.0.0.21 key 7 134272319...`
` ip vrf forwarding Mgmt`
` ip tacacs source-interface gi0`

`aaa authentication login default group tacacs+ local`
`aaa authorization exec default group tacacs+ if-authenticated`

Verify

`test aaa group tacacs+ USER SECRET123 new-code`
`show tacacs`

### Radius

Cisco IOS RADIUS använder AV pairs, UDP port 1645-1646 eller 1812-1813,
accounting är separat från authentication och authorization. Endast
lösenord är krypterat.

`radius server ISE1`
` address ipv4 10.0.0.30 auth-port 1812 acct-port 1813`
` key 7 01300F175804575D72`

`aaa group server radius ISE-GROUP`
` server name ISE1`
` server name ISE2`
` ip vrf forwarding mgmt`
` ip radius source-interface Vlan100`
` retransmit 2`
` timeout 4`
` deadtime 1`

`aaa authentication login VTY-LINES group ISE-GROUP local`
`aaa authorization exec default group radius local`

Verify

`test aaa group radius USER SECRET123 new-code`
`show radius`

IPS
===

IOS kan sättas upp som ett Intrusion Prevention System.

`mkdir ips`
`ip ips config location flash:/ips`
`ip ips name IPS`

`show ip ips config`

[Category:Cisco](/Category:Cisco "wikilink")