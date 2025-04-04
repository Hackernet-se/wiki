---
title: Dd
permalink: /Dd/
---

dd är verktyp som går att använda för diverse ändamål.

Skriva över en disk med nollor

`dd if=/dev/zero of=/dev/sda bs=1M status=progress`

Vissa dd-operationer kan ta lång tid och det finns olika sätt att kolla
progress. T.ex. kan man följa det med hjälp av watch-kommandot (i en ny
session om man inte la till &-tecken efter dd-kommandot).

`watch 'killall -USR1 dd'`

Default intervallet för watch är 2 sekunder, detta går att ställa själv.

Prestandatester
---------------

Följande exempel är simpla prestandatester som inte säger allt men
fungerar som en fingervisning.

### Disk/share

Write

`dd if=/dev/urandom of=/home/$USER/DDfile bs=1M count=4096 oflag=direct #urandom flaskar`
`dd if=/dev/`[`frandom`](/frandom "wikilink")` of=/home/$USER/DDfile bs=1M count=4096 oflag=direct`

`dd if=/dev/zero of=/home/$USER/DDfile bs=1M count=4096 oflag=direct`

Istället för oflag=direct kan conv=fdatasyn användas.

Read
*Cachning kan behövas stängas av vid readtesterna.*

`dd if=/home/$USER/DDfile of=/dev/null bs=1M count=4096 iflag=direct`

Med detta exemplet skapas det en 4GB stor fil, glöm inte ta bort den
efteråt.

### CPU

`dd if=/dev/zero bs=1M count=1024 | sha512sum`

[Category:Tools](/Category:Tools "wikilink")