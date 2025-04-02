---
title: Pagespeed
permalink: /Pagespeed/
---

[Category:Guider](/Category:Guider "wikilink") PageSpeed är ett program
utvecklat av Google för att göra internet lite snabbare.
(https://developers.google.com/speed/pagespeed/) Om man kollar på
källkoden på Googles söksida ser man ett oläsligt hav av tecken, det är
resultatet av PageSpeed på deras sida. Det finns moduler för
[Nginx](/Nginx "wikilink") och [Apache](/Apache "wikilink"). (Pagespeed
module is only available as source)

Optimiseringsfilter
-------------------

Här följer en lista på några användbara filter:

1.  **Local Storage Cache**

This filter saves inlined resources to the browser's local storage (an
HTML5 feature) on the first view of a page, and loads them from local
storage on subsequent views rather than sending them (inline) again.

1.  **Combine CSS**

'Combine CSS' seeks to reduce the number of HTTP requests made by a
browser during page refresh by replacing multiple distinct CSS files
with a single CSS file, containing the contents of all of them. This is
particularly important in old browsers, that were limited to two
connections per domain. In addition to reduced overhead for HTTP headers
and communications warm-up, this approach works better with TCP/IP
slow-start, increasing the effective payload bit-rate through the
browser's network connection.

1.  **Pre-Resolve DNS**

This can contribute significantly towards total page load time. This
filter reduces DNS lookup time by providing hints to the browser at the
beginning of the HTML, which allows the browser to pre-resolve DNS for
resources on the page.

1.  **Collapse Whitespace**

The filter reduces the transfer size of HTML files by replacing
contiguous whitespace with a single whitespace character. Because HTML
is often formatted with extra whitespace for human readability or as an
incidental effect of the templates used to generate it, this technique
can reduce the number of bytes needed to transmit HTML resources.

1.  **Lazyload Images**

The lazyload_images filter defers loading of images until they become
visible in the client's viewport or the page's onload event fires. This
avoids blocking the download of other critical resources necessary for
rendering the above the fold section of the page.

1.  **Insert Google Analytics**

The 'Insert Google Analytics' filter adds the basic Google Analytics
javascript snippet to each HTML page. If the page already has a Google
Analytics snippet inside

<head>

with the specified ID, then no additional snippet will be added. If
another Google Analytics snippet is on the page with a different ID,
then an additional snippet will be added with the ID specified in with
AnalyticsID. In order to avoid any strange Google Analytics reporting,
make sure that the ID specified in the configuration file matches the
one used on your site.

1.  **Remove Comments**

The remove_comments filter eliminates HTML comments, which are often
used to document the code or to comment out experiments. Note that this
directive applies only to HTML files. CSS comments are eliminated with
the rewrite_css filter, and Javascript comments are eliminated with the
rewrite_javascript filter.

Nginx
-----

(Installation)

`server {`
`...`
`pagespeed on;`
`pagespeed RewriteLevel CoreFilters;`
`pagespeed FileCachePath "/var/cache/ngx_pagespeed/";`
`pagespeed EnableFilters combine_css,remove_comments,collapse_whitespace;`
`...`
`}`