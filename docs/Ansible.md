---
title: Ansible
permalink: /Ansible/
---

Ansible är ett automatiseringsverktyg som hjälper till att managera din
miljö. Ansible ansluter till flera hostar samtidigt och kör små program
som heter "moduler" i den ordning som har specificerats i "playbooks".

“I wanted a tool that I could not use for 6 months, come back later, and
still remember how it worked.” - Michael DeHaan, creator.

Är det rätt verktyg för dig?
<http://www.infoworld.com/article/2609482/data-center/data-center-review-puppet-vs-chef-vs-ansible-vs-salt.html>

Installation
------------

Till skillnad mot t.ex. puppet finns det inga agenter/klienter utan man
installerar endast på en maskin, dvs standalone.

`#Ubuntu `
`sudo apt-get install software-properties-common`
`sudo apt-add-repository ppa:ansible/ansible`
`sudo apt-get update && sudo apt-get -y install ansible`

`#CentOS/Fedora`
`sudo yum install ansible`

`#Alternativt`
`sudo pip install ansible`

Grunder
-------

Efter installation är det dags att sätta ihop sin inventory-fil. Där
listar och grupperar man alla hostar som man ska jobba med, se nästa
stycke. Förslagsvis använder man inte IP-adresser utan namn i
DNS/hosts-fil för att hitta rätt. Det behöver också fixas SSH-nycklar på
alla hostar så att ansible kan autentisera sig på hostarna utan
lösenord. Se [Jumpgate](/Jumpgate "wikilink") för hur man genererar
nycklar och skickar ut. Har man olika användarnamn på maskinerna man ska
in på kan man specificera det i sin inventory-fil men för att hålla den
så ren som möjligt kan det också göras i \~/.ssh/config, se
[Jumpgate](/Jumpgate "wikilink").

Konfiguration
-------------

I ditt inventory läggs alla maskiner till och finns default i:
/etc/ansible/hosts

`#[all] gäller alla`
`cacti`
`ns02`
`beeswarm:2222`

`[dbservers]`
`dbsrv1`
`dbsrv2`

`[webservers]`
`websrv1`
`websrv2`

Moduler
-------

<http://docs.ansible.com/modules_by_category.html>

`ansible -m [modulnamn] all`
`ansible -m shell -a 'free -m' host1:host3`

Testa så att det funkar. Ping-modulen loggar in på maskinerna och kör
ping 127.0.0.1, output blir success eller fail.

`ansible all -m ping`

Default används SSH-nyckel för autentisering, för pw-fråga istället lägg
till: -k

Playbooks
---------

En playbook är en uppsättning instruktioner skrivna i yaml. Yaml är
lättläst för oss människor.

`ansible-playbook -i inventory_file dinplaybook.yml`

Exempel på playbook:

``` yaml
---
- hosts: all
  sudo: true
  tasks:
  - name: install apache2
    apt:
      pkg: apache
      state: present
      update_cache: true
  - name: start service
    service:
      name: apache2
      state: started
```

Om man har angett hosts i playbooken behövs de inte anges när man kör
kommandot. Annars kan man specificera enskilda hosts.

`ansible-playbook -l host5 apache.yml`

Kolla vilka hostar som eventuellt skulle beröras

`ansible-playbook playbook.yml --list-hosts`

Sudo

`ansible-playbook apache.yml -K  #--ask-sudo-pass`

### Ladda upp filer

Man kan ladda upp lokala filer i tasken.

`   - name: Upload default index.html for host`
`     copy: src=localfiles/index.html dest=/var/www/html/ mode=0644`

### Ladda ner filer

`   - name: Download file from website`
`     get_url: url=`[`http://hackernet.se/file.htm`](http://hackernet.se/file.htm)` dest=/var/www/html/index.html`

### Roller

Med roller kan man kalla på variabler, tasks och handlers som är
fördefinierade. Det kräver att man har en filstruktur för det.

`mkdir -p /etc/ansible/roles/`

### YAML

Yaml använder mellanslag som delimiter, använd ej tab.

``` yaml
---
- hosts: [target hosts]
  remote_user: [yourname]
  tasks:
    - [task 1]
    - [task 2]
```

**handlers:**
Handler är samma sak som task fast körs bara om de blivit kallade på av
en notify. Notify läggs i en task.

``` yaml
tasks:
  - [task 1]
    notify:
      - restart apache

handlers:
  - name: restart apache
    service: name=apache state=restarted
```

**vars_prompt**

``` yaml
vars_prompt:

- name: "Password"
  prompt: "Enter password"
  private: yes

...
  password: "{{Password}}"
...
```

### Templates

Bygg och testa jinja-templates: <https://ansible.sivel.net/test/>

Vault
-----

Med vault kan man skydda sina lösenord och nycklar med assymetrisk
AES-kryptering.

`ansible-vault create vault.yml`
`ansible-vault edit vault.yml`
`ansible-playbook vault.yml --ask-vault-pass`

[Category:Guider](/Category:Guider "wikilink")