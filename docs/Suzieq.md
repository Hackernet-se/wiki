---
title: Suzieq
permalink: /Suzieq/
---

Suzieq är ett open-source multi-vendor network observability tool som
man kan använda för att analysera ett nätverk med hjälp av olika
queries. Det finns stöd för Arista, Cisco, Juniper mm.

Skapa ett device inventory, t.ex. /home/USER/suzieq_inventory.yml.

``` yaml
sources:
- name: device_list
  hosts:
    - url: ssh://10.1.0.10
    - url: ssh://10.1.0.11
    - url: ssh://10.1.0.12

auths:
- name: svc
  username: svc-readonly
  password: password123

devices:
- name: nxos
  devtype: nxos
  ignore-known-hosts: true

namespaces:
- name: oob
  source: device_list
  auth: svc
  device: nxos
```

Sätt upp Suzieq med [Docker](/Docker "wikilink")

``` Bash
docker volume create suzieq-storage
docker run -itd --rm -p 8501:8501 -e TZ=Europe/Stockholm \
  -v suzieq-storage:/suzieq/parquet \
  -v /home/USER/suzieq_inventory.yml:/suzieq/inventory/suzieq.yml \
  --name suzieq netenglabs/suzieq:latest

docker attach suzieq

sq-poller -I /suzieq/inventory/suzieq.yml &
suzieq-gui &
```

Webgui når man sedan på port 8501.

[Category:Network](/Category:Network "wikilink")