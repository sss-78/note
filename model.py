# from sqlalchemy import Column, Integer, String, DateTime, text, TIMESTAMP
# from sqlalchemy.orm import declarative_base
# from datetime import datetime
# from database import Base

# class Users(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     username = Column(String, nullable=False)
#     email = Column(String, nullable=False, unique=True)
#     password = Column(String, nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)