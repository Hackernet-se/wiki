---
title: VM Encryption
permalink: /VM_Encryption/
---

VM Encryption sker i hypervisorn, "under" den virtuella maskinen. VM
Encryption är helt agnostiskt, Guest OS eller datastore-typ spelar ingen
roll. Krypteringen aktiveras via Storage-policy. De filer som krypteras
är:

-   VM-filer (VSWP, VMSN mfl)
-   VM-diskfiler
-   Host core dumps

Filer som inte krypteras:

-   Loggfiler
-   VM-konfigurationsfiler (VMX, VMSD)
-   Descriptor-filer för virtuella diskar (innehåller dock en krypterad
    bundling av nycklar)

### Requirements

För att aktivera VM Encryption måste Host Encryption mode vara påslaget,
detta ska oftast ske automatiskt, men kan explicit aktiveras. Detta görs
via **Host** -\> **Configure** -\> **System** -\> **Security Profile**
-\> välj **Host Encryption Mode** -\> **Edit** -\> sätt till
**Enabled**. Under tiden en VM krypteras måste även minst lika mycket
ledig diskyta på datastore:t finnas som VM:en förbrukar.

### KMS-server för VM Encryption

Förutsatt att en (tredjeparts) KMS-server finns tillgänglig:

1.  Lägg till den via **vCenter-noden** -\> **Configure** -\> **More**
    -\> **Key Management Server** -\> Tryck på plustecknet med texten
    **Add KMS** bredvid.
2.  Skapa ett nytt kluster, fyll i infon som efterfrågas.
3.  Sätt klustret som default KMS Cluster.
4.  Klicka på Trust i Trust Certificate-rutan för att acceptera Trust:en
    mot KMS.

Om KMS-servern är korrekt konfigurerad kan du verifiera detta genom att
titta på Connection Status, en grön bock visar detta (=Normal).

KMS-servern är den som hanterar kryptering av VMs, vCenter är endast
klient till KMS-servern. Om man inte vill att alla administratörer ska
ha tillgång till management av VM Encryption kan man använda den nya
default-rollen **No Cryptography Administrator**.

### Encryption Storage Policy

Efter anslutningen mot KMS upprättats kan man skapa sin Encryption
Storage Policy. Behörighetsmässigt krävs även *Cryptographic
operations.Manage encryption policies*-behörigheten. Policyn skapas via
**Home** -\> **Policies and Profiles** -\> **VM Storage Policies** -\>
**Create VM Storage Policy**.

1.  Följ wizarden, sätt namn m.m.
2.  Bocka för **Use common rules in the VM storage policy**.
3.  Tryck på **Add component**, välj **Encryption** -\> **Default
    Encryption Properties** och sedan **Next** (Defaults räcker oftast
    om policyn inte skall innefatta andra funktioner, t ex caching eller
    replikering).
4.  Bocka ur **Use rule-sets in the storage policy**, välj **Next**.
5.  På **Storage compatibility**-sidan, låt **Compatible** vara förvalt,
    välj ett datastore och sedan **Next**.
6.  Verifiera alla settings och tryck **Finish**.

Den virtuella maskinen kan krypteras för sig medan diskarna kan lämnas
okrypterade, då man endast applicerar Encryption Storage Policy:n på VM
Home och inte på diskarna. Krypterade diskar kan däremot inte användas
av en okrypterad VM. [Category:VMware](/Category:VMware "wikilink")