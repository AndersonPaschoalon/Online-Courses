import sqlalchemy.ext.declarative
from sqlalchemy.orm import registry

mapper_registry = registry()

ModelBase = sqlalchemy.ext.declarative.declarative_base()
