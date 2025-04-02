---
title: VMware vCenter
permalink: /VMware_vCenter/
---

vCenter är en central manage server för alla dina ESXi hostar. Det är
med vCenter du får funktioner som HA. Det krävs ett VMware konto för att
kunna ladda hem vCenter och sedan en licens för att kunna använda längre
än 60 dagar.

Installation
------------

Enklaste sättet att få igång vCenter är att ladda hem vmwares appliance
från vmware och deploya den på en esxi host.
VCSA 6.0, vCenter Server Appliance, finns inte längre som .ovf utan man
laddar hem iso.

Konfiguration
-------------

Den mesta konfiguration sker med hjälp av vmwares klient eller vmware
webui.

### Första gången

-   Default användarnamn och lösenord på vmwares appliance är,

`root/vmware`

-   Börja med att öppna en console och logga in. Kör scriptet under för
    att sätta ip, hostnamn, gw, dns.

`/opt/vmware/share/vami/vami_config_net`

-   Surfa sedan in på <https://><ip>:5480, här görs den initiala
    setupen.
-   All datacenter och klustermanagering görs sedan från:
    <https://><ip>:9443

### LDAP koppla vCenter

-   Logga in som administrator@vsphere.local (Default lösenord är
    vmware)
-   Gå till
    `Administration > Single Sign-On > Configuration > Identity Sources`.
    Tryck på det gröna plustecknet.

`Om inte Single Sign-On finns under Administration så är du antagligen inloggad som användaren root.`

-   Fyll sedan i dina uppgifter och tryck på "Test connection".


För att kunna se Single sign-on under Administration och göra ändringar
behöver man lägga till sin användare eller en grupp i Administrators.

-   Gå till `Users and Groups > Groups`. Lägg till en användare eller en
    grupp i **Administrators** gruppen. Dettaa har inget med
    rättigheterna mot VM's.


\* För att styra rättigheter för vad en användare får göra gå till
`Administration > Access Control > Roles` Tryck på gruppen Administrator
och sedan klicka på vCenterns hostnamn.

-   Under vCenterns `Manage > Permissions` Sätter man permissions för
    vilka användare och grupper som får göra vad på servern.

### Enable SCP

För att kunna SCP'a filer till vCenter skriv följande:

`chsh –s /bin/bash`

Då ändrar man login skalet från **appliancesh** till **bash** och kan då
SCP filer.

För att ändra tillbaka till vanliga skriv:

`chsh -s /bin/appliancesh`

VMware Client Integration Plugin
--------------------------------

Behövs för att kunna öppna console eller logga in med sitt windows
login. Länk till pluginet finns längst ner på
<https://><vCenterip>:9443.

### Chrome NPAPI

Pluginet använder sig av NPAPI(Netscape Plugin Application Programming
Interface). Chrome valde i version 42 att stänga av stödet för NPAPI och
kommer i version 45 att ta bort NPAPI helt från webbläsaren.

Tills dom tagit bort NPAPI kan man aktivera pluginet igen med denna
länken,

[`chrome://flags/#enable-npapi`](chrome://flags/#enable-npapi)

#### Chrome 45

Nu får man installera ett CIP-paket för att få samma funktionalitet,
detta använder inte NPAPI.

[`http://vsphereclient.vmware.com/vsphereclient/2/9/9/4/0/4/1/VMware-ClientIntegrationPlugin-6.0.0.exe`](http://vsphereclient.vmware.com/vsphereclient/2/9/9/4/0/4/1/VMware-ClientIntegrationPlugin-6.0.0.exe)

VMware Remote Console
---------------------

VMware Remote Console(VMRC) togs fram efter att Chrome valde att ta bort
stödet för NPAPI. VMRC är ett standalone program för Windows och Mac OS
och används tillsamans med VMware vSphere Web Client det följer med
vCenter Server 5.5U2b och senare.

För att ladda hem och starta VMCR i vSphere 5.5 och 6.0 så har två nya
länkar lagts till på varje VM's status sida.

**vSphere 5.5** heter länkarna **Open with VMRC** och **Download VMCR**

**Vsphere 6.0** heter länkarna **Launch Remote Console** och **Download
Remote Console**

Ändra Login UI
--------------

I vCenter 6.0 går det att göra om sitt LoginUI tex lägga till en egen
bild. Det finns 2 filer som man kan ändra i, det är **unpentry.jsp** och
**login.css**. I mappen **img** kan du lägga bilder och referera till
dom i koden.

[Hackernet's egna Login
UI](https://github.com/Hackernet-se/vmware-custom-login)

**VCSA 6.0**

`/usr/lib/vmware-sso/vmware-sts/webapps/websso/WEB-INF/views/unpentry.jsp`
`/usr/lib/vmware-sso/vmware-sts/webapps/websso/resources/css/login.css`
`/usr/lib/vmware-sso/vmware-sts/webapps/websso/resources/img`

**Windows vCenter Server 6.0**

`C:\ProgramData\VMware\vCenterServer\runtime\VMwareSTSService\webapps\websso\WEB-INF\views`
`C:\ProgramData\VMware\vCenterServer\runtime\VMwareSTSService\webapps\websso\resources\css`
`C:\ProgramData\VMware\vCenterServer\runtime\VMwareSTSService\webapps\websso\resources\img`

Regenerate certificates
-----------------------

För att skapa nya cert eller lägga in ett eget cert från tex [Let's
Encrypt](/Let's_Encrypt "wikilink") så använder man certificate manager.

`/usr/lib/vmware-vmca/bin/certificate-manager`

Reset the VMware vCenter Single Sign-On administrator password
--------------------------------------------------------------

Om man glömt sitt lösenord till en användare tex
Administrator@vSphere.local kan man skapa ett nytt.

`/usr/lib/vmware-vmdir/bin/vdcadmintool`

-   Välj nr 3: **Reset account password**
-   Ange följande som UPN: '''Administrator@vSphere.

[Category:VMware](/Category:VMware "wikilink")
[Category:Guider](/Category:Guider "wikilink")