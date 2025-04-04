---
title: Pi-hole
permalink: /Pi-hole/
---

Pi-hole är en färdig DNS server med inbyggd adblock och malware block.

Eftersom Pi-hole blockar reklam redan på DNS nivå så kommer det funka på
**alla enheter** och appar i mobilen. Får man problem att använda någon
sida så kan det därför vara bra att inaktivera Pi-hole en stund, det gör
man visa WebUI.

-   **DNS over TLS (DoT)** packages DNS transactions over a persistent
    TLS session over TCP
-   **DNS over QUIC (DoQ)** packages DNS transactions over an encrypted
    QUIC session over UDP
-   **DNS over HTTPS (DoH)** uses DNS over HTTP/3 (over QUIC) where
    supported, and DNS over HTTP2 (over TLS) otherwise

Installation
============

Pi-Hole går att installera på bla **Ubuntu, Debian, CentOS, Fedora**.
För att installera Pi-hole kör man deras script.

`curl -sSL `[`https://install.pi-hole.net`](https://install.pi-hole.net)` | bash`

Uppdatera sedan din DHCP server så att den skickar ut Pi-Hole serverns
IP adress som DNS server.

Uppgradera
----------

Kör följande kommando för att uppgradera Pi-hole:

`pihole -up`

Dry-run

`pihole -up --check-only`

Konfiguration
=============

Pi-hole har ett webui för att kunna göra enklare inställningar. Det når
man via:

[`http://`](http://)<pi-hole IP>`/admin`

[Category:Guider](/Category:Guider "wikilink")