from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base
from typing import Dict, Any

class WifiPoint(Base):
    __tablename__ = "wifi_points"  # Nombre de la tabla en la base de datos

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id = Column(String, primary_key=True, index=True)
    programa = Column(String, nullable=False)
    fecha_instalacion = Column(String, nullable=True)
    latitud = Column(Float, nullable=True)
    longitud = Column(Float, nullable=True)
    colonia = Column(String, nullable=True)
    alcaldia = Column(String, nullable=True)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "uuid": str(self.uuid),
            "id": self.id,
            "programa": self.programa,
            "fecha_instalacion": self.fecha_instalacion,
            "latitud": self.latitud,
            "longitud": self.longitud,
            "colonia": self.colonia,
            "alcaldia": self.alcaldia
        }