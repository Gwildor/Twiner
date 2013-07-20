import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, Interval, String

Base = declarative_base()


class Timeline(Base):
    __tablename__ = 'Twiner_timelines'

    id = Column(Integer, primary_key=True)
    screen_name = Column(String(length=20))
    interval = Column(Interval, default=datetime.timedelta(minutes=5))
    last_update = Column(DateTime)

    def __repr__(self):
        return '<Timeline({0}, {1}, {2})>'.format(self.screen_name,
                                                  self.interval,
                                                  self.last_update)
