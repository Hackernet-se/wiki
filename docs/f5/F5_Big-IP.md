---
title: F5 Big-IP
permalink: /F5_Big-IP/
---

[Category:F5](/Category:F5 "wikilink")

F5 Big-IP är en plattform utfärdad av företaget F5 med möjlighet att
köra lastbalancering, remote vpn, ddos skydd på olika nivåer. Alla
funktionerna styrs till olika moduler på den Linuxbaserade enheten och
man kan specificera hur många kärnor man vill lägga till vilken adc. En
adc kallas den enhet som kör flera VMar på den fysiska appliancen med
berörda moduler och hårdvaruspecifikation tilldelat till sig.

Moduler
-------

-   [LTM (Local Traffic
    Manager)](https://www.f5.com/pdf/products/big-ip-local-traffic-manager-ds.pdf)
-   [APM (Access Policy
    Manager)](https://www.f5.com/pdf/products/big-ip-access-policy-manager-ds.pdf)
-   [AFM (Advanced Firewall
    Manager)](https://www.f5.com/pdf/products/big-ip-advanced-firewall-manager-datasheet.pdf)
-   [AAM (Application Acceleration
    Manager)](https://www.f5.com/pdf/products/big-ip-application-acceleration-manager-datasheet.pdf)
-   [ASM (Application Security
    Manager)](https://www.f5.com/pdf/products/big-ip-application-security-manager-ds.pdf)
-   [GTM (Global Traffic
    Manager)](https://www.f5.com/pdf/products/big-ip-global-traffic-manager-ds.pdf)
-   [Link
    Controller](https://www.f5.com/pdf/products/big-ip-link-controller-ds.pdf)
-   PSM (Procotol Security Module)

Big-IP Appliance
----------------

Hårdvaruplattformen som modulerna i fråga aktiveras på finns det olika
specifikation på beroende på throughput och portdensitet. Modelerna som
är aktuella i dagsläget är de som börja på (i). Det finns även
chassibaserade enheter som kallas Viprion. Dessa körs i stor skala hos
de större leverantörena och kan i sitt chassi basera på konfiguration
simulera flera mindre ADC enheter eller köra en all-in-one lösning.

HTTP2
-----

Detta protokoll är mycket användbart framförallt för att man utöckar
möjligheten att hämta information från en webbfront mycket snabbare och
säkrare. HTTP2 bygger på en ny struktur istället för HTTP1.0/1.1. Man
har i HTTP2 möjlighet att köra följande features.

-   Multiplexing
-   Server Push
-   Header Compression
-   Binary format
-   Extended Security

1.  Minimum Keys
2.  Ephemeral key
3.  TLS 1.2

Alla dessa features bidrar till en snabbare och säkrare publicering av
webbtjänster och F5an har möjlighet att publicera HTTP2 när servern
bakom inte kan eller endast kan köra HTTP1.1.