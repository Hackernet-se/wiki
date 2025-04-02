---
title: Tmux
permalink: /Tmux/
---

Tmux är en terminal multiplexer precis som screen. En fördel med att
använda terminal multiplexers är att du inte tappar dina shell fönster
om du skulle tappa anslutningen eller vill fortsätta jobbet på en annan
dator.

Installation
============

Tmux är enkelt att installera och finns redan färdig packat i dom flesta
distars repos.

**Debian baserade**

`apt-get install tmux`

**RHEL baserade**

`yum install epel-release`
`yum install tmux`

Kommandon
=========

Starta tmux,

`tmux`

Lista tmux sessioner,

`tmux ls`

Attach till en session

`tmux attach`

Attach till en session och detach andra som är anslutna till samma
session.

`tmux attach -d`

Attach till en session om man har flera igång.(Byt \# mot siffra)

`tmux a -t #`

Stäng en session(Byt \# mot en siffra)

`tmux kill-session -t #`

Keybinds
========

Default prefix för tmux är .

\- Skapa ett nytt fönster.

\- Gå till nästa eller föregående fönster.

\- Byt fönster.

\- Meny med alla fönster.

\- Stäng ett fönster.

\- Byt namn på ett fönster.

\- Splitta fönster horisontellt.

\- Splitta fönster vertikalt.

\- För att hoppa imellan paneler.

\- Stäng den aktiva panelen.

\- Skapa ett nytt fönster med den aktiva panelen.

\- Zooma in ett fönster.

\- Copy läge.

-   \- För att börja markera text i copy läget.

-   För att kopiera den markerade texten.

\- Klistra in den kopierade texten.

\- För att deattacha en session.

\- För att scrolla upp och ner.

Tmux Plugin Manager
===================

Kräver version 1.9 eller högre. Plugins som gör ditt Tmux fönster lite
trevligare.

Installera
----------

`git clone `[`https://github.com/tmux-plugins/tpm`](https://github.com/tmux-plugins/tpm)` ~/.tmux/plugins/tpm`

Skapa filen `.tmux.conf` i din home folder.

`# List of plugins`
`set -g @plugin 'tmux-plugins/tpm'`
`set -g @plugin 'tmux-plugins/tmux-sensible'`

`# Other examples:`
`# set -g @plugin 'github_username/plugin_name'`
`# set -g @plugin 'git@github.com/user/plugin'`
`# set -g @plugin 'git@bitbucket.com/user/plugin'`

`# Initialize TMUX plugin manager (keep this line at the very bottom of tmux.conf)`
`run '~/.tmux/plugins/tpm/tpm'`

Ladda sedan TPM genom att starta om din tmux session eller ladda om
confen med.

`tmux source ~/.tmux.conf`

Lägga till plugins
------------------

Plugins finns på [TPM's Github](https://github.com/tmux-plugins)

Lägg sedan till pluginet i `.tmux.conf` med kommandot
`set -g @plugin '...'`

Öppna sedan Tmux och tryck för att installera.

`prefix + I`

Ta bort plugin genom att ta bort raden kommentera ut den i `.tmux.conf`
och tryck.

`prefix + alt + u`

Bra plugins
-----------

[Sensible](https://github.com/tmux-plugins/tmux-sensible) - Ett gäng
inställningar som man bör ha.

[Resurrect](https://github.com/tmux-plugins/tmux-resurrect) - Spara din
nuvarande Tmux session.

[Continuum](https://github.com/tmux-plugins/tmux-continuum) - Autosparar
din nuvarande Tmux session.(Kräver resurrect)

[Sidebar](https://github.com/tmux-plugins/tmux-sidebar) - Öppnar en tree
liknande sidebar.

[Vim-tmux](https://github.com/tmux-plugins/vim-tmux) - Fixar visa saker
i vim som inte funkar så bra annars.

[tmux-logging](https://github.com/tmux-plugins/tmux-logging) - Toggla
av/på för att logga en pane till textfil, "screencapture" på en pane,
eller spara all historik i en pane till textfil.

Auto attach
===========

Lägg detta i din `.bashrc` för att automatiskt starta tmux och attacha
till en session vid inloggning.

``` bash
if  -z "$TMUX" ; then
   tmux has-session &> /dev/null
   if [ $? -eq 1 ]; then
     exec tmux new
     exit
   else
     exec tmux attach
     exit
   fi
fi
```

Tips'n'trix
===========

#### För att skriva till alla panes samtidigt.

`:setw synchronize-panes`

#### Clear-history

`:clear-history`

Eller binda det till

`bind -n C-k clear-history`

#### Problem att piltangenterna inte fungerar?

Upptäckte problemet när jag var ansluten till senare versioner av
[JunOS](/Juniper_JunOS "wikilink"). Att jag var tvungen att skriva om
alla kommandon igen för att jag inte kunde trycka fram det senast körda
kommandona. Efter att ha lagt till följande i min **.tmux.conf** fil så
fungera det igen.

`set -g default-terminal "xterm-256color"`

#### Byt pane snabbt utan prefix

Lägg till följande i din tmux.conf för att kunna byta pane med .

`bind -n M-Left select-pane -L`
`bind -n M-Right select-pane -R`
`bind -n M-Up select-pane -U`
`bind -n M-Down select-pane -D`

#### Byt window utan prefix

Lägg till följande för att byta window med

`bind -n S-Left  previous-window`
`bind -n S-Right next-window`

[Category:Tools](/Category:Tools "wikilink")