# Plan de Implementación de 4 Semanas — Prototipo MVP Certificados Académicos UTB

Hoja de ruta práctica para construir en solitario el prototipo funcional especificado en [TRD.md](./TRD.md) y diseñado en [ARCHITECTURE.md](./ARCHITECTURE.md), manteniendo intacta la visión institucional de [Planificación certificados utb.md](../Planificación%20certificados%20utb.md) y el índice ejecutivo en [README.md](./README.md).

## 1. Ritmo de Trabajo (4 Semanas a Tiempo Parcial — 1 Persona)

El plan está diseñado para **1 desarrollador a tiempo parcial** trabajando por cortes verticales:
- **Cierre semanal demostrable:** Cada semana cierra con un flujo navegable y funcional en pantalla, evitando semanas aisladas de solo base de datos o maquetación sin conectar.
- **Cero fricción de infraestructura (`RNF-01`):** Ejecución 100% local sobre `backend/utb_proto.db` (SQLite con SQLAlchemy listo para PostgreSQL vía `DATABASE_URL`) y carpeta `backend/storage/certificados/`.
- **Tareas atómicas para tablero:** Cada ítem `- [ ]` equivale a un *Issue* acotado (1 a 3 horas de foco) listo para gestionarse en **GitHub Projects**.
- **Definición de terminado por tarea:** Endpoint probado en `/docs` (Swagger de FastAPI), conectado a la vista correspondiente en `frontend/` y respetando estados/montos exactos en `COP` (`RNF-03`).

---

## 2. Cronograma Semanal con Tareas Accionables (`Issues`)

### Semana 1 — Base del Proyecto, Mockup Base y Solicitud Estudiante (`RF-01`..`RF-03`)

**Meta visible al cerrar la semana:** Alternar roles en la barra superior, explorar el catálogo tarifario UTB, armar un carrito con varios certificados y radicar una solicitud obteniendo `Numero_Radicado` + orden de pago con vigencia de **48 horas**.

- [ ] **S1-01 — Inicializar `backend/` con FastAPI + SQLAlchemy + SQLite:** Crear `app/main.py`, `database.py` (`DATABASE_URL` por defecto `sqlite:///./utb_proto.db`), CORS local y directorio `backend/storage/certificados/`.
- [ ] **S1-02 — Modelar las 5 tablas relacionales:** Declarar en `models.py` y `schemas.py` las tablas `catalog_items`, `requests`, `request_items`, `documents` y `notifications` usando enteros exactos en `COP` (`RNF-03`).
- [ ] **S1-03 — Sembrar catálogo tarifario UTB y perfiles demo (`RF-02`):** Cargar semilla inicial de certificados (notas, buena conducta, contenidos programáticos con `requiere_opt=true`, etc.), tarifas `COP`, SLA en días hábiles, días de vigencia y `GET /api/catalog`.
- [ ] **S1-04 — Inicializar `frontend/` en Next.js + barra Modo Demo (`RF-01`, `RN-04`):** Configurar App Router + TypeScript + Tailwind CSS (`RNF-04`) y barra `DemoRoleBar` persistente para alternar en 1 clic entre `Estudiante / Egresado` (activo o egresado), `Tesorería`, `Auxiliar de Registro Académico` y `Dirección de Programa`.
- [ ] **S1-05 — Endpoint de radicación con carrito múltiple (`RF-03`, `RN-02`, `RN-03`):** Implementar `POST /api/requests` calculando total acumulado, `sla_max_dias` = máximo del carrito, estado `PENDIENTE_PAGO`, vencimiento `expira_pago_en` (+48 horas) y `NOTIF_1_RADICADO`.
- [ ] **S1-06 — Vista de catálogo, carrito y orden referenciada:** Construir la pantalla estudiantil para agregar `1..N` certificados al carrito, confirmar radicación y mostrar referencia única con temporizador de 48h.

> **Chequeo de cierre Semana 1:** Radicar un carrito con 2 certificados distintos desde `Estudiante / Egresado`, verificar en `utb_proto.db` un único registro en `requests` (`PENDIENTE_PAGO`), 2 filas en `request_items` y el SLA igual al mayor de los dos ítems.

### Semana 2 — Simulador de Pago, Tesorería y Bandejas Operativas (`RF-04`..`RF-06`)

**Meta visible al cerrar la semana:** Aprobar el pago en 1 clic sin subir comprobantes, atender la cola ordenada por SLA en Registro Académico, marcar observaciones de revisión o escalar consulta opcional a Dirección de Programa.

- [ ] **S2-01 — Conciliación simulada y ventana de 48 horas (`RF-04`, `RN-03`, `RN-05`):** Implementar `POST /api/requests/{numero_radicado}/pay` validando las 48h (marca `EXPIRADO` si venció; si está vigente pasa a `EN_ELABORACION` con ítems en `PENDIENTE`, fija `fecha_limite_sla` y crea `NOTIF_2_PAGO`).
- [ ] **S2-02 — Botón *"Simular pago aprobado"* y vista de `Tesorería`:** Integrar pago en 1 clic desde el resumen del estudiante y bandeja de órdenes `PENDIENTE_PAGO` en `Tesorería`, sin adjuntar soportes ni recibos bancarios.
- [ ] **S2-03 — Bandeja de Registro Académico priorizada por SLA (`RF-05`):** Ampliar `GET /api/requests` y maquetar la cola de `Auxiliar de Registro Académico` ordenada por `fecha_limite_sla` más próxima con indicador `PDF_LISTO / total`.
- [ ] **S2-04 — Marcación de ítem `OBSERVADO` (`RF-06`, `RN-01`, `RN-05`):** Implementar `PATCH /api/request-items/{item_id}/status` y formulario rápido para retener ítems con inconsistencias reales (ej. **lugar de expedición** equivocado o diferencias de créditos entre avance de carrera e historia académica).
- [ ] **S2-05 — Flujo opcional `EN_CONSULTA_OPT` con Dirección de Programa (`RF-06`):** Permitir escalar un ítem a `EN_CONSULTA_OPT`, habilitar bandeja de respuesta en `Dirección de Programa` y devolver el expediente a `EN_ELABORACION` al registrar el aval académico.

> **Chequeo de cierre Semana 2:** Pagar en 1 clic el radicado de la Semana 1, cambiar el selector superior a `Auxiliar de Registro Académico`, marcar un ítem como `OBSERVADO` y escalar el segundo a `Dirección de Programa` verificando el reflejo inmediato de estados.

### Semana 3 — Carga Manual de PDFs, Entrega Consolidada e Historial (`RF-07`..`RF-09`)

**Meta visible al cerrar la semana:** Subir manualmente el PDF final de cada ítem con huella `SHA-256`, comprobar la retención en carritos parciales (`1 de N`) y disparar la **entrega única consolidada** con notificaciones in-app y línea de tiempo.

- [ ] **S3-01 — Subida manual de PDF y custodia local `SHA-256` (`RF-07`, `RN-01`, `RNF-02`):** Implementar `POST /api/request-items/{item_id}/document` guardando `<id_documento>.pdf` en `backend/storage/certificados/`, registrando `hash_sha256`, `fecha_expedicion`, `fecha_vigencia` y solo-lectura lógica tras la entrega.
- [ ] **S3-02 — Regla de entrega única consolidada (`RF-08`, `RN-02`, `RN-05`):** Evaluar tras cada subida si el `100%` del carrito llegó a `PDF_LISTO`; retener descargas mientras esté parcial (`1 de N`) y, al completar `N de N`, transitar a `ENTREGADO`, calcular `cumplio_sla` y emitir `NOTIF_3_ENTREGADO`.
- [ ] **S3-03 — Centro de notificaciones dentro de la app (`RF-09`):** Implementar `GET /api/notifications` y campana superior con las 3 alertas transaccionales (#1 radicación/referencia, #2 pago confirmado, #3 certificados entregados).
- [ ] **S3-04 — Línea de tiempo y rastreador por radicado (`RF-09`):** Construir vista de autoseguimiento (`GET /api/requests/{numero_radicado}`) mostrando etapa actual, sub-estado `EN_CONSULTA_OPT` cuando aplique y avance individual por certificado.
- [ ] **S3-05 — Vista inicial del Historial de Certificados (`RF-10`):** Implementar `GET /api/documents/history/{id_titular}` listando certificados `ENTREGADO` con sus fechas de expedición, vigencia documental y huella `SHA-256`.

> **Chequeo de cierre Semana 3:** En un carrito de 2 ítems, subir solo el primer PDF y confirmar que el estudiante aún no puede descargarlo (`1 de 2`); subir el segundo PDF y verificar el paso automático a `ENTREGADO` + `NOTIF_3_ENTREGADO`.

### Semana 4 — Re-descarga con Telemetría, Métricas y Tus Ideas Nuevas (`RF-10`)

**Meta visible al cerrar la semana:** Prototipo redondo de extremo a extremo con re-descarga auditada por vigencia, tablero de 3 indicadores, datos semilla de casos borde y espacio para tus mejoras propias.

- [ ] **S4-01 — Re-descarga con control de `fecha_vigencia` y telemetría (`RF-10`, `RN-05`, `RNF-02`):** Implementar `GET /api/documents/{id_documento}/download` comprobando integridad `SHA-256` y `fecha_actual <= fecha_vigencia`, sumando `+1` a `contador_redescargas` o deshabilitando la descarga si venció.
- [ ] **S4-02 — Tablero ligero de 3 tarjetas de métricas (`RF-10`):** Implementar `GET /api/metrics` y vista resumen con 3 indicadores claros: trámites por estado, porcentaje de cumplimiento SLA y total acumulado de re-descargas.
- [ ] **S4-03 — Datos semilla de casos borde y pulido visual (`RNF-04`):** Precargar expedientes demostrativos listos al abrir la app (`EXPIRADO` >48h, carrito `1 de 2`, ítem `OBSERVADO` por lugar de expedición y documento vencido) y ajustar diseño responsivo.
- [ ] **S4-04 — Espacio abierto para tus ideas propias del prototipo:** Iterar mejoras diferenciales sin añadir infraestructura pesada (ej. botón demo *"Adelantar reloj +49h / +90 días"* para probar expiraciones en vivo, o verificador local de integridad `SHA-256`).

> **Chequeo de cierre Semana 4:** Re-descargar dos veces un certificado vigente viendo subir `contador_redescargas` en Historial y en las 3 métricas, y comprobar que un certificado con `fecha_vigencia` vencida muestra bloqueo e invita a solicitar uno nuevo.

---

## 3. Cómo Llevar tu Control Semanal en GitHub Projects + MCP en Antigravity

Gestiona las 4 semanas desde Antigravity sin perder tiempo copiando tareas a mano:

1. **Activar repositorio y tablero Kanban en GitHub Projects:**
   - Crea el repositorio remoto en GitHub y en la pestaña **Projects > New project > Board** define 3 columnas: `Todo`, `Esta Semana` y `Hecho`.
   - Crea 4 etiquetas (`semana-1`, `semana-2`, `semana-3`, `semana-4`) para filtrar cada corte semanal.
2. **Conectar el servidor MCP de GitHub en `~/.gemini/config/mcp_config.json`:**
   Genera un *Personal Access Token* en GitHub (permisos de lectura/escritura en *Issues*, *Contents* y *Projects*) y agrégalo al archivo global `~/.gemini/config/mcp_config.json` de Antigravity:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_REEMPLAZA_CON_TU_TOKEN"
      }
    }
  }
}
```

   *Opción remota sin Node local:* También puedes usar el endpoint oficial Streamable HTTP de GitHub definiendo `"url": "https://api.githubcopilot.com/mcp/"` dentro de `"github"` (verificable en **Additional Options (...) > MCP Servers**).

3. **Prompts prácticos para delegarle el seguimiento al agente:**
   - *Lunes al arrancar semana:* `"Lee Docs/IMPLEMENTATION-PLAN.md y crea en GitHub los issues S1-01 a S1-06 con la etiqueta semana-1."`
   - *Durante la semana:* `"Terminamos S2-04; actualiza y cierra el issue en GitHub resumiendo la validación de OBSERVADO y dime qué tarea sigue."`
   - *Alternativa rápida por terminal (sin MCP):* `gh issue create --title "S1-01 Inicializar backend FastAPI + SQLite" --label "semana-1"`.

---

## 4. Criterio de Cierre Semanal (Checklist de Control Personal)

Antes de dar por cerrada cada semana en tu tablero `Esta Semana -> Hecho`, confirma estos 4 puntos rápidos:
- [ ] El flujo de la semana se puede recorrer completo desde el navegador usando únicamente la barra `DemoRoleBar` (`RN-04`).
- [ ] Ningún cálculo de tarifas usa punto flotante y las transiciones respetan las reglas de [TRD.md](./TRD.md) (`RN-01`..`RN-05`, `RNF-03`).
- [ ] La base local `backend/utb_proto.db` y la carpeta `backend/storage/certificados/` persisten los datos tras reiniciar FastAPI (`RNF-01`, `RNF-02`).
- [ ] La suite documental sigue intacta ejecutando `python -m unittest tests/test_docs_suite.py -v`.
