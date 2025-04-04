---
title: PSC
permalink: /PSC/
---

Platform Services Controller tillhandahåller gemensamma tjänster för
vSphere-miljön, däribland licensiering, certifikatshantering och
autentisering via SSO.

Arkitektur & Komponenter
------------------------

Vid installation av vCenter finns tre olika typer av deployment:

-   vCenter with External PSC – vCenter installeras standalone och
    ansluts mot en standalone PSC.
-   vCenter with Embedded PSC – vCenter och PSC deployas i samma maskin.
-   PSC Only – Standalone-installation av PSC.

PSC-gränssnittet nås via <https://IP_or_FQDN/psc>

### PSC Features

-   Hanterar och genererar SSL-certifikat till vSphere-miljön.
-   Lagrar och replikerar licensnycklar.
-   Lagrar och replikerar permissions via Global Permissions-lagret.
-   Hanterar lagring och replikering av Tags och Categories.
-   Inbyggd automatisk replikering mellan SSO-siter (om de finns).

### vCenter Single Sign-On

vCenter SSO består av Secure Token Service (STS), Administration server,
VMware Directory Service (vmdir) och Identity Management Service.

-   STS – Delar ut Security Assertion Markup Language (SAML) tokens.
    Dessa tokens representerar en användares identitet efter denne
    autentiserat genom en identitetskälla (t ex LDAP). SAML tokens
    möjliggör att användaren slipper autentisera om sig för de olika
    vCenter-tjänster som stöds av SSO.
-   Administration Server - Används för att konfigurera SSO-servern,
    initialt kan endast administrator@your_domain_name användas för
    detta. Fr o m vSphere 6.0 kan detta domännamn sättas till någon
    annat än vsphere.local, använd dock inte samma namn som din AD-
    eller OpenLDAP-domän.
-   VMware Directory Service (vmdir) - vmdir är den katalogtjänst som
    associeras med SSO-domänen som skapas vid deployment. I miljöer med
    flera PSC:er propageras förändringar i en vmdir-instans till övriga
    instanser. Vmdir lagrar förutom vCenter SSO-information även
    certifikatsinformation. PSC Sites kan även skapas i vmdir, en logisk
    container för gruppering av PSC-instanser i en SSO-domän.
-   Identity Management Service – Hanterar identitetskällor och STS
    authentication requests.

Med hjälp av SSO kan de olika komponenterna i vSphere kommunicera med
varandra genom samma secure token-mekanism. I vCenter SSO autentiseras
mänskliga användare via AD eller OpenLDAP, medan solution users
autentiseras med hjälp av certifikat.

### Användare (SSO)

För att lägga till/ta bort/aktivera/inaktivera SSO-användare gå till
**Administration** -\> **SSO** -\> **Users and groups** -\> Högerklicka
på användaren -\> **Edit**/**Disable**/**Enable**/**Unlock**.

### Grupper (SSO)

Administrators – Globala rättigheter till SSO och hela inventoryt.
CAAdmins – Kan managera VMCA.
LicenseService.Administrator - Kan managera licenser.

### SSO Policies

Policies för Passwords, Lockout och Tokens hanteras via **Home** -\>
**Administration** -\> **SSO** -\> **Configuration** -\>
**Policies**-fliken. För att t ex ändra till att lösenord aldrig upphör,
editera Password Policy:n och sätt Maximum lifetime till 0.

### VMware Certificate Authority (VMCA)

VMCA tillhandahåller och provisionerar alla nödvändiga certifikat för
vCenter och ESXi, och är en del av PSC. VMware rekommenderar att
antingen använda default-inställningarna, dvs att VMCA hanterar alla
certifikat, eller VMCA default certificates med externa SSL-cert; Hybrid
Mode. Hybrid mode innebär att PSC och vCenter-certifikaten byts ut och
att VMCA får hantera certifikat för solution users och ESXi-hostar.
VMware Endpoint Certificate Store (VECS) kallas det repository där alla
custom-certifikat lagras. Om custom-certifikat på ESXi-hostar ska
användas, lagras de lokalt på hosten, inte i VECS.

För att se vilka certifikat som används av vCenter, gå till **Home** -\>
**System Configuration** -\> **Nodes** -\> **vCenter-noden** -\>
**Manage** -\> **Certificate Authority**. Om du inte har tillgång till
denna vy, lägg till din användare i CAAdmins-gruppen.

### Licenshantering

Licenshantering i vSphere-miljön hanteras av VMware License Service, en
del av PSC.

Deployment
----------

Det finns flera olika sätt att koppla samman vCenter och PSC.

### Embedded Linked Mode

En topologi med flera vCenter Appliance:r, tillkom i 6.5U2, Windows
Embedded PSC är inte supporterad för detta. Embedded Linked Mode
möjliggör Enhanced Linked Mode mellan två eller flera (upp till 15) VCSA
med Embedded PSC. Om vCenter HA används anses de tre noderna som en
logisk vCenter-nod. Denna deployment förenklar backup & restore, då
färre steg behöver genomföras. PSC HA förenklas också avsevärt, då
behovet av lastbalanserare för PSC försvinner. Embedded Linked Mode kan
endast aktiveras under installation av VCSA, inte efteråt.

### Enhanced Linked Mode

Enhanced Linked Mode länkar samman flera vCenter samt en eller flera
PSC:er (ej embedded). Upp till 10 VCSA eller 8 Windows vCenter kan
anslutas i en grupp. Anslutningen sker under installation, inte efter.

Utan lastbalanserare – I en deployment utan LB måste manuell failover
till nästa PSC utföras i vCenter. Först avregistreras nuvarande PSC med
`cmsso-util unregister`, sedan pekas vCenter om med
`cmsso-util repoint-psc`. Om din topoplogi innehåller tre eller flera
PSC:er kan en ringtopologi konfigureras för att garantera tillgänglighet
då en instans fallerar. Detta görs genom att köra
`/usr/lib/vmware-vmdir/bin/vdcrepadmin -f createagreement` på den första
och sista PSC-instansen som deployats.

Med lastbalanserare – Om LB används mellan vCenter(s) och PSC:erna sker
failover automatiskt om en PSC blir oresponsiv. Detta kräver att alla
PSC:er är antingen Appliance- eller Windows-baserade.

### Multi-Site PSC-installation

I grova drag är det man behöver utföra: Installera PSC först, sedan
vCenter som kopplas mot PSC. För flera PSC:er och vCenter; återupprepa
tidigare steg. Alla efterföljande appliance:r efter den första PSC:en
måste deployas med "Join an existing vCenter SSO Domain". Då blir
PSC:erna replication partners och vCenter:na ansluts mot SSO-domänen.

Topologin kan ändras efter installation, från embedded till external
(eller vice versa), så länge SSO-domänen inte ändras. En extern PSC bör
användas då fler än en lösning med SSO-integration används, t ex vCenter
+ vRealize Automation.

Nedan KB listar supporterade (även deprecated) topologier för PSC
deployment: <https://kb.vmware.com/kb/2147672>

### Uppgradera PSC

Om extern PSC används måste alla PSC-instanser uppgraderas i sekvens.
Efter detta är gjort kan VCSA uppgraderas.

[Category:VMware](/Category:VMware "wikilink")