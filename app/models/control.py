from sqlalchemy import Column, Boolean
from app.database import Base

class ImportControl(Base):
    __tablename__ = "import_control"
    id = Column(Boolean, primary_key=True, default=True)
    imported = Column(Boolean, default=False)