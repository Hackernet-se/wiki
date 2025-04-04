---
title: Rsyslog
permalink: /Rsyslog/
---

[Category:Guider](/Category:Guider "wikilink") RSYSLOG står för
**ro**cket-fast **sys**tem for **log** processing. Rsyslog är väldigt
flexibelt har en mängd olika input plugins och output plugins som gör
att du kan forwarda dina loggar till andra system som Elasticsearch,
Kafka eller bara spara ner dina loggar till en fil som roterar dagligen.

Rsyslog lämpar sig därför väldigt bra som en central log aggeragator.

Installation
============

-   <btn data-toggle="tab" class="">\#tab1\|CentOS 7/8</btn>
-   <btn data-toggle="tab" class="">\#tab2\|Ubuntu 18.04/20.04</btn>

<div class="tab-content">
<div id="tab1" class="tab-pane fade in active">

`yum -y install rsyslog`

</div>
<div id="tab2" class="tab-pane fade">

`apt-get install rsyslog`
`  `

</div>
</div>

Konfiguration
=============

Default så letar rsyslog efter **.conf** filer under **/etc/rsyslog.d/**

Syslog server
-------------

Starta en syslog server som lysnar på port 514 TCP/UDP och som sparar
ner varje enhet i sin egen fil.

``` bash
# Load modules for UDP & TCP
module(load="imudp")
module(load="imtcp")

# Start to listen on port 514 TCP/UDP
input(type="imudp" port="514")
input(type="imtcp" port="514")

# Templates
template(name="RemoteHost" type="string" string="/var/log/remote/%HOSTNAME%_%$YEAR%_%$MONTH%_%$DAY%.log")

# Actions
action(type="omfile" DynaFile="RemoteHost")
```

Kafka Output
------------

Man kan använda rsyslog som en aggregator som sedan skickar datan vidare
till en Kafka instance. Då kan man man använda sig av
[omkafka](https://www.rsyslog.com/doc/master/configuration/modules/omkafka.html)
pluginet.

-   <btn data-toggle="tab" class="">\#tab3\|CentOS 7/8</btn>
-   <btn data-toggle="tab" class="">\#tab4\|Ubuntu 18.04/20.04</btn>

<div class="tab-content">
<div id="tab3" class="tab-pane fade in active">

`yum -y install rsyslog-kafka`

</div>
<div id="tab4" class="tab-pane fade">

`apt-get install rsyslog-kafka`
`  `

</div>
</div>

Simpel syslog server som tar emot på port 514 TCP/UDP och som exportar
till en Kafka instans direkt.

``` bash
# Load modules for UDP & TCP
module(load="imudp")
module(load="imtcp")
module(load="omkafka")

# Start to listen on port 514 TCP/UDP
input(type="imudp" port="514")
input(type="imtcp" port="514")

# Actions
action(type="omkafka" Broker="<BROKER IP>" Topic="<KAFKA-TOPIC>")
```

### Dynamic Topic

Man kan skicka syslog till olika topics baserat på innehållet i syslog
meddelandet, tex facility, hostname, datum osv. Egentligen allt som
rsyslog själv kan urskilja, vad det finns för färdig definierade
variabler kan man hitta
[här.](https://www.rsyslog.com/doc/master/configuration/properties.html)

För att slå på denna funktion använder man sig av:

`DynaTopic="on"`

Det gör att **topic** parametern pekar på en template istället.

I detta exempel så skickar jag syslog till en topic baserat på vilken
input syslogen kommer in på.

``` bash
# Module loaders
module(load="imudp")
module(load="imtcp")
module(load="omkafka")

# Juniper input
input(type="imudp" port="5141" name="juniper")
input(type="imtcp" port="5141" name="juniper")

# VMware input
input(type="imudp" port="5140" name="vmware")
input(type="imtcp" port="5140" name="vmware")

# Template
template(name="Kafka_Topic" type="string" string="syslog.%INPUTNAME%")

# Output to Kafka
action(type="omkafka" Broker="<BROKER IP>" DynaTopic="on" Topic="Kafka_Topic")
```

### Dynamic Key

By default så skriver man i random order till olika partitioner för att
lastbalansera. Detta kommer göra att när man läser tillbaka syslogen
ifrån Kafka så kommer meddelande ifrån samma enhet att inte komma i
ordning. För att fixa detta måste man skicka med en key. Det gör att
alla meddelande ifrån enhet1 tex alltid kommer att hamna i partition 1.
På så sätt kommer man alltid läsa meddelanden från varje enhet i den
ordningen dom skapades.

För att fixa detta använder man sig av:

`DynaKey="on"`

Det gör att **key** parametern pekar på en template istället.

I exemplet nedan så sätter vi keyn till IP'n det kommer ifrån.

``` bash
# Module loaders
module(load="imudp")
module(load="imtcp")
module(load="omkafka")

# Input
input(type="imudp" port="514")
input(type="imtcp" port="514")

# Template
template(name="Kafka_Key" type="string" string="%FROMHOST-IP%")

# Output to Kafka
action(type="omkafka" Broker="<BROKER IP>" DynaKey="on" Topic="Kafka_Key")
```

### Multiple brokers

Om man har ett Kafka cluster så behöver man sätta flera brokers det gör
man såhär:

``` bash
action(type="omkafka" Broker=["<BROKER IP>","<BROKER IP>","<BROKER IP>"] Partitions.Auto="on" Topic="Kafka_Topic")
```

Det är också bra om man sätter på:

`Partitions.Auto="on"`

Det gör att man automatiskt kommer att last balansera alla meddelande
man skapar till alla partioner för den topicen.

Structured data - RFC5424
-------------------------

Ifall du har en syslog som följer RFC 5424 kan du använda dig av den
fördefinierade templaten **RSYSLOG_SyslogProtocol23Format** för att
behålla strukturen när du sparar till fil eller forwardar loggen till
ett annat system.

``` bash
action(type="omkafka" Broker="<BROKER IP>" Topic="<KAFKA-TOPIC>" template="RSYSLOG_SyslogProtocol23Format")
```