---
title: Multiarch
permalink: /Multiarch/
---

Multipla architekturer kan vara bra att använda om du finner att ett
program eller library du behöver inte finns i t.ex. 32 bitars men du
vill köra 64 bitars på servern

"dpkg --print-foreign-architectures" Listar arktikturer som du kan lägga
till "dpkg --add-architecture i386" lägger till i386 som en extra
kategori Sen är det bara att göra apt-get update som vanligt så ska du
kunna installera libs och program för den andra arkitekturen.

I vanliga fall kommer då det du vill installera installeras i din
standard arktiektur om du istället vill tvinga det till en speciel
arkitektur så kör du istället t.ex. "apt-get install apache2:i386"

Du kan ta bort multiarchs med "dpkg --remove-architecture i386"

Ett vanligt fel meddelande som kommer upp när man försöker köra en fil
men inte har rätt arkitektur är "No such file or directory"

[Category:Guider](/Category:Guider "wikilink")