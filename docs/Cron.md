---
title: Cron
permalink: /Cron/
---

Cron är det generella namnet på den service som kör schemalagda jobb och
är ett klassiskt verktyg inom UNIX oxh Linuxvärlden. Med cron kan man
automatisera återkommande uppgifter. Crond är namnet på daemonen som
körs i bakgrunden.

### Crontab

Cron tables är filer som läses av crond och innehåller de schemalagda
jobben. Detta kan även kallas cronjobs. Den generella formen för
crontab:

`minute hour day-of-month month day-of-week  command`

Visa aktuella cronjobs för nuvarande användare

`crontab -l`

Editera cronjobs

`crontab -e`

### Output

Cron skickar per default output från jobben till användarens mailbox,
t.ex. output som annars skickas till stdout. Vill man slippa detta kan
man skicka outputen till /dev/null.

`>/dev/null`

Vill man även slippa error-output till sin mailbox kan man ignorera
allt.

`>/dev/null 2>&1`

### Access Control

För att styra vilka som får schemalägga jobb kan man skriva användarnamn
i följande filer:

-   /etc/cron.d/cron.allow
-   /etc/cron.d/cron.deny

[Category:Tools](/Category:Tools "wikilink")