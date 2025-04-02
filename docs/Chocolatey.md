---
title: Chocolatey
permalink: /Chocolatey/
---

Chocolatey är en pakethanterare för Windows, som [apt](/apt "wikilink")
och yum.

Installation
------------

Du kan installera via cmd eller powershell.

### CMD

Kör cmd som admin.

`@powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((new-object net.webclient).DownloadString('`[`https://chocolatey.org/install.ps1`](https://chocolatey.org/install.ps1)`'))" && SETPATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin`

### Powershell

Kör powershell som admin.

``` powershell
iex ((new-object net.webclient).DownloadString('https://chocolatey.org/install.ps1'))
```

Se till att `Get-ExecutionPolicy` är satt till bypass.

`Set-ExecutionPolicy bypass`

Exempel
-------

**Installera**

Starta cmd som admin och skriv,

`choco install git 7zip vlc firefox -y`

**Söka**

`choco search firefox`

GUI
---

`choco install chocolateygui`

[Category:Windows](/Category:Windows "wikilink")