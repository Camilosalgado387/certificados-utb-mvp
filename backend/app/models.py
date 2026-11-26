import uuid
from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime,ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from .database import Base


def utcnow () -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo = None)


# 1. Catálogo tarifario configurable (RF-02)

class CatalogItem(Base):
    __tablename__ = "catalog_items"
    id = Column(Integer, primary_key=True,index=True)
    codigo = Column(String(50), unique=True,nullable=False, index=True)
    nombre = Column(String(150), nullable=False)        
    precio_cop = Column(Integer, nullable=False)  #RNF-03: Entero exacto en COP (sin floats)
    sla_dias_habiles = Column(Integer,nullable=False)
    dias_vigencia = Column(Integer, nullable=False)     
    requiere_opt = Column(Boolean, default=False,nullable=False)
    activo = Column(Boolean, default=True,nullable=False)





# 2. Cabecera del expediente por radicado (RF-03,RN-02, RN-03)
class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True,index=True)
    numero_radicado = Column(String(40), unique=True,nullable=False, index=True)
    id_titular = Column(String(40), nullable=False, index=True)
    nombre_titular = Column(String(150),nullable=False)
    perfil_titular = Column(String(20), nullable=False)  # ESTUDIANTE | EGRESADO
    referencia_pago = Column(String(40), unique=True,nullable=False)
    total_cop = Column(Integer, nullable=False)  #RNF-03: Entero exacto
    sla_max_dias = Column(Integer, nullable=False)  #RN-02: SLA más largo del carrito
    estado = Column(String(30), nullable=False,default="PENDIENTE_PAGO", index=True)
    expira_pago_en = Column(DateTime, nullable=False)# RN-03: +48 horas
    fecha_limite_sla = Column(DateTime,nullable=True)
    cumplio_sla = Column(Boolean, nullable=True)        
    creado_en = Column(DateTime, nullable=False,default=utcnow)
    pagado_en = Column(DateTime, nullable=True)
    entregado_en = Column(DateTime, nullable=True)      

    # Relaciones con los hijos del expediente
    items = relationship("RequestItem",back_populates="request", cascade="all,delete-orphan")
    notifications = relationship("Notification",back_populates="request", cascade="all,delete-orphan")


# 3. Detalle por certificado dentro del carrito(RF-05, RF-06, RN-05)
class RequestItem(Base):
    __tablename__ = "request_items"
    id = Column(Integer, primary_key=True,index=True)
    request_id = Column(Integer,ForeignKey("requests.id"), nullable=False,index=True)
    catalog_item_id = Column(Integer,ForeignKey("catalog_items.id"), nullable=False)     
    precio_unitario_cop = Column(Integer, nullable=False)
    estado_item = Column(String(30), nullable=False,default="PENDIENTE")
    motivo_observacion = Column(Text, nullable=True)    
    consulta_opt_nota = Column(Text, nullable=True)     
    respuesta_opt = Column(Text, nullable=True)
    actualizado_en = Column(DateTime, nullable=False, default=utcnow, onupdate=utcnow)

    request = relationship("Request", back_populates="items")
    catalog_item = relationship("CatalogItem")
    document = relationship(
        "Document",
        back_populates="request_item",
        uselist=False,
        cascade="all, delete-orphan",
    )


    # 4. Custodia verificada de PDFs y telemetría de re-descargas (RF-07, RF-10, RNF-02)
class Document(Base):
    __tablename__ = "documents"

    id_documento = Column(String(36),primary_key=True, default=lambda:str(uuid.uuid4()))
    request_item_id = Column(Integer,
    ForeignKey("request_items.id"), unique=True, nullable=False)
    numero_radicado = Column(String(40),nullable=False, index=True)
    id_titular = Column(String(40), nullable=False,index=True)
    tipo_certificado = Column(String(150),nullable=False)
    fecha_expedicion = Column(DateTime,nullable=False)
    fecha_vigencia = Column(DateTime, nullable=False)   
    hash_sha256 = Column(String(64), nullable=False)    
    ruta_archivo = Column(String(255),nullable=False)
    contador_redescargas = Column(Integer,nullable=False, default=0)
    request_item = relationship("RequestItem",back_populates="document")


    # 5. Bandeja interna de notificaciones transaccionales (RF-09)
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True,index=True)
    request_id = Column(Integer,
    ForeignKey("requests.id"), nullable=False,index=True)
    numero_radicado = Column(String(40),nullable=False, index=True)
    id_destinatario = Column(String(40),nullable=False, index=True)
    tipo_hito = Column(String(30), nullable=False)  #   NOTIF_1_RADICADO | NOTIF_2_PAGO |NOTIF_3_ENTREGADO
    mensaje = Column(Text, nullable=False)
    leida = Column(Boolean, nullable=False,default=False)
    creado_en = Column(DateTime, nullable=False,default=utcnow)
    request = relationship("Request",back_populates="notifications")