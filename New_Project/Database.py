from datetime import datetime
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime

Base = declarative_base()
class Capture(Base):
    __tablename__ = 'Capture'
    id = Column(Integer, primary_key = True)
    filename = Column(String(50))
    date = Column(DateTime, default = datetime.now)
    def __str__(self):
        return self.filename

engine = create_engine("sqlite:///animation.sqlite3",echo=True)
Base.metadata.create_all(engine)