---
title: IPXE
permalink: /IPXE/
---

iPXE är en open source network boot firmware. Funkar precis som vanliga
PXE fast med en del extra features som:

-   Boota från web server via HTTP.
-   Boota från ett iSCSI SAN, AoE SAN eller Fibre channel SAN via FCoE.
-   Boota från Wi-Fi eller WAN koppling.
-   Boota från ett Infiniband nätverk.
-   Kontrollera boot processen med hjälp av script.

Man kan flasha in iPXE ROM filen på sitt nätverkskort. Vill man inte det
kan man ladda iPXE över TFTP med PXE. Se även
[PXE-Deploy](/PXE-Deploy "wikilink")

Förberedelse
============

För att kunna bygga iPXE från source koden behövs följande paket:

-   gcc (version 3 or later)
-   binutils (version 2.18 or later)
-   make
-   perl
-   syslinux (for isolinux, only needed for building .iso images)
-   liblzma or xz header files
-   zlib, binutils and libiberty header files (only needed for EFI
    builds)

Installation
============

Ladda hem senaste source koden från GIT.

`git clone `[`git://git.ipxe.org/ipxe.git`](git://git.ipxe.org/ipxe.git)` && cd ipxe/src`
`make`

Bootbar ISO
-----------

iPXE har en egen [bootbar ISO](http://boot.ipxe.org/ipxe.iso) om man
vill prova snabbt och enkelt.

VMware
------

Du kan byta ut VMwares PXE rom med iPXE.

iPXE har stöd för följande vmware nics.

| VMware name | iPXE driver name | PCI vendor:device IDs | iPXE ROM image |
|-------------|------------------|-----------------------|----------------|
| e1000       | intel            | 8086:100f             | 8086100f.mrom  |
| e1000e      | intel            | 8086:10d3             | 808610d3.mrom  |
| vlance      | pcnet32          | 1022:2000             | 10222000.rom   |
| vmxnet      | (not supported)  | 15ad:0720             |                |
| vmxnet3     | vmxnet3          | 15ad:07b0             | 15ad07b0.rom   |

Börja med att välja en av dom supportade nics genom att ändra följande
rad i din **.vmx** fil.

`ethernet0.virtualDev = "e1000"`

Ladda hem source koden och bygg filerna med följande kommando.

`git clone `[`git://git.ipxe.org/ipxe.git`](git://git.ipxe.org/ipxe.git)` && cd ipxe/src`
`make bin/8086100f.mrom bin/808610d3.mrom bin/10222000.rom bin/15ad07b0.rom`

Kopiera sedan över följande filer **8086100f.mrom, 808610d3.mrom,
10222000.rom** och **15ad07b0.rom** till din vmware server och lägg dom
på tex ett datastore.

Lägg sedan till följande rader i din **.vmx** fil.

`ethernet0.opromsize = 262144`
`e1000bios.filename = "/path/to/datastore/8086100f.mrom"`
`e1000ebios.filename = "/path/to/datastore/808610d3.mrom"`
`nbios.filename = "/path/to/datastore/10222000.rom"`
`# nxbios.filename = ""`
`nx3bios.filename = "/path/to/datastore/15ad07b0.rom"`

[Category:Guider](/Category:Guider "wikilink")