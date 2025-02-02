from unittest.mock import Base
from sqlalchemy import Column, Integer, String, Float

class WifiPoint(Base):
    __tablename__ = "wifi_points"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    colonia = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    status = Column(String, default="activo")  #Opcional: para marcar si el punto está activo o no
