---
title: VSphere Permissions
permalink: /VSphere_Permissions/
---

Access Control
--------------

vSphere erbjuder detaljerad behörighetskontroll med hjälp av
permissions. Behörigheterna specificeras med hjälp av roles, som kan
bestå av flera privileges. En permission har tre beståndsdelar; en role
(innehållandes privileges), som tillsammans med en användare/grupp
mappas mot ett objekt.

När en permission tilldelas får man välja om den ska propagera nedåt i
hierarkin. Propageringen ställs inte in universellt, utan för varje
tilldelad permission. Permissions som appliceras på child-objekt
överskrider alltid en permission som propagerats från parent-objekt,
dock kan enbart en permission explicit appliceras på ett objekt per
användare/grupp. Då två permissions ärvs till samma objekt, t ex vid en
kombination av arv från VM Folder och Resource Pool, kombineras de. Om
en användare är medlem i flera grupper som har olika Permissions på ett
objekt kan två saker hända:

-   Om inga permissions definierats för användaren direkt på objektet
    appliceras de behörigheter som grupperna medför.
-   Om en permission definierats för användaren på objektet, tar den
    företräde över alla gruppbehörigheter (även de som ärvts).

För att se vilka permissions som applicerats på ett objekt går man till
vSphere-objektet -\> **Permissions**-fliken, sedan tittar man i "Defined
In"-kolumnen. Ifrån denna vy kan även en lista över permissions
exporteras.

För att lägga till/modifiera/ta bort permissions går man till: **Home**
-\> **Administration** -\> **Access Control** -\> **Roles**

### ESXi Local Host Permissions

Standalone-hostar har tre fördefinierade roles som kan användas för att
tilldela permissions. Dessa är **Administrator**, **Read Only** och **No
Access**.

vCenter Server Permissions
--------------------------

vCenter Permissions appliceras på objekt i objekthierarkin.

### Global Permissions

Global permissions appliceras på ett globalt rotobjekt som sträcker sig
över olika lösningar, t ex kan permission tilldelas en användare/grupp
som ger läsrättigheter både i vCenter och vRealize Orchestrator. Om inte
propagering för en Global Permission slås på kommer användaren/gruppen
inte få tillgång till objekten i hierarkin, utan enbart ett fåtal
globala funktioner, t ex att skapa Roles.

### vSphere.local group membership

Medlemmar i vSphere.local-grupper kan utföra vissa saker, t ex
licenshantering. Dessa grupper gäller också för administration av PSC.

### Identity Sources

Det finns fyra supporterade identitetskällor som kan läggas till i
vCenter (PSC):

-   Active Directory
-   Active Directory over LDAP
-   OpenLDAP (flera implementationer stöds)
-   LocalOS (lokala användare på PSC:n)

vCenter Single Sign-On system users finns också, denna källa skapas och
läggs till automatiskt när vCenter SSO installeras. Om Active Directory
ska användas som identitetskälla måste vCenter-servern först bli medlem
i domänen. Detta görs under **Administration** -\> **Deployment** -\>
**System Configuration** -\> **Nodes**, välj vCenter-servern i listan.
Sedan under **Manage**-fliken -\> **Settings** -\> **Advanced** -\>
**Active Directory**, klicka på "**Join...**"-knappen.

### Permission Validation

Som standard valideras alla användare och grupper var 1440:e minut
(24h), om en användare tagits bort eller bytt namn tas alla permissions
relaterade till denne bort vid nästa validering.

### System Roles kontra Sample Roles

System & Sample Roles finns per default, det som skiljer dem åt är att
System Roles inte går att editera eller ta bort, endast kloning är
möjlig.

De System Roles som finns är följande: Administrator, No Cryptography
Administrator, No Access och Read Only.

De fördefinierade Sample Roles är: Virtual Machine Power User, Virtual
Machine User, Resource Pool Administrator, VMWare Consolidated Backup
User, Datastore Consumer, Network Administrator, Content Library
Administrator

[Category:VMware](/Category:VMware "wikilink")