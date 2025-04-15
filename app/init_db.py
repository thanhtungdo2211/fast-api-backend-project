from sqlalchemy import create_engine

from configure import config
from database import Base

def init_db():
    engine = create_engine(config.URL_DATABASE)
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()