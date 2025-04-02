---
title: JQ
permalink: /JQ/
---

jq är en command-line JSON parser. Som kan användas precis lika enkelt
som [sed](/sed "wikilink"),[awk](/awk "wikilink") och
[grep](/grep "wikilink") används för text.

Installation
============

-   <btn data-toggle="tab" class="">\#tab1\|CentOS 7</btn>
-   <btn data-toggle="tab" class="">\#tab2\|Ubuntu 16.04</btn>

<div class="tab-content">
<div id="tab1" class="tab-pane fade in active">
Kör sedan:

`sudo yum install jq`
`  `

</div>
<div id="tab2" class="tab-pane fade">

`sudo apt-get install jq`
`  `

</div>
</div>

Användning
==========

Skaffa lite exempel JSON via Hackernets API där vi söker på alla sidor
som innehåller ordet Cisco:

`curl '`[`https://hackernet.se/api.php?action=query&list=search&srsearch=cisco&format=json`](https://hackernet.se/api.php?action=query&list=search&srsearch=cisco&format=json)`'`

Pretty-printa JSON koden så den blir läsbar:

`curl '`[`https://hackernet.se/api.php?action=query&list=search&srsearch=cisco&format=json`](https://hackernet.se/api.php?action=query&list=search&srsearch=cisco&format=json)`' | jq '.'`

Filtrera ut vilka sidor du hitta:

`curl '`[`https://hackernet.se/api.php?action=query&list=search&srsearch=cisco&format=json`](https://hackernet.se/api.php?action=query&list=search&srsearch=cisco&format=json)`' | jq '.query.search[].title'`

Filtrera ut titeln och exempel texten från sidan:

`curl '`[`https://hackernet.se/api.php?action=query&list=search&srsearch=cisco&format=json`](https://hackernet.se/api.php?action=query&list=search&srsearch=cisco&format=json)`' | jq '.query.search[] | {titel: .title, text: .snippet}'`

Sortera sidorna efter lägst antal ord:

`curl '`[`https://hackernet.se/api.php?action=query&list=search&srsearch=cisco&format=json`](https://hackernet.se/api.php?action=query&list=search&srsearch=cisco&format=json)`' | jq '.query.search | sort_by(.wordcount) | .[].title'`

Skapa en URL till varje sida:

`curl '`[`https://hackernet.se/api.php?action=query&list=search&srsearch=cisco&format=json`](https://hackernet.se/api.php?action=query&list=search&srsearch=cisco&format=json)`' | jq '.query.search[] | ("`[`https://hackernet.se/w/"+`](https://hackernet.se/w/%22+)`""+.title)'`

Tips'N'Tricks
=============

Använd [jqplay](https://jqplay.org/) för att enkelt skriva jq filter.

[Category:Guider](/Category:Guider "wikilink")