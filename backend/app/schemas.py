from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

PerfilTitular = Literal["ESTUDIANTE", "EGRESADO"]
RolDemo = Literal["ESTUDIANTE", "TESORERIA", "REGISTRO", "DIRECCION"]
EstadoRadicado = Literal[
    "PENDIENTE_PAGO",
    "EN_ELABORACION",
    "EN_CONSULTA_OPT",
    "ENTREGADO",
    "EXPIRADO",
]
EstadoItem = Literal["PENDIENTE", "OBSERVADO", "EN_CONSULTA_OPT", "PDF_LISTO"]
TipoHito = Literal["NOTIF_1_RADICADO", "NOTIF_2_PAGO", "NOTIF_3_ENTREGADO"]


# --- Catálogo y Perfiles Demo (S1-03) ---
class CatalogItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str
    nombre: str
    precio_cop: int = Field(..., ge=0)
    sla_dias_habiles: int = Field(..., ge=1)
    dias_vigencia: int = Field(..., ge=1)
    requiere_opt: bool
    activo: bool


class DemoProfileRead(BaseModel):
    id_usuario: str
    nombre: str
    rol: RolDemo
    perfil_titular: PerfilTitular | None = None
    etiqueta: str


# --- Custodia y Notificaciones (S1-02 / Semanas 3-4) ---
class DocumentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_documento: str
    request_item_id: int
    numero_radicado: str
    id_titular: str
    tipo_certificado: str
    fecha_expedicion: datetime
    fecha_vigencia: datetime
    hash_sha256: str
    ruta_archivo: str
    contador_redescargas: int = Field(..., ge=0)


class NotificationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    request_id: int
    numero_radicado: str
    id_destinatario: str
    tipo_hito: TipoHito
    mensaje: str
    leida: bool
    creado_en: datetime


# --- Solicitudes / Carrito (S1-05) ---
class RequestCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    id_titular: str = Field(..., min_length=3, max_length=40)
    nombre_titular: str = Field(..., min_length=3, max_length=150)
    perfil_titular: PerfilTitular
    catalog_item_ids: list[int] = Field(..., min_length=1)


class RequestItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    request_id: int
    catalog_item_id: int
    precio_unitario_cop: int = Field(..., ge=0)
    estado_item: EstadoItem
    motivo_observacion: str | None = None
    consulta_opt_nota: str | None = None
    respuesta_opt: str | None = None
    actualizado_en: datetime
    catalog_item: CatalogItemRead | None = None
    document: DocumentRead | None = None


class RequestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    numero_radicado: str
    id_titular: str
    nombre_titular: str
    perfil_titular: PerfilTitular
    referencia_pago: str
    total_cop: int = Field(..., ge=0)
    sla_max_dias: int = Field(..., ge=1)
    estado: EstadoRadicado
    expira_pago_en: datetime
    fecha_limite_sla: datetime | None = None
    cumplio_sla: bool | None = None
    creado_en: datetime
    pagado_en: datetime | None = None
    entregado_en: datetime | None = None
    items: list[RequestItemRead] = []
    notifications: list[NotificationRead] = []


