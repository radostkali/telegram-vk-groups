from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import POSTGRES_URI


engine = create_engine(POSTGRES_URI)
Session = sessionmaker(bind=engine)
