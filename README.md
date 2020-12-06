# NYT Article Scraper

This repo scrapes info about articles from the New York Times API.  It doesn't get the full articles, just the metadata, headline, and snippets.

This fork rotates API keys and updates query limits.

Getting Started
-------------

* The first step is to sign up for an API key.  You can get one [here](http://developer.nytimes.com/), by clicking on the `keys` link to the left.
* Now, clone this repo and go into the folder.
    * `git clone git@github.com:VikParuchuri/nyt-articles.git`
    * `cd nyt-articles`
* Make a file called `private.py`, and add the following lines to it (with your values instead of the shown ones).
    * `API_KEY = "INSERT_YOUR_KEY_HERE"`
    * `SCRAPE_TERMS = ["list", "of", "terms", "you", "want", "to", "get", "articles", "for"]`
* Run `python run_scrape.py` to download all the article information and save it to the database.  You'll see a lot of log messages as this goes on.
* Run `python database_to_csv.py` to output all of the articles from the database to `articles.csv`.

Problems this addresses
--------------------

* The NYT API only allows `10,000` requests per day.  This repo will sleep until the next day once the limit is hit.
* The NYT API only allows `200` pages of results per search query (`2000` articles total).  But sometimes you want to get articles for a long time period.  This gets around it by adding `start_date` and `end_date`, automatically segmenting the articles into smaller sets, and downloading the whole range through multiple queries.
* If you get disconnected, restarting in the right spot can be a pain.  This repo stores everything in the database, which enables it to restart in the right spot without any additional queries.
* There are a lot of strange error conditions that can pop up as you go through the process.  This can deal with some of them.

Additional configuation
--------------------

* Change `START_DATE` and `END_DATE` in `settings.py` (or better yet, add them to private.py) to your own values to change the default start and end dates to fetch articles from.
* Change the `ARTICLE_OUTPUT_TERMS` key in `settings.py` to change which data fields show up in the output csv.  Double underscore `__` gets nested dictionary keys.

Contribution
---------------------

Please fork this repo and make a pull request to contribute.
