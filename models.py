from sqlalchemy import Column, Integer, String
from database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, index=True)
    title = Column(String, index= True, nullable=False)
    content = Column(String, index= True, nullable= False)
    date_created = Column(Datetime, default = datetime.utcnow)
