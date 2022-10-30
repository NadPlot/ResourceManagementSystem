from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

from .config import settings


engine = create_engine(settings.db_url)

# подключение к существующей БД (была создана отдельно)
metadata = MetaData()
metadata.reflect(engine)
Base = automap_base(metadata=metadata)
Base.prepare()

# Определено в соответствии с таблицами отдельно созданной БД
User = Base.classes.User


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
