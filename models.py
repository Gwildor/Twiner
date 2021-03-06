import datetime

import dateutil.parser
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, \
    Interval, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Timeline(Base):
    __tablename__ = 'Twiner_timelines'

    id = Column(Integer, primary_key=True)
    screen_name = Column(String(length=20))
    interval = Column(Interval, default=datetime.timedelta(minutes=5))
    last_update = Column(DateTime)

    tweets = relationship('Tweet', backref='timeline', lazy='dynamic')

    def __repr__(self):
        return '<Timeline({0}, {1}, {2})>'.format(
            self.screen_name, self.interval, self.last_update)


class Tweet(Base):
    __tablename__ = 'Twiner_tweets'

    id = Column(BigInteger, primary_key=True)
    timeline_id = Column(Integer, ForeignKey(Timeline.id))
    text = Column(String(length=200))
    date = Column(DateTime)

    def __init__(self, tweet={}):
        self.id = tweet['id']
        self.text = tweet['text'].encode('utf8')
        self.date = dateutil.parser.parse(tweet['created_at'])

    def __repr__(self):
        return '<Tweet({0}, {1}, {2})>'.format(self.timeline.screen_name,
                                               self.text, self.date)
