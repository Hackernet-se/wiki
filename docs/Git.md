---
title: Git
permalink: /Git/
---

Git är ett versionshanteringsprogram som är gratis och open source. Det
skapades 2005 för att hantera källkoden till Linuxkärnan. Ens lokala
repository består av tre "trees" som git håller koll på.

-   Working Directory: håller alla filer som man jobbar med.
-   Index: är där filerna mellanlandar när man addar dem, innan commit.
-   HEAD: pekar på den senaste commiten man gjort.

### Overview

[<File:Hackernet-Git.PNG>](/File:Hackernet-Git.PNG "wikilink")

Installation
------------

`sudo apt-get install git`

Alternativt git-all för att få med alla subpackages.

Usage
=====

CLI

`git status`
`git log`
`git shortlog`
`git config color.ui true`

Det finns flera grafiska program för git.

### Repo

Skapa nytt lokalt repo.

`mkdir ~/reponame && cd ~/reponame`
`echo "reponame" >> README.md`
`git init`
`git add README.md`
`git commit -m "first commit"`

Skapa en working copy av ett lokalt repo.

`git clone /path/to/repository`

Lägg till ändring till Index.

`git add `<filename>
`git add *`

Commit till HEAD, dock är det fortfarande lokalt.

`git commit -m "Commit message"`

Pusha ändring till remote repo.

`git push origin master`

För att uppdatera det lokala repot med de senaste commitsen.

`git pull`

### Branch

Branches används för att utveckla features isolerat från varandra. Man
kan utveckla flera branches parallellt för att sedan mergea tillbaka dem
till Master. Master branch är "default" när man skapar ett repo.

Skapa en ny branch

`git checkout -b NAME`

Byt till en annan branch

`git checkout NAME`

Kolla branches

`git branch`

### .gitignore

Är en fil som används för att man ska skydda sig så att man av misstag
inte commitar filer man inte vill eller som är onödiga tex swp filer,
log filer, lösenord eller databas filer. [Github .gitignore
templates](https://github.com/github/gitignore)

`sparco@jumpgate:~/ircbot$ cat .gitignore`
`*.swp`
`test.py`
`__pycache__/`
`config.ini`
`*.log`

GitHub
======

GitHub är en webb-baserad Git repository hosting service. Det är gratis
att skapa ett konto och man kan pusha sin kod dit för att dela med sig
till andra.

Author name and email address

`git config --global user.name "Skeletor"`
`git config --global user.email "user@hackernet.se"`

Connect local repository to a remote server, add the server to be able
to push to it

`git remote add origin `[`https://github.com/user/reponame.git`](https://github.com/user/reponame.git)
`git remote -v`
`git push -u origin master`

Password cache

`git config --global credential.helper cache`
`git config --global credential.helper 'cache --timeout=3600'`

Klona repo från GitHub

`git clone `[`https://github.com/username/reponame.git`](https://github.com/username/reponame.git)

[Category:Guider](/Category:Guider "wikilink")