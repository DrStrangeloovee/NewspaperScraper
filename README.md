# NewspaperScraper
Newspaper scraping and datamining in python

## Run it via docker-compose
```bash
docker-compose up --build --remove-orphans
```

## Fetching comments manually
```bash
curl 'https://apps.derstandard.at/forum/1/2000121360370' -H 'User-Agent: Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'X-Requested-With: XMLHttpRequest' -H 'Origin: https://www.derstandard.at' -H 'Connection: keep-alive' -H 'Referer: https://www.derstandard.at/story/2000121360370/flugauto-bekommt-strassenzulassung-in-europa'
```

## Dependencies
Scrapy==2.5.0
chompjs==1.1.4
itemloaders==1.0.4
psycopg2-binary==2.9.1