# NewspaperScraper
Newspaper scraping and datamining in python


## Fetching comments manually
```bash
curl 'https://apps.derstandard.at/forum/1/2000121360370' -H 'User-Agent: Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'X-Requested-With: XMLHttpRequest' -H 'Origin: https://www.derstandard.at' -H 'Connection: keep-alive' -H 'Referer: https://www.derstandard.at/story/2000121360370/flugauto-bekommt-strassenzulassung-in-europa'
```

## Dependencies
Scrapy==2.4.1
chompjs==1.0.16
itemloaders==1.0.4
scrapy-pagestorage==0.3.1