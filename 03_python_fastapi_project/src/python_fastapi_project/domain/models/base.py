from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

# This Base class serves as a foundation for mapping models to database tables
# Every model class inheriting this Base class will tell the ORM (SQLAlchemy) that: this is a database table.
Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True # This tells the ORM that this class is not a table itself
    id = Column(Integer, primary_key=True, index=True)

class BaseAudit(BaseModel):
    __abstract__ = True
    created_by = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_by = Column(String(100))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
