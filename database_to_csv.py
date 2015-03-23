from database import Session, Article
import settings
import csv
import json

def extract_field(data, field):
    field_items = field.split("__")
    try:
        for f in field_items:
            data = data[f]
    except (KeyError, TypeError):
        return ""
    if not isinstance(data, (str, bytes)):
        data = ""
    if isinstance(data, bytes):
        data = data.decode("utf-8")
    return data.replace(",", " ")

def dump_articles():
    session = Session()
    articles = session.query(Article).all()
    headers = ["term"] + settings.ARTICLE_OUTPUT_FIELDS
    article_list = [headers]
    for a in articles:
        article_list_item = [a.term]
        data = json.loads(a.data)
        for field in settings.ARTICLE_OUTPUT_FIELDS:
            article_list_item.append(extract_field(data, field))
        article_list.append(article_list_item)

    with open(settings.OUTPUT_CSV_PATH, "w+") as csvfile:
        wr = csv.writer(csvfile)
        wr.writerows(article_list)

if __name__ == "__main__":
    dump_articles()
