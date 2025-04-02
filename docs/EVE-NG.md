---
title: EVE-NG
permalink: /EVE-NG/
---

EVE-NG (Emulated Virtual Environment New Generation) är en uppdaterad
variant av Unetlab som det tidigare hette. EVE-NG fungerar precis som
[GNS3](/GNS3 "wikilink") där man kan virtualisera sin nätverksmiljö med
routrar, brandväggar, switchar men även klienter och servrar som
Windows, [Linux](/Linux "wikilink") och [ESXi](/VMware_ESXi "wikilink").

EVE-NG är clientless så det enda som behövs är en webbläsare för att
kunna nå sina enheter.

Kolla denna
[lista](http://www.eve-ng.net/index.php/documentation/supported-images)
över vilka enheter EVE-NG har support för.

Några märken som EVE-NG har stöd för är **Cisco, Juniper, Extreme
Network, Arista, PaloAlto, VyOS, pfSense, F5, Fortigate**.

Installation
============

Tanka hem deras senaste **ova** eller **iso** från deras hemsida.

[`http://www.eve-ng.net/index.php/downloads/eve-ng`](http://www.eve-ng.net/index.php/downloads/eve-ng)

Surfa sedan in på den IP du gett EVE-NG, default username och password
är **admin/eve**

Installera images
-----------------

För att lägga in en Qemu supportad enhet så måste man döpa den på ett
specifikt sätt och ladda upp filen till **/opt/unetlab/addons/qemu/**

EVE tillhandahåller en
[lista](http://www.eve-ng.net/index.php/documentation/images-table) på
hur man ska döpa en image.

### Cumulus

Download URL: [Cumulus
VX](https://cumulusnetworks.com/products/cumulus-vx/download/)

Cumulus VX har ingen schysst device icon i EVE men det går att lägga
till själv genom att lägga png-filer i
"/opt/unetlab/html/images/icons/". Default har Cumulus VX templaten för
lite minne vilket gör att netd krashar.

`sed -i 's/= 256/= 512/' /opt/unetlab/html/templates/cumulus.php`

### [Extreme](/Network#Extreme_Networks "wikilink")

Download URL:
[EXOS-VM_v21.1.1.4-disk1.qcow2](https://stackingtool.extremenetworks.com/github/EXOS-VM_v21.1.1.4-disk1.qcow2)
Filen ska döpas till **extremexos-21.1.1.4/hda.qcow2**

Extreme Network har även lagt upp några images på deras
[GitHub](https://github.com/extremenetworks/Virtual_EXOS) som man kan
använda.

[Category:Guider](/Category:Guider "wikilink")