import os
from datetime import date

BASE_PATH = os.path.dirname(__name__)
DB_PATH = os.path.join(BASE_PATH, "db.sqlite3")
DB_URL = 'sqlite:///{0}'.format(DB_PATH)
OUTPUT_CSV_PATH = os.path.join(BASE_PATH, "articles.csv")

SHELF_PATH = os.path.join(BASE_PATH, "shelf.shelve")

START_DATE = date(2010, 11, 24)
END_DATE = date(2020, 11, 24)

QUERY_KEY = "query_count"
LAST_DAY_KEY = "last_day"
QUERY_LIMIT = 10000
MAX_HIT_PAGES = 200
HITS_PER_PAGE = 10

API_KEY = ""

SCRAPE_TERMS = []
ARTICLE_OUTPUT_FIELDS = ["snippet", "lead_paragraph", "abstract", "source", "print_page", "headline__main", "headline__print_headline", "pub_date", "news_desk", "section_name", "document_type", "web_url", "type_of_material", "word_count", "_id"]


from private import *
