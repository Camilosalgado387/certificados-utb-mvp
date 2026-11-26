import uuid
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import CatalogItem, Notification, Request, RequestItem, utcnow
from ..schemas import RequestCreate, RequestRead


router = APIRouter(prefix= "/api/requests", tags = ["Solicitudes"])

@router.post("", response_model = RequestRead, status_code = status.HTTP_201_CREATED)

def create_request(payload:RequestCreate, db: Session = Depends(get_db)):
    #1 Consultar CatalogItem para payload.CatalogItem_ids y validar que existan/estén activos
    encontrados = (db.query(CatalogItem)
        .filter(
            CatalogItem.id.in_(payload.catalog_item_ids),
            CatalogItem.activo.is_(True),
        )
        .all()
    )
    #Diccionario para busca rapido
    mapa_catalogo = {item.id: item for item in encontrados}

    #Armamos lista del carrito validando uno por uno de los ids recibidos
    items_carritos = []
    for item_id in payload.catalog_item_ids:
        if item_id not in mapa_catalogo:
          raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"El certificado con id {item_id} no existe o esta inactivo.",
          )  
        items_carritos.append(mapa_catalogo[item_id])
    #2 Calculo de los 5 datos
    total_cop = sum(item.precio_cop for item in items_carritos)
    sla_max_dias = max(item.sla_dias_habiles for item in items_carritos)
    ahora = utcnow()
    expira_pago_en = ahora + timedelta(hours = 48)
    codigo_corto = uuid.uuid4().hex[:6].upper()
    numero_radicado = f"UTB-{ahora.year}-{codigo_corto}"
    referencia_pago = f"REF-{uuid.uuid4().hex[:8].upper()}"

    #3 Crear Request -> db.add(), se creo el header y flush()
    nueva_solicitud = Request(                          
        numero_radicado=numero_radicado,                
        id_titular=payload.id_titular,
        nombre_titular=payload.nombre_titular,
        perfil_titular=payload.perfil_titular,
        referencia_pago=referencia_pago,
        total_cop=total_cop,
        sla_max_dias=sla_max_dias,
        estado="PENDIENTE_PAGO",
        expira_pago_en=expira_pago_en,
        creado_en=ahora,
    )
    db.add(nueva_solicitud)
    db.flush()

    #4 Crear cada RequestItem y la Notificación #1
    #4a. Guardar una fila en request_items por cada certificado del carrito

    for item in items_carritos:
        nuevo_item = RequestItem(
            request_id = nueva_solicitud.id,
            catalog_item_id = item.id,
            precio_unitario_cop = item.precio_cop,
            estado_item = "PENDIENTE",
        )
        db.add(nuevo_item)
    #4b. Guardar la Notificación #1 (NOTIF_1_RADICADO) en notificaciones
    notificacion = Notification(

        request_id = nueva_solicitud.id,
        numero_radicado = numero_radicado,
        id_destinatario = payload.id_titular,
        tipo_hito = "NOTIF_1_RADICADO",
        mensaje = (
            f"Solicitud {numero_radicado} radicada por ${total_cop:,} COP. "
            f"Referencia de pago {referencia_pago} vigente por 48 horas."
        ),
        creado_en = ahora
    )
    db.add(notificacion)
    #5 Guardar en SQLite y retornar
    #5.1 Confirmar toda la transacción de golpe, refrescar relaciones y retornar

    db.commit()
    db.refresh(nueva_solicitud)
    return nueva_solicitud