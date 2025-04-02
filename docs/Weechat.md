---
title: Weechat
permalink: /Weechat/
---

[Category:Guider](/Category:Guider "wikilink") WeeChat är en
terminalbaserad Internet Relay Chat (IRC) klient. WeeChat är skriven i
C, och är gjord för att vara flexibel och utbyggbar. WeeChat har alla
möjliga plugins skrivna i olika språk t.ex.
[Python](/Python "wikilink"), Perl, och Ruby.

Installation
------------

Exempel: Ubuntu 18.04

`sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 11E9DE8848F2B65222AA75B8D1820DB22A11534E`
`sudo apt-get install apt-transport-https`
`echo "deb `[`https://weechat.org/ubuntu`](https://weechat.org/ubuntu)` bionic main" | sudo tee /etc/apt/sources.list.d/weechat.list `
`sudo apt-get update && sudo apt-get -y install weechat weechat-scripts`

Använd [Tmux](/Tmux "wikilink") och [Systemd](/Systemd "wikilink") för
att få weechat som en bakgrundstjänst med autostart.

``` bash
sudo dd of=/etc/systemd/system/weechat.service << EOF
[Unit]
Description=Weechat IRC Client (in tmux)

[Service]
User=$USER
Type=forking
ExecStart=/usr/bin/tmux -2 new-session -d -s weechat /usr/bin/weechat
ExecStop=/usr/bin/tmux kill-session -t weechat

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable weechat
```

Konfiguration
-------------

Starta Weechat och lägg in grundläggande konfiguration. Glöm inte att
spara efter varje inställning du gör som du vill ska finnas kvar efter
reboot.

`sudo systemctl start weechat && tmux attach`

`/set irc.server_default.nicks "HorseBoy_92"`
`/set irc.server_default.realname "John Smith"`
`/save`

#### Anslut till irc-nätverk

Basic exempel:

`/server add freenode irc.freenode.net/6667 -autoconnect`
`/set irc.server.freenode.autojoin "#FreeNAS,#cisco,#pfsense"`

Exempel med password och self-signed cert server side.

`/server add hacker irc1.hacker.se/6667 -password=noes -ssl -autoconnect`
`/set irc.server.hacker.ssl_verify off`
`/save`

Anslut till nästa IRC server.

`/reconnect freenode -switch`

#### Script

`/script`
`/script install keepnick.py`

#### Ångra inställning

Alla kommandon som börjar med /set kan man köra /unset på.

`/unset `<option>

#### Relay

Relay behövs för tex glowing-bear, se nedan.

`/set relay.network.password secretpw`
`/relay add weechat 9001`

Vet ej vilken av följande två som behövs för att tillåta klienter från
ett annat nät än samma som weechatservern.

`/set relay.network.allowed_ips *`
`/set relay.network.websocket_allowed_origins *`

Weechat relay lyssnar default efter IPv6. För att stänga av.

`/set relay.network.ipv6 off`

#### Skicka ett kommando när du ansluter.

`/set irc.server.quakenet.command "/MSG Q@CServe.quakenet.org AUTH USERNAME PASSWORD"`

#### Filter

Filter kan användas för att slippa se vissa ord, användare eller
meddelande.

För att filtrera bort join/part/quit-meddelanden.

`/set irc.look.smart_filter on`
`/filter add joinquit *.freenode.* irc_join,irc_part,irc_quit *`

Fish
----

`aptitude install python-crypto`
`/script install fish.py`
`/set fish.look.mark_encrypted "."`
`/set fish.look.mark_position off|begin|end`

`DH1080:                    /blowkey exchange nick `
`Set the key for a channel: /blowkey set -server freenet #blowfish key`
`Remove the key:            /blowkey remove #blowfish`
`Set the key for a query:   /blowkey set nick secret+key`
`List all keys:             /blowkey `

Glowing Bear
------------

Glowing Bear är en webb-frontend för weechat, byggd i html5. Man behöver
aldrig sköta något underhåll utav Glowing Bear, utan koden hämtas av din
webbläsare från deras servrar varje gång man använder det. Kräver att
man kör Weechat version 0.4.2 eller högre. En relay behövs för att
glowing bear ska fungera, se ovan. Anslut sedan på glowing bear sidan
mot IP eller DNS-namn. Notera att detta kan vara en intern IP.

Länk [http](http://www.glowing-bear.org/)
Länk [https](https://glowing-bear.github.io/glowing-bear/)

### SSL

För att kryptera trafiken mellan din webbläsare och din weechat relay så
använd SSL.

#### Skapa eget cert

`mkdir -p ~/.weechat/ssl && cd ~/.weechat/ssl`
`openssl req -nodes -newkey rsa:4096 -keyout relay.pem -x509 -days 3650 -out relay.pem -subj "/CN=glowing.fu.se/"`

`/set relay.network.password secretpw`
`/relay sslcertkey`
`/relay add ssl.weechat 9001`

#### Let's Encrypt

Weechat kan använda cert som är signade med [Let's
Encrypt](/Let's_Encrypt "wikilink").

`mkdir -p ~/.weechat/ssl`
`cat cert.pem > ~/.weechat/ssl/relay.pem && cat chain.pem >> ~/.weechat/ssl/relay.pem && cat privkey.pem >> ~/.weechat/ssl/relay.pem`
`/set relay.network.password secretpw`
`/relay sslcertkey`
`/relay add ssl.weechat 9001`

**För att ladda om SSL certet.**

`/relay sslcertkey`

### Bakom Reverse Proxy

För att köra glowing bear genom en
[Nginx](/Nginx "wikilink")/[Apache](/Apache "wikilink") HTTP reverse
proxy måste man köra det som en websocket, inte en HTTP-anslutning
("Upgrade").

**Nginx**.

``` apache
limit_req_zone $binary_remote_addr zone=weechat:10m rate=5r/m;

server {
        [... other config...]

        location /weechat {
            proxy_pass http://localhost:9001/weechat;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "Upgrade";
            proxy_read_timeout 604800;
            proxy_set_header X-Real-IP $remote_addr;
            limit_req zone=weechat burst=1 nodelay;
        }
}
```

**Apache**

``` apache
 <IfModule mod_proxy.c>
     ProxyVia On
     ProxyRequests Off
     ProxyPreserveHost off

     #Websocket
     ProxyPass / ws://10.0.0.10:9001/
     ProxyPassReverse / ws://10.0.0.10:9001/
 <Proxy *>
```