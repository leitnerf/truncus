from sqlalchemy.ext.declarative import declarative_base
from config import DBUSER, DBPASS, DBHOST, DBNAME, DBTYPE
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData

DBSession = ''
Base = ''
print_query = ''

Base = declarative_base()

engine = create_engine("%s://%s:%s@%s/%s" % (DBTYPE, DBUSER, DBPASS, DBHOST, DBNAME), convert_unicode=True, pool_recycle=3600)
metadata = MetaData(engine)

Session = sessionmaker(bind=engine)
DBSession = Session()
