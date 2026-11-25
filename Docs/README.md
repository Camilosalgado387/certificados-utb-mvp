# Índice de Documentación — Prototipo MVP Certificados Académicos UTB

Punto de entrada técnico para construir en solitario el prototipo funcional del modelo unificado de solicitud, validación financiera, expedición y custodia post-entrega de certificados académicos de la Universidad Tecnológica de Bolívar (UTB).

## 1. Qué es este Prototipo (En 5 Líneas)

1. Es un **MVP 100% local y ligero** que demuestra de extremo a extremo el flujo propuesto de certificados académicos UTB sin depender de infraestructura en la nube ni integraciones pesadas.
2. Invierte el proceso fragmentado actual hacia **solicitud y liquidación previa al pago**, agrupando múltiples certificados en un solo carrito bajo un único `Numero_Radicado`.
3. Elimina el envío manual de comprobantes mediante una **referencia de pago con vigencia de 48 horas** y aprobación simulada en 1 clic desde Estudiante o Tesorería.
4. Articula sobre el mismo expediente a **4 roles en Modo Demo** (`Estudiante / Egresado`, `Tesorería`, `Auxiliar de Registro Académico` y `Dirección de Programa`).
5. Respeta la **subida manual verificada de PDFs** (`SHA-256`), aplica **entrega única consolidada** al completar el 100% del carrito y mide re-descargas dentro de `fecha_vigencia`.

---

## 2. Mapa de Archivos de Documentación

| Archivo | Rol en el Repositorio | Cuándo Usarlo |
| :--- | :--- | :--- |
| [Planificación certificados utb.md](../Planificación%20certificados%20utb.md) | **Visión institucional original (intacta):** Diagnóstico *As-Is*, proceso *To-Be*, custodia documental conceptual y KPIs. | Para consultar el sustento funcional institucional de la UTB sin alterar ni una línea del documento base. |
| [TRD.md](./TRD.md) | **Requisitos Técnicos del MVP:** Alcance local, 4 roles en Modo Demo, reglas `RN-01`..`RN-05`, estados y requisitos `RF-01`..`RF-10` / `RNF-01`..`RNF-05`. | Antes de implementar validaciones de negocio, vencimientos de 48h, entregas consolidadas o casos borde. |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | **Arquitectura Ligera:** Stack `frontend/` (Next.js) + `backend/` (FastAPI, SQLAlchemy, SQLite `utb_proto.db` compatible con PostgreSQL) + `storage/certificados/`. | Al estructurar carpetas, crear las 5 tablas relacionales y programar los endpoints REST `/api/...`. |
| [IMPLEMENTATION-PLAN.md](./IMPLEMENTATION-PLAN.md) | **Hoja de Ruta de 4 Semanas:** Desglose semanal con checkboxes `- [ ]` y guía de **GitHub Projects** + servidor MCP de GitHub (`mcp_config.json`). | Al iniciar y cerrar cada semana para priorizar cortes verticales visibles y gestionar Issues desde Antigravity. |
| [tests/test_docs_suite.py](../tests/test_docs_suite.py) | **Suite Automatizada (`unittest`):** Comprueba el hash SHA-256 del documento fuente, concisión de guías, IDs del MVP e integridad de enlaces locales. | Después de cualquier cambio en `Docs/` para asegurar cero regresiones documentales. |

---

## 3. Resumen de las 4 Semanas (1 Desarrollador)

| Semana | Alcance (`TRD`) | Entregable Visible y Funcional al Cerrar la Semana |
| :--- | :--- | :--- |
| **Semana 1** | `RF-01` .. `RF-03` | Base `backend/` + `frontend/`, barra Modo Demo Multirrol, catálogo tarifario en `COP`, carrito múltiple y orden de pago vigente por **48 horas**. |
| **Semana 2** | `RF-04` .. `RF-06` | Botón *"Simular pago aprobado"*, vista Tesorería sin recibos, cola SLA de Registro Académico, marcación `OBSERVADO` y consulta opcional `EN_CONSULTA_OPT`. |
| **Semana 3** | `RF-07` .. `RF-09` | Carga manual de PDFs a `backend/storage/certificados/` con `SHA-256`, **entrega única consolidada** (`N de N`), notificaciones in-app y línea de tiempo. |
| **Semana 4** | `RF-10` + Ideas | Historial con validación de `fecha_vigencia` y `contador_redescargas`, 3 tarjetas de métricas simples, semillas de casos borde y tus ideas propias. |

---

## 4. Reglas Esenciales del Dominio a Respetar

- **Subida manual verificada (`RN-01`):** El sistema no autogenera PDFs; Registro Académico revisa datos sensibles (ej. **lugar de expedición** y cruce de créditos) y carga cada archivo manualmente.
- **Entrega única consolidada (`RN-02`):** El radicado hereda el SLA más largo del carrito y retiene descargas parciales (`1 de N`) hasta que el `100%` de los ítems esté en `PDF_LISTO`.
- **Pago previo de 48h sin soportes (`RN-03`):** Primero se liquida el carrito (`PENDIENTE_PAGO`); superar **48 horas** sin pago anula la referencia en `EXPIRADO`.
- **Modo Demo sin infraestructura pesada (`RN-04`, `RNF-01`):** Sin SSO real, Banner, PSE, S3/MinIO, Celery ni SMTP; todo corre en local con cambio instantáneo de rol y diseño modular (`RNF-05`).
- **Custodia inmutable y vigencia (`RN-05`, `RNF-02`):** Archivos UUID en solo-lectura lógica verificados por `SHA-256`, bloqueando la re-descarga cuando `fecha_actual > fecha_vigencia`.

---

## 5. Primer Paso para Arrancar Hoy la Semana 1

1. **Valida la suite documental desde la raíz del proyecto:**
   ```powershell
   python -m unittest tests/test_docs_suite.py -v
   ```
2. **Prepara tu tablero semanal en GitHub Projects + MCP:**
   - Crea un tablero Kanban con 3 columnas (`Todo`, `Esta Semana`, `Hecho`) y añade el bloque `github` en `~/.gemini/config/mcp_config.json` siguiendo la sección 3 de [IMPLEMENTATION-PLAN.md](./IMPLEMENTATION-PLAN.md).
   - Pídele al agente en Antigravity crear los issues `S1-01` a `S1-06` y mueve esos 6 tickets a `Esta Semana`.
3. **Ejecuta tu primer bloque de código (`S1-01` y `S1-02`):**
   - Crea `backend/app/` y `backend/storage/certificados/` conforme al árbol de [ARCHITECTURE.md](./ARCHITECTURE.md).
   - Configura FastAPI + SQLAlchemy (`sqlite:///./utb_proto.db`) levantando las 5 tablas (`catalog_items`, `requests`, `request_items`, `documents`, `notifications`) con precios enteros en `COP` (`RNF-03`).
4. **Completa el corte vertical de la Semana 1 (`S1-03` a `S1-06`):**
   - Siembra el catálogo tarifario UTB (`GET /api/catalog`) y verifica la respuesta JSON desde `http://localhost:8000/docs`.
   - Levanta `frontend/` en Next.js (`http://localhost:3000`) con `DemoRoleBar` persistente en la parte superior.
   - Radica en pantalla tu primer carrito múltiple (`POST /api/requests`) comprobando el estado inicial `PENDIENTE_PAGO` y su vigencia de 48 horas.

---

## 6. Guía Rápida de Estados, Tablas y Notificaciones

- **Cinco tablas del modelo (`backend/app/models.py`):** `catalog_items`, `requests`, `request_items`, `documents` y `notifications`.
- **Estados del radicado (`requests`):** `PENDIENTE_PAGO` -> `EN_ELABORACION` <-> `EN_CONSULTA_OPT` -> `ENTREGADO` | `EXPIRADO`.
- **Estados por certificado (`request_items`):** `PENDIENTE` -> `OBSERVADO` / `EN_CONSULTA_OPT` -> `PDF_LISTO`.
- **Hitos de notificación (`notifications`):** `NOTIF_1_RADICADO` (orden y referencia 48h), `NOTIF_2_PAGO` (ingreso a cola SLA) y `NOTIF_3_ENTREGADO` (entrega consolidada lista).

---

## 7. Evolución Posterior al Prototipo (`RNF-05`)

- Cuando se apruebe pasar del MVP local a un piloto institucional UTB, bastará cambiar `DATABASE_URL` hacia **PostgreSQL** y reemplazar de forma aislada los adaptadores simulados de sesión, pago y almacenamiento sin reescribir las reglas `RN-01`..`RN-05`.
