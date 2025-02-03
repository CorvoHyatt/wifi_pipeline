from unittest.mock import Base
from sqlalchemy import Column, String, Float

class WifiPoint(Base):
    __tablename__ = "wifi_points"

    id = Column(String, primary_key=True, index=True)
    programa = Column(String, nullable=False)
    fecha_instalacion = Column(String, nullable=True)
    latitud = Column(Float, nullable=False)
    longitud = Column(Float, nullable=False)
    colonia = Column(String, nullable=True)
    alcaldia = Column(String, nullable=True)
