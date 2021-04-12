# CoronaStatus

## Funktionen

Dieses Program soll Statusmeldungen von legitimen Quellen zu Corona per Telegram verschicken.

## Aufbau

Das Programm besteht aus dem rssHandler und dem api_handler.

### rssHandler

* Der rssHandler ist verantwortlich für den download und die Sortierung von Nachrichten.

* Der _**rssGRABBER**_ cached die Daten des RSS-Feeds der Tagesschau, also die letzten ca. 40 Nachrichten auf der Webseite der Tagesschau, in einer JSON Datei.

* Der _**rssSorter**_ filtert die gecachten Nachrichten nach einigen Schlüsselbegriffen und speichert relevante Meldungen in einer weiteren JSON Datei.

### api_handler

* Der api besitzt einen api_parser, der auf Anfdreage von dem API ourworldindata.org/data/owid-covid-data aktuelle Statusinformationen abruft.
* Hinzugefügt werden sollen ein **acessing-Programm**, ein **error-logger** und ein **cacher**, in dem die ereignisse eine gewisse Zeit gespeichert werden.
* Anfragen gestalten sich so:

_setup:_

```python
from api_handler.metadata_api_parser import api_parser

parser = api_parser('preferred country alias')
parser.get_by_key_and_date('preferred key', 'eventually date')
```

_für eine Liste der Länder-aliasse:_

```python
parser.get_possible_countrys()
```

_für eine Liste der Keys:_

```python
parser.return_possible_keys()
```

## Quellen der Statusmeldungen

Tagesschau.de\
ourworldindata.org
