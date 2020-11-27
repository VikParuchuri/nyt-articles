from requests.packages.urllib3.exceptions import ProtocolError
import settings
import requests
import urllib
import json
from database import Session, Article
import shelve
import datetime
from copy import deepcopy
import time
import dateutil
import dateutil.parser
import math
import logging
log = logging.getLogger(__name__)

# Setup logging
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


def access_api(term, page, start_date, end_date):
    time.sleep(6)
    start_string = start_date.strftime("%Y%m%d")
    end_string = end_date.strftime("%Y%m%d")
    url = "http://api.nytimes.com/svc/search/v2/articlesearch.json?q={0}&page={1}&api-key={2}&begin_date={3}&end_date={4}".format(term, page, urllib.parse.quote_plus(settings.API_KEY), start_string, end_string)

    resp = None
    content = None
    i = 0
    while i < 3 and (content is None or resp.status_code != 200):
        try:
            resp = requests.get(url)
            increment_queries()
        except ProtocolError:
            log.warn("Protocol error, sleeping 5 mins and retrying.")
            time.sleep(300)
            resp = requests.get(url)
        try:
            data = json.loads(resp.content.decode("utf-8"))
            content = data["response"]
        except ValueError:
            log.error("Could not decode response: {0}".format(resp.content))
            raise ValueError
        i += 1

    return content

def increment_queries():
    cache = shelve.open(settings.SHELF_PATH, writeback=True)
    amount = cache.get(settings.QUERY_KEY, 0)

    last_time = cache.get(settings.LAST_DAY_KEY, datetime.datetime.now())
    if (datetime.datetime.now() - last_time) > datetime.timedelta(days=1):
        last_time = datetime.datetime.now()
        amount = 0
    cache[settings.LAST_DAY_KEY] = last_time
    cache[settings.QUERY_KEY] = amount + 1
    cache.sync()

    if amount % 100 == 0:
        log.info("Have {0} queries so far today.".format(amount))

    if (amount + 1) > settings.QUERY_LIMIT:
        log.info("Sleeping...")
        while (datetime.datetime.now() - last_time) < datetime.timedelta(days=1):
            log.info("Sleeping for another {0} hours.".format(24 - ((datetime.datetime.now() - last_time).total_seconds() / 60 / 60)))
            time.sleep(960)
    cache.close()


def scrape_term(term):
    log.info("Starting on: {0}".format(term))
    end_date = deepcopy(settings.END_DATE)
    start_date = deepcopy(settings.START_DATE)
    date_gap = end_date - start_date
    page = 0
    session = Session()
    last_article = session.query(Article).filter_by(term=term).order_by(Article.created.desc()).first()
    if last_article is not None:
        start_date = last_article.start_date
        end_date = last_article.end_date
        if end_date >= settings.END_DATE:
            return
    while start_date < settings.END_DATE:
        if end_date > settings.END_DATE:
            end_date = deepcopy(settings.END_DATE)
        date_gap = end_date - start_date
        data = access_api(term, page, start_date, end_date)
        allowed_hits = (settings.MAX_HIT_PAGES * settings.HITS_PER_PAGE)
        while data["meta"]["hits"] > allowed_hits:
            date_ratio = data["meta"]["hits"] / allowed_hits
            date_gap = date_gap / date_ratio
            end_date = deepcopy(start_date) + date_gap
            data = access_api(term, page, start_date, end_date)
        log.info("Working on date range {0} to {1}, with {2} hits.".format(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), data["meta"]["hits"]))
        page = 0
        while page * settings.HITS_PER_PAGE < data["meta"]["hits"] and (page + 1) < settings.MAX_HIT_PAGES:
            data = access_api(term, page, start_date, end_date)
            for doc in data["docs"]:
                article = session.query(Article).filter_by(nyt_id=doc["_id"]).first()
                if article is None:
                    published = dateutil.parser.parse(doc["pub_date"])
                    article = Article(
                        data=json.dumps(doc),
                        nyt_id=doc["_id"],
                        term=term,
                        page=page,
                        start_date=start_date,
                        end_date=end_date,
                        published=published
                    )
                    session.add(article)
                    session.commit()
            page += 1
        start_date = end_date
        end_date = deepcopy(start_date) + date_gap
    log.info("Done with term {0}.".format(term))

if __name__ == "__main__":
    for term in settings.SCRAPE_TERMS:
        scrape_term(term)




