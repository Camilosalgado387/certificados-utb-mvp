from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import CatalogItem
from ..schemas import CatalogItemRead, DemoProfileRead
from ..services.seed import DEMO_PROFILES

router = APIRouter(prefix="/api/catalog", tags=["Catálogo"])


@router.get("", response_model=list[CatalogItemRead])
def list_active_catalog(db: Session = Depends(get_db)):
    """Lista los certificados activos con tarifa exacta en COP, SLA y vigencia (RF-02)."""
    return (
        db.query(CatalogItem)
        .filter(CatalogItem.activo.is_(True))
        .order_by(CatalogItem.id.asc())
        .all()
    )


@router.get("/demo-profiles", response_model=list[DemoProfileRead])
def list_demo_profiles():
    """Devuelve los perfiles precargados para la barra Modo Demo Multirrol (RF-01, RN-04)."""
    return DEMO_PROFILES

