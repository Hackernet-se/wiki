---
title: Docker
permalink: /Docker/
---

Docker är ett open source-projekt som automatiserar utrullning av
applikationer i containers genom att lägga ett extra lager av
abstraktion och automatisering av virtualisering på Linux. Docker
använder resursisoleringsfunktioner i Linuxkärnan, såsom cgroups och
kernel namespace för att tillåta oberoende "containers" att köra i en
och samma Linuxinstans. Detta minskar overhead jämfört med virtuella
maskiner.
Mer info: <http://www.nkode.io/2014/08/24/valuable-docker-links.html>

Installation
------------

Fedora 23

`sudo dnf -y install docker-io`

Ubuntu 14.04

`sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9`
`sudo sh -c "echo deb `[`https://get.docker.com/ubuntu`](https://get.docker.com/ubuntu)` docker main > /etc/apt/sources.list.d/docker.list"`
`sudo apt-get update && sudo apt-get -y install lxc-docker`

**Alternativt**

`wget -qO- `[`https://get.docker.com/`](https://get.docker.com/)` | sh`

### Starta

`sudo docker daemon &`

Add user till grupp

`sudo usermod -aG docker $(whoami)`

Imagehantering
--------------

Snapshots av containers eller OS-images, t.ex. ubuntu

`sudo docker search ubuntu`
`sudo docker pull ubuntu`

Visa tillgängliga images

`sudo docker images`

Starta en container utifrån en image.

`docker run -i -t ubuntu /bin/bash`

För att spara det man har gjort i en image måste man commita

`sudo docker commit [container ID] [image name]`

Remove image

`docker image ls`
`docker rmi `<IMAGE ID>

Containerhantering
------------------

Kolla aktiva och inaktiva containers.

`sudo docker ps`
`sudo docker ps -l`

Starta och stoppa en container.

`sudo docker run [container ID]`
`sudo docker stop [container ID]`

Öppna ett bash skal i en container

`sudo docker exec -it [container namn] bash`

Starta och stoppa alla containers:

`docker stop $(docker ps -aq)`
`docker start $(docker ps -aq)`

Ta bort alla containers:

`docker rm $(docker ps -aq)`

Ta bort alla images:

`docker rmi $(docker images -q)`

Inspect
-------

Med docker inspect kan man få ut info om images och containers. T.ex.
IP-adresser, hostname, kommentarer mm.

`docker inspect myself/myimage`
`docker inspect container-id`
`docker inspect --format "{{ .NetworkSettings.IPAddress }}" $(docker ps -q)`

Clean up
--------

Städa bort alla stoppade containrar, oanvända networks, dangling images
samt dangling build cache.

`docker system prune`

För att även ta bort alla unused images.

`docker system prune -a`

Dockerfile
----------

`nano Dockerfile`
`sudo docker build -t my_test .  `

registry.hub.docker.com
-----------------------

Docker Hub är en central punkt för Docker, där hostas offentliga
images.
Vill man ladda upp det man har gjort måste man först regga sig på
hemsidan. Sedan kan man pusha imagear.

`sudo docker push username/imagename`

Central hantering
-----------------

Central Dockerhantering gör det möjligt att managera images, containers,
hostar och övriga Dockerresurser från ett och samma ställe. Exempel på
detta är [Shipyard](/Shipyard "wikilink"), Swarm och
[Rancher](/Rancher "wikilink")

Network
-------

Fr.o.m version 1.9 finns *docker network*. Nu använder man Docker Engine
för att skapa virtuella nätverk som kan spänna över flera hostar.
Overlay görs med VXLAN.

`docker network --help`
`docker network ls`

Default finns det 3 nätverk.
**Host mode:** containern kopplas till samma L2-domän som hosten.

`docker run -d --name webb1 --net=host`

**Bridge mode:** (default) containern hamnar bakom hostens ip och man
kan portforwarda.

`docker run -d --name webb1 -p 8081:80`

**None mode:** inget nätverk.

`docker run -d --name webb1 --net=none`

New bridge network

`docker network create --driver=bridge --subnet=192.168.100.0/24 --gateway=192.168.100.1 --ip-range=192.168.100.128/25 testbridge`

IP-adresser till containerar allokeras från rangen.

`docker network connect testbridge webb1`

### Overlay

`docker network create -d overlay --subnet=10.10.0.0/24 testoverlay`

[Category:Guider](/Category:Guider "wikilink")