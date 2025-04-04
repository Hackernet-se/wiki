---
title: ESXi Security
permalink: /ESXi_Security/
---

ESXi Security Hardening
-----------------------

Trots att vSphere 6.5 kommit med många förbättringar på säkerhetssidan
finns det en hel del att göra för att öka säkerheten på dina ESXi:er.

### Host Profiles

Även om de inte ökar säkerheten i sig, är de ett väldigt bra verktyg att
använda för att nå eventuella säkerhetskrav. En Host Profile kan ses som
en mall som appliceras på en ESXi-host och ändrar de definierade
inställningarna i profilen, däribland säkerhetsinställningar.

För att slå på en Host Profile: **Cluster** -\> **Manage** -\>
**Settings** -\> **Configuration** -\> **Profiles**, tryck på
"**Attach...**"

### Security Profile (Firewall & Services)

Tillåt endast nödvändiga tjänster när de används, t ex SSH. För att
ändra en brandväggsregel/tjänst: **Host** -\> **Configure** -\>
**System** -\> **Security Profile**.

En brandväggsregel i ESXi avgör vilka inkommande/utgående portar och
protokoll som används för en tjänst, samt status på Daemon:en i ESXi.
Vissa tjänster går även att starta/stoppa/starta om via Security
Profile. Startup Policy går också att ändra, detta avgör ifall tjänsten
startar samtidigt som ESXi, när porten är öppen, eller manuellt.

### Managed Object Browser

MOB används för att utforska objektmodellen i ESXi, vilket kan användas
för att utföra skadliga konfigurationsändringar. Sedan 6.0 är MOB
avstängt som standard, men behövs för bla att extrahera gamla
certifikat. MOB slås av/på via Advanced System Settings på en Host,
värdet som ändras är `Config.HostAgent.plugins.solo.enableMob`

Lockdown Mode
-------------

Lockdown mode är en säkerhetsfunktion som stänger av lokal management på
ESXi-hostar; management kan enbart ske via vCenter (utantag finns). Det
finns två olika lägen, normal och strict lockdown.

#### Normal Lockdown

DCUI körs fortfarande på hosten. Priviligerade konton kan fortfarande
logga in och stänga av Lockdown. Bara de konton med administrativ
behörighet som specificerats i Exception User-listan för Lockdown kan
göra detta. Exception Users är också till för service-konton som behöver
utföra specifika tasks direkt på hosten. Det finns även en advanced
option (DCUI.Access), som ger en användare (även icke-admins)
möjligheten att logga på DCUI och stänga av Lockdown Mode.

#### Strict Lockdown

DCUI-tjänsten stoppas; om kommunikationen till vCenter försvinner och
inte kan återupprättas finns ingen annan utväg än ominstallation. Dock
finns det ett sätt att förebygga detta, om SSH och/eller ESXi Shell
aktiverats på hosten. Då kan en admin-användare på Exception User-listan
logga på hosten via CLI:t.

#### Aktivera Lockdown

För att slå på Lockdown Mode: **Host** -\> **Configure** -\> **System**
-\> **Security Profile** -\> "**Edit**"-knappen under **Lockdown Mode**,
välj sedan **Enable**.

När Lockdown Mode slås på termineras alla sessioner för de användare som
inte är med på Exception User-listan.

SSH/DCUI/Shell Access
---------------------

Dessa tre tjänster går att slå av manuellt via **Host** -\>
**Configure** -\> **System** -\> **Services**. SSH och ESXi Shell kan
även slås av via **DCUI** -\> **F2** -\> **Troubleshooting options**,
här kan även timeout-värden för dessa två tjänster, samt DCUI, ändras.

[Category:VMware](/Category:VMware "wikilink")