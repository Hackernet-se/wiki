---
title: KVM
permalink: /KVM/
---

Kernel-based Virtual Machine är en kernelmodul för hårdvaruaccelerering
och med hjälp av Quick EMUlator blir det en type-1 hypervisor. QEMU
själv är en type-2 hypervisor.

Installation
------------

*Pre-requisites Intel CPU*

`egrep '(vmx)' /proc/cpuinfo`

Installera

`dnf groupinfo virtualization`
`dnf groupinstall "Virtualization"`

Usage
=====

**GUI**

`virt-manager`

**CLI**

`virsh list`
`virsh net-list`

**Top**

`virt-top`

**OVA**
Nyare versioner av KVM/QEMU har stöd för vmdk. Packa upp och använd
sedan vmdk:n.

`tar -xf Appliance.ova`

**Kickstart**
Skapa vm med kickstartfil

`virt-install -x ks=filename.ks`

**Migration**
Requirements: CPU type, time sync, shared storage

`virsh migrate --live TestVM qemu+ssh://test2.example.com/system`

[Category:Guider](/Category:Guider "wikilink")