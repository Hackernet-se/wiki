---
title: Bash
permalink: /Bash/
---

Bash är den allra vanligaste kommandotolken man möts av i Linux.

Bash sensible
=============

\[<https://github.com/mrzool/bash-sensible>\| Bash sensible\] är ett
script som försöker sätta bättre bash default inställningar. Precis som
Vim sensible försöker göra åt vim.

Sensible fixar bla hur bash hanterar history

-   Adderar till historiken istället för att skriva över.
-   Sparar multi-line kommandon som ett kommando.
-   Större historik.
-   Tar bort dubbletter.
-   Sparar inte onödiga kommandon som exit, ls, bg, fg och history.

`git clone `[`https://github.com/mrzool/bash-sensible/blob/master/sensible.bash`](https://github.com/mrzool/bash-sensible/blob/master/sensible.bash)

För att installera kan man kopiera hela **sensible.bash** eller delar av
filen in i sin **bashrc** fil eller source in filen i sin **bashrc**
fil:

``` bash
if [ -f ~/bash-sensible/sensible.bash ]; then
   source ~/bash-sensible/sensible.bash
fi
```

Awesome bash
============

Awesome bash är en lista med massa länkar till olika bash saker. Allt
från böcker, custom environment, frameworks, spel.

[`https://github.com/awesome-lists/awesome-bash`](https://github.com/awesome-lists/awesome-bash)

Bash scripting
==============

Att skriva bash script kan vara väldigt enkelt och kan spara mycket tid,
här under kommer en del tips som kan vara bra att känna till.

Shebang
-------

Man öppnar alltid alla script med en så kallad shebang. Detta för att
systemet ska veta av hur den ska köra filen.

``` bash
 #!/usr/bin/env bash
```

Variabler
---------

Variabler i bash skrivs på följande sätt **`variable-name=`***<value>*

``` bash
#!/usr/bin/env bash
HW="Hello World"
echo $HW
```

``` bash
sparco@jumpgate:~$ ./script
Hello World
```

Argument
--------

Att kunna skicka in argument i sitt bash script för att göra det mer
dynamiskt kan vara bra ibland. Första argumentet mappas mot `$1` medans
resten bara fortsätter enligt `$2,$3,$4...`.

``` bash
#!/usr/bin/env bash
echo $1 $2
```

``` bash
sparco@jumpgate:~$ ./script Hello World
Hello World
```

Debuga scripts
--------------

Att kunna debuga scripts kan göras på olika sätt genom att köra `echo`
på variabler eller sätta på en växel i bash som gör att den printar allt
i sdout. Att köra scriptet med `bash -x`

``` bash
sparco@jumpgate:~$ bash -x ./script Hello world
+ echo Hello world
Hello world
```

Ett annat sätt om man vill debuga delar av ett script istället för allt
kan man använda sig av följande sätt:

``` bash
set -x
......
set +x
```

[Category:Tools](/Category:Tools "wikilink")