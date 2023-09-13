from sqlalchemy import Column, String, Integer
from  model import Base

class Comments(Base):
    __tablename__ = 'comments'

    id = Column("pk_comment", Integer, primary_key=True)
    user = Column(Integer)
    title = Column(String(100))
    emoji = Column(String(80))
    text = Column(String(220))

    def __init__(self, user:int, title:str, emoji:str, text:str):
        self.user = user
        self.title = title
        self.emoji = emoji
        self.text = text

  
