from sqlalchemy import create_engine, func
import settings
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine(settings.DB_URL, echo=False)

metadata = MetaData()
from sqlalchemy import Column, Integer, String
class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    data = Column(String)
    term = Column(String)
    page = Column(Integer)
    published = Column(DateTime)
    nyt_id = Column(String, unique=True)
    start_date = Column(Date)
    end_date = Column(Date)

    created = Column(DateTime, server_default=func.now())
    modified = Column(DateTime, server_default=func.now(), onupdate=func.current_timestamp())

    def __repr__(self):
        return "<Article(term='{0}', page='{1}', id='{2}')>".format(self.term, self.page, self.id)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)