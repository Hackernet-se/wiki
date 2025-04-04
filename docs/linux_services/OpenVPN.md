---
title: OpenVPN
permalink: /OpenVPN/
---

[Category:Guider](/Category:Guider "wikilink") OpenVPN är öppen källkod.
Detta är exempelkonf för remote access med säkerhet i åtanke.
Två-faktors-autentisering för inlogg samt TLS-autentisering av paketen.
Tyvärr kan man inte hårdställa TLS-version. CA-certifikatet och
TLS-nyckeln körs inline i konfigfilen för att det ska bli färre filer
att hålla reda på. Remote access VPN är utmärkt om du vill känna dig som
hemma var du än befinner dig.

Installation
------------

Med pakethanterare:

`apt-get install openvpn`
`openvpn --version`

Road warrior installer.

`wget `[`https://git.io/vpn`](https://git.io/vpn)` | sudo bash`

OBS kontrollera det du wgetar innan du pipear till sudo bash.

Konfiguration
-------------

Openvpn är uppdelat i server och klient.

### Server

En OpenVPN-server måste ha Diffie-Hellman-parametrar.

`time openssl dhparam -out dhparam.pem 4096`

Servern måste kunna forwarda trafik

`echo 1 > /proc/sys/net/ipv4/ip_forward`

TLS-autentiseringsnyckeln ska vara samma på servern som klienterna

`openvpn --genkey --secret ta.key`

`dev tun`
`proto tcp`
`server 10.8.0.0 255.255.255.0`
`ifconfig-pool-persist ipp.txt`

`ca [inline]`
`cert Server.crt`
`key Server.pem`
`#auth-`

`dh dhparam.pem`
`tls-server`
`tls-auth [inline] 0`

`keepalive 10 30`
`cipher AES-256-CBC`
`user nobody`
`group nogroup`
`persist-key`
`persist-tun`
`comp-lzo`
`tun-mtu 1500`
`mssfix 1200`
`verb 3`

`client-to-client`
`status openvpn-status.log`

`push "redirect-gateway def1 bypass-dhcp"`
`push "dhcp-option DNS 10.8.0.1"`

<ca>
`-----BEGIN CERTIFICATE-----`
`MIIFjjCCA3agAwIBAgICAQAwDQYJKoZIhvcNAQENBQAwaDELMAkGA1UEBhMCU0Ux`
`...`
`W45x0oueEpRKlORpP00dSaeAEj9yJCd/0pltmmR92cGVYg==`
`-----END CERTIFICATE-----`
</ca>

<tls-auth>
`-----BEGIN OpenVPN Static key V1-----`
`fae4feae672f9e291a40be76ee408106`
`...`
`16c46f97c66441da9bcddd2f717672d0`
`-----END OpenVPN Static key V1-----`
</tls-auth>

### Klient

Klientkonf som funkar till serverkonfen ovan. Spara conf filen i
`/etc/openvpn/client/`

`client`
`dev tun0`
`proto udp`
`remote vpn.hackernet.se 1194`
`resolv-retry infinite`
`nobind`

`ca [inline]`
`cert Klient1.crt`
`key Klient1.pem`
`auth-user-pass auth.txt`

`tls-client`
`tls-auth [inline] 1`
`verify-x509-name vpn.hackernet.se name`

`keepalive 10 30`
`cipher AES-256-CBC`
`auth SHA256`
`persist-key`
`persist-tun`
`comp-lzo`
`tun-mtu 1500`
`mssfix 1200`
`verb 3`

<ca>
`-----BEGIN CERTIFICATE-----`
`MIIFjjCCA3agAwIBAgICAQAwDQYJKoZIhvcNAQENBQAwaDELMAkGA1UEBhMCU0Ux`
`...`
`W45x0oueEpRKlORpP00dSaeAEj9yJCd/0pltmmR92cGVYg==`
`-----END CERTIFICATE-----`
</ca>

<tls-auth>
`-----BEGIN OpenVPN Static key V1-----`
`fae4feae672f9e291a40be76ee408106`
`...`
`16c46f97c66441da9bcddd2f717672d0`
`-----END OpenVPN Static key V1-----`
</tls-auth>

HTTPS
-----

OpenVPN och HTTPS kan samsas på samma port.

[<File:Openvpn1.png>](/File:Openvpn1.png "wikilink")

Dölja trafik
------------

En bra början:
<https://www.bestvpn.com/blog/5919/how-to-hide-openvpn-traffic-an-introduction/>

Systemd service
---------------

Vill du veta mer om hur systemd templates fungerar kan du läsa
[här](/Systemd#Template_unit "wikilink").