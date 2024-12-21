Code to get a map from wikipedia for each English county (via web scraping or API) and turn this into an [anki](https://apps.ankiweb.net/) flashcard package. 

First run:

`python get-images.py`

Alternatively, can specify the arguments if don't want to use defaults:

`python get-images.py --save-folder data --use-api false`

Then run:

`python generate-deck.py`

Or:

`python generate-deck.py --image-folder data --output-file data/county_deck.apkg`
