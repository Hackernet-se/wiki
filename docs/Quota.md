---
title: Quota
permalink: /Quota/
---

Quotas kan användas så att användare eller en viss grupp bara får lagra
en viss mängd på ett filsystem.

Installation
------------

`apt-get install quota`

Konfiguration
-------------

Börja med att ändra i `fstab` och lägg till **usrquota** eller/och
**grpquota** på det filsystemet du vill använda det på.

`# /home was on /dev/sda6 during installation`
`UUID=9ca5cef9-f734-4396-9f29-ddaeedc21e28 /home           ext4    defaults,`**`usrquota`**`        0       2`

Mounta om filsystemet.

`mount -o remount /home`

Skapa en quota index fil. I filen sparas användarens/gruppens limit och
hur mycket utrymme som används.

`quotacheck -cum /home`

Slå av och på quotas med följande kommandon.

`quotaon /home`
`quotaoff /home`

För att sätta en quota på en användare med max limit på 1Gb skriv och
ändra: [Byte converter](http://www.whatsabyte.com/P1/byteconverter.htm)

`edquota user1`

`Disk quotas for user user1 (uid 1001):`
` Filesystem                   blocks       soft       hard     inodes     soft     hard`
` /dev/disk/by-label/DOROOT         8      `**`1000000`**`    `**`1048576`**`        2        0        0`

|            |                                                                             |
|------------|-----------------------------------------------------------------------------|
| Filesystem | Visar vilket filsystem som har quota aktiverat                              |
| blocks     | Visar hur många block som används just nu.                                  |
| soft block | Anger hur många block som får lagras innan grace perioden börjar räkna ner. |
| hard block | Anger max antal block som en användare får lagra.                           |
| inodes     | Visar hur många inodes som finns just nu.                                   |
| soft inode | Samma som **soft block** fast för inode.                                    |
| hard inode | Samma som **hard block** fast för inode.                                    |
|            |                                                                             |

**Blocks** anger hur mycket utrymme man får medans **inodes** anger hur
många filer och mappar man kan använda.

Hard block är det absoluta max en användare eller grupp kan använda når
man detta får man inget mer utrymme.

Soft block sätter en max gräns för hur mycket utrymme man har. Men man
kan lagra mer än vad soft anger under en tidsperiod som kallas **grace
period**.

Kolla quotan på en användare/grupp.

`quota user1`

Skapa en rapport som visar varje användare/grupp quota inställningar.

`repquota -a`

### Grace Period

Grace period sätter hur länge en användare får överstiga sin soft limit.
Denna inställningen är system wide och gäller för alla grupper och
användare.

`edquota -t`

Tips'N'Trix
-----------

Prova din quota genom att skapa en 1Gb fil.

`dd if=/dev/zero of=/home/$USER/DDfile bs=1M count=1024 oflag=direct`

[Category:Guider](/Category:Guider "wikilink")