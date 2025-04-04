---
title: Hdparm
permalink: /Hdparm/
---

hdparm är ett verktyg för att managera hårdvaruparametrar på hårddiskar.
T.ex. GParted inkluderar hdparm.

Info om hårddisk

`hdparm -i /dev/sda`

Läsprestandatest

`hdparm -tT /dev/sda`

Sänk ljudnivån på bekostnad av prestanda.

`hdparm -M 128 /dev/sda`

Fabriksåterställning

`hdparm --yes-i-know-what-i-am-doing --dco-restore /dev/sda`

[Category:Tools](/Category:Tools "wikilink")