---
title: Lenovo BIOS update
permalink: /Lenovo_BIOS_update/
---

[Category:Hardware](/Category:Hardware "wikilink") Ladda ner senaste
BIOS versionen för din x220a @
<http://support.lenovo.com/us/en/products/laptops-and-netbooks/thinkpad-x-series-laptops/thinkpad-x220/downloads/>
(I mitt fall så laddade jag ner "8duj25us.iso" )

### Själva processen för att skapa imagefilen:

För att extrahera boot imagen så använder man sig av ett perlscript vid
namn "geteltorito"

*`wget`` `[`http://www.uni-koblenz.de/~krienke/ftp/noarch/geteltorito/geteltorito.pl`](http://www.uni-koblenz.de/~krienke/ftp/noarch/geteltorito/geteltorito.pl)*

\- (Ställ dig i den map där både .iso filen samt geteltorito
perlscriptet ligger)

*`perl`` ``geteltorito.pl`` ``8duj25us.iso`` ``>`` ``biosupdate.img`*

Man skall kunna föra över imagefilen till usbminnet enligt följande:
''sudo dd if=biosupdate.img of=/dev/sdb1 bs=512K ''

I mitt fall blev filerna korrupta och behövde istället föra över imagen
till en windowsmiljö och använde '''"win32 disk imager" '''för att fixa
till det.

In med USB minnet i laptopen, kör F12 vid boot och boota från USB
minnet.

Source:
<http://forums.lenovo.com/t5/Linux-Discussion/SUPPORT-REQUEST-X220-BIOS-UPDATE-INSTRUCTIONS-USB/td-p/532077>