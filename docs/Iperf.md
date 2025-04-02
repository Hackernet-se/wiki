---
title: Iperf
permalink: /Iperf/
---

Iperf är ett verktyg som används för att testa bandbredd mellan 2 noder
i ett nätverk. Det sätter upp TCP- och UDP-dataströmmar för att mäta
throughput.

### Iperf3

Iperf3 är en omskrivning av Iperf från början, med målet om en mindre
och enklare kodbas. Programmet funkar med både IPv4 och IPv6. Iperf3 är
inte bakåtkompatibel med Iperf2.

`apt-get install iperf3`
`yum install iperf3`

### Server

Den ena noden är server och lyssnar på inkommande instruktioner. Default
är TCP/UDP 5201. För att starta iperf i server läge.

`iperf3 -s`

Daemon mode och port 5203

`iperf3 -s -D -p 5203`

**Systemd**
sudo nano /etc/systemd/system/speedtest.service

`[Unit]`
`Description=iPerf3 speed test server`
`After=network.target`

`[Service]`
`ExecStart=/usr/bin/iperf3 -s -p 5500`

`[Install]`
`WantedBy=multi-user.target`

`sudo systemctl daemon-reload`
`sudo systemctl start speedtest.service`
`sudo systemctl enable speedtest.service`

### Klient

För att starta ett test mot servern skriv.

`iperf3 -c `<ip till server>

Ställ hur länge testat ska köra. Default är 10 sekunder.

`iperf3 -c 192.168.0.20 -t 60`

Reverse mode, servern skickar till klienten.

`iperf3 -c 192.168.0.20 -R`

För att köra 5 streams samtidigt skriv.

`iperf3 -c 192.168.0.20 -P 5`

UDP kan användas för att mäta jitter och paketförlust. *Klientspecifik
växel.*

`iperf3 -c 192.168.0.20 -u`

[Category:Tools](/Category:Tools "wikilink")