from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import settings


engine = create_engine(settings.DATABASE_URL)
Session = sessionmaker(bind=engine)
