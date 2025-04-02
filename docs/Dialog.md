---
title: Dialog
permalink: /Dialog/
---

Dialog är ett program som skapar snygga dialogrutor inifrån shell
scripts. Det finns t.ex. rutor för yes/no, menu, input, message.

`dnf -y install dialog`

Några exempel på dialogrutor.

`dialog --textbox /etc/hosts 22 70`
`dialog --title "Message" --yesno "Big box?" 19 75`
`dialog --infobox "Stuff is happening" 10 30 ; sleep 8`
`dialog --inputbox "Enter something:" 8 40 2>answer`
`dialog --menu "Choose one:" 10 30 3 1 red 2 green 3 blue`

[Category:Tools](/Category:Tools "wikilink")