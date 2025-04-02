---
title: Google Authenticator
permalink: /Google_Authenticator/
---

Med Google Authenticator kan man använda time-based one-time password
(TOTP) tillsammans med sitt vanliga lösenord på sin
[SSH-server](/Jumpgate "wikilink") för att få 2-faktors-autentisering.
Allt sker mellan server och mobil som båda vet när nycklar är giltiga.

Installation
============

`sudo apt-get -y install libpam-google-authenticator`
`echo "#Google Authenticator $(date)" | sudo tee -a /etc/pam.d/sshd && echo "auth required pam_google_authenticator.so" | sudo tee -a /etc/pam.d/sshd`
`sudo sed -i 's/ChallengeResponseAuthentication no/ChallengeResponseAuthentication yes/g' /etc/ssh/sshd_config`
`sudo service ssh restart`

Konfiguration
=============

Logga in på det lokala konto som ska köra MFA.

`google-authenticator`

Svara y, starta appen och scanna qr-koden.

**Vitlista nätverk**
Man kan styra om MFA ska användas eller ej beroende på source address på
SSH-sessionerna. Lägg in följande i /etc/pam.d/sshd ovanför raden *auth
required pam_google_authenticator.so*

`auth [success=1 default=ignore] pam_access.so accessfile=/etc/security/access-local.conf`

`cat /etc/security/access-local.conf`
`+ : ALL : 10.0.0.0/24`
`+ : ALL : LOCAL`
`- : ALL : ALL`

[Category:Guider](/Category:Guider "wikilink")