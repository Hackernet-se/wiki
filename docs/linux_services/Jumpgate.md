---
title: Jumpgate
permalink: /Jumpgate/
---

En jumpgate kan användas för att öka säkerheten men också för att
förenkla maskinhantering genom att ha ett enda ställe man loggar in på
och kan managera övriga resurser.

Grundläggande
-------------

Grundläggande för en jumpgate är att ha en kompetent terminal
multiplexer, t.ex [Tmux](/Tmux "wikilink").

### Screen

``` bash
sudo apt-get update && sudo apt-get upgrade && sudo apt-get -y install screen

cat <<'__EOF__'>> .screenrc
defscrollback 10000
term xterm-256color
termcapinfo xterm* ti@:te@
altscreen on
nethack on
hardstatus alwayslastline
shelltitle 'bash'
hardstatus string '%{gk} %H [%{wk}%?%-Lw%?%{=b kR}(%{W}%n*%f %t%?(%u)%?%{=b kR})%{= w}%?%+Lw%?%? %{g} ] %{W}'
screen -t $ 0
screen -t $ 1 htop
screen -t bash 2
select 0
__EOF__
```

Ännu mer grundläggande är att ha en automagisk screen som alltid ställer
upp vid login.

``` bash
cat <<'__EOF__'>> .bashrc
if [ -z "$STARTED_SCREEN" ] && [ -n "$SSH_TTY" ]
then
 case $- in
   (*i*)
     STARTED_SCREEN=1; export STARTED_SCREEN
     mkdir -p -- "$HOME/lib/screen-logs"
     screen -R -D -S main  ||
       echo "Screen failed! continuing with normal bash startup"
 esac
fi
__EOF__
```

### Tmux

`sudo apt-get update && sudo apt-get upgrade && sudo apt-get -y install tmux`

Attacha automatiskt till din tmux session vid inloggning.

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

**Keep-Alive**
Håll SSH-sessioner vid liv genom att skicka ett litet paket med jämna
mellanrum.

`echo "    ServerAliveInterval 120" | sudo tee -a /etc/ssh/ssh_config`

SSH Autentisering
-----------------

För att göra inloggning mot andra maskiner smidigare kan man använda sig
av SSH-nycklar som autentisering. Och för att göra det mindre smidigt se
[Google Authenticator](/Google_Authenticator "wikilink").

Först måste man skaffa sig nyckelpar man kan distribuera till övriga
hostar. Detta görs endast en gång.

`ssh-keygen -t rsa -b 4096`
`ssh-keygen -t ecdsa -b 521`
`ssh-keygen -t ed25519`

Sedan skicka ut nyckeln till hostarna med:

`ssh-copy-id 192.168.0.10`

*Om ssh-copy-id ej finns tillgängligt*

`cat ~/.ssh/id_rsa.pub | ssh user@192.168.0.10 "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"`

Alternativt skicka med den vid automatiserad PXE-installation.

Användarnamn
------------

För att slippa skriva olika användarnamn beroende på host kan man lägga
in dem så de autoanvänds vid anslutning.

`dd of=~/.ssh/config << EOF`
`Host server1`
`User root`

`Host 192.168.0.1`
`User elnacho`

`Host fw02`
`User admin`
`ServerAliveInterval 60`
`EOF`

Login Notification
------------------

Sshd kan trigga script via PAM, t.ex. om man vill få en notis i slack
när någon loggar in på en server.

``` Bash
echo "#sshd login notify slack, $(date)" | sudo tee -a /etc/pam.d/sshd && \
echo "session  optional  pam_exec.so  /usr/sbin/sshd-login_notify-slack.sh" | sudo tee -a /etc/pam.d/sshd
sudo dd of=/usr/sbin/sshd-login_notify-slack.sh << EOF
#!/bin/bash
if [ "$PAM_TYPE" != "close_session" ]; then
    WEBHOOK_URL="https://hooks.slack.com/services/0FTBMMLJ/EWUYGN2J/aGq3nW2PjrNcPdhxxx"
    SERVER="$(hostname)"
    PAYLOAD=" { \"text\": \"$PAM_USER logged in to $SERVER from remote host: $PAM_RHOST.\" }"
    curl -X POST -H 'Content-Type: application/json' -d "$PAYLOAD" "$WEBHOOK_URL"
fi
exit
EOF
sudo chmod +x /usr/sbin/sshd-login_notify-slack.sh
```

Testa

`PAM_USER=test PAM_RHOST=1.2.3.4 PAM_TYPE=open_session /usr/sbin/sshd-login_notify-slack.sh`

Bastion
-------

En bastion fungerar som en reverse proxy för SSH-servrar. Komponenten
som behövs är SSH Agent Forwarding och finns inbyggt i OpenSSH. För att
göra hoppet genom proxyn transparent måste SSH-nycklar användas för
autentisering. DNS-uppslag på alla maskiner måste fungera.

[500px](/File:ssh-bastion.png "wikilink")

`nano ~/.ssh/config`
`Host inside-server`
` ProxyJump bastion`

`Host bastion`
` User basse`
` IdentityFile ~/.ssh/ed25519`
` ForwardAgent yes`

.bashrc
-------

.bashrc är en fil som körs varje gång bash laddas. I denna filen kan du
skriva egna kommandon som du kan köra i kommandoprompten.

**Extract**
Skriv `extract `<filnamn> för att packa upp en fil.

``` bash
 extract () {
    if [ -f $1 ] ; then
        case $1 in
            *.tar.bz2)   tar xvjf $1    ;;
            *.tar.gz)    tar xvzf $1    ;;
            *.bz2)       bunzip2 $1     ;;
            *.rar)       unrar x $1       ;;
            *.gz)        gunzip $1      ;;
            *.tar)       tar xvf $1     ;;
            *.tbz2)      tar xvjf $1    ;;
            *.tgz)       tar xvzf $1    ;;
            *.zip)       unzip $1       ;;
            *.Z)         uncompress $1  ;;
            *.7z)        7z x $1        ;;
            *)           echo "don't know how to extract '$1'..." ;;
        esac
    else
        echo "'$1' is not a valid file!"
    fi
  }
```

[Category:Guider](/Category:Guider "wikilink")