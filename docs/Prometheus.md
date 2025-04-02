---
title: Prometheus
permalink: /Prometheus/
---

[Category:Guider](/Category:Guider "wikilink")

Prometheus is a an open source monitoring and alerting toolkit.
Originally built by a couple of Soundcloud engineers to modernize
monitoring.The core of Prometheus is a data model with time series data
identified by metric name and key/value pairs and stored in a time
series database.

Prometheus also includes:

-   a flexible query language to leverage this dimensionality
-   no reliance on distributed storage; single server nodes are
    autonomous
-   time series collection happens via a pull model over HTTP
-   pushing time series is supported via an intermediary gateway
-   targets are discovered via service discovery or static configuration
-   multiple modes of graphing and dashboarding

Hackernets Setup
----------------

We are using a fairly simple setup with all prometheus components
running in docker containers. Since Prometheus relies on pulling metrics
via HTTP the data gathering and conversion to the correct metric format
has to be done by components outside of Prometheus. We currently use
different projects to gather data, but writing your own applications is
very easy considering the extensive amount of language support that the
Prometheus project has to offer.

**Our containers:**

``` bash
[root@prometheus ~]# docker ps
CONTAINER ID        IMAGE                COMMAND                  CREATED             STATUS              PORTS                    NAMES
7e22a6c7bbc4        vmware_exporter      "/opt/vmware_exporte…"   8 days ago          Up 8 days           0.0.0.0:9272->9272/tcp   vmware_exporter
67c5bfbaa81b        blackbox_exporter    "/bin/blackbox_expor…"   9 days ago          Up 8 days           0.0.0.0:9115->9115/tcp   blackbox_exporter
c77043cc77fe        grafana/grafana      "/run.sh"                9 days ago          Up 8 days           0.0.0.0:80->3000/tcp     grafana
463e5b3663c7        prom/prometheus      "/bin/prometheus --c…"   2 weeks ago         Up 8 days           0.0.0.0:9090->9090/tcp   prometheus
809f4ab916c9        prom/node-exporter   "/bin/node_exporter"     2 weeks ago         Up 8 days           0.0.0.0:9100->9100/tcp   node_exporter
```

Node Exporters
--------------

### pfSense

Följande är veriferat på pfsense 2.4.2 som kör FreeBSD 11.1. Ändra till
**yes** i följande 3 filer:

`vi /usr/local/etc/pkg/repos/FreeBSD.conf`
`vi /usr/local/etc/pkg/repos/pfSense.conf               `
`vi /etc/pkg/FreeBSD.conf`

Installera sedan **node_exporter**

`pkg install node_exporter`

Lägg sedan till så node_exporter startar vid omboot.

`echo "node_exporter_enable="YES"" >> /etc/rc.conf`

Starta sedan tjänsten:

`service node_exporter start`

Exportern går att nå på default porten 9100.

### Linux

``` Bash
sudo useradd --no-create-home --shell /bin/false node_exporter && \
wget https://github.com/prometheus/node_exporter/releases/download/v0.18.1/node_exporter-0.18.1.linux-amd64.tar.gz && \
tar -xf node_exporter-0.18.1.linux-amd64.tar.gz && sudo cp node_exporter-0.18.1.linux-amd64/node_exporter /usr/local/bin/ && \
sudo chown node_exporter:node_exporter /usr/local/bin/node_exporter && rm -rf node_exporter-0.18.1.linux-amd64* && \
sudo bash -c "cat <<__EOF__>> /etc/systemd/system/node_exporter.service
[Unit]
Description=Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
__EOF__"
sudo systemctl daemon-reload && sudo systemctl start node_exporter && sudo systemctl enable node_exporter
```