from sqlalchemy.orm import Session
from ..models import CatalogItem

INITIAL_CATALOG = [
    {
        "codigo": "CERT-MATRICULA",
        "nombre": "Certificado de Estudio / Matrícula Activa",
        "precio_cop": 18500,
        "sla_dias_habiles": 2,
        "dias_vigencia": 60,
        "requiere_opt": False,
        "activo": True,
    },
    {
        "codigo": "CERT-NOTAS",
        "nombre": "Certificado de Notas / Historia Académica",
        "precio_cop": 29000,
        "sla_dias_habiles": 3,
        "dias_vigencia": 90,
        "requiere_opt": False,
        "activo": True,
    },
    {
        "codigo": "CERT-CONDUCTA",
        "nombre": "Certificado de Buena Conducta Disciplinaria",
        "precio_cop": 22000,
        "sla_dias_habiles": 3,
        "dias_vigencia": 90,
        "requiere_opt": False,
        "activo": True,
    },
    {
        "codigo": "CERT-EGRESADO",
        "nombre": "Certificado de Terminación de Materias / Egresado",
        "precio_cop": 25000,
        "sla_dias_habiles": 4,
        "dias_vigencia": 90,
        "requiere_opt": False,
        "activo": True,
    },
    {
        "codigo": "CERT-CONTENIDOS",
        "nombre": "Contenidos Programáticos Avalados por Programa",
        "precio_cop": 48000,
        "sla_dias_habiles": 5,
        "dias_vigencia": 180,
        "requiere_opt": True,
        "activo": True,
    },
]

DEMO_PROFILES = [
    {
        "id_usuario": "T00054321",
        "nombre": "Valentina Morales (Ing. de Sistemas)",
        "rol": "ESTUDIANTE",
        "perfil_titular": "ESTUDIANTE",
        "etiqueta": "Estudiante Activo (Pregrado)",
    },
    {
        "id_usuario": "T00019876",
        "nombre": "Andrés Mendoza (Egresado Ing. Industrial)",
        "rol": "ESTUDIANTE",
        "perfil_titular": "EGRESADO",
        "etiqueta": "Egresado UTB",
    },
    {
        "id_usuario": "TES-001",
        "nombre": "Analista de Servicios Financieros",
        "rol": "TESORERIA",
        "perfil_titular": None,
        "etiqueta": "Tesorería",
    },
    {
        "id_usuario": "REG-001",
        "nombre": "Auxiliar de Certificaciones",
        "rol": "REGISTRO",
        "perfil_titular": None,
        "etiqueta": "Auxiliar de Registro Académico",
    },
    {
        "id_usuario": "DIR-001",
        "nombre": "Coordinación Académica de Programa",
        "rol": "DIRECCION",
        "perfil_titular": None,
        "etiqueta": "Dirección de Programa",
    },
]


def seed_catalog(db: Session) -> None:
    """Inserta de forma idempotente cualquier certificado inicial faltante por código."""
    existing_codes = {row[0] for row in db.query(CatalogItem.codigo).all()}
    inserted = False
    for data in INITIAL_CATALOG:
        if data["codigo"] not in existing_codes:
            db.add(CatalogItem(**data))
            inserted = True

    if inserted:
        db.commit()
