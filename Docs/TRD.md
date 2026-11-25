# Documento de Requisitos Técnicos (TRD) — Prototipo MVP Certificados Académicos UTB

Especificación funcional y técnica ligera para construir, por un único desarrollador, el prototipo demostrativo (MVP) del modelo unificado de solicitud, validación financiera, expedición y custodia post-entrega de certificados académicos de la Universidad Tecnológica de Bolívar (UTB).

## 1. Objetivo y Alcance del Prototipo (MVP)

El prototipo demuestra de extremo a extremo el flujo propuesto ("solicitud y liquidación previa al pago") sobre un expediente único por radicado, eliminando la carga manual de comprobantes de pago y habilitando trazabilidad en vivo e historial de re-descarga con telemetría.

**Incluido en el MVP:**
- Catálogo tarifario dinámico con costos en COP, SLA en días hábiles y días de vigencia documental.
- Carrito múltiple de certificados y liquidación automática previa al pago bajo un único `Numero_Radicado`.
- Simulación de pago referenciado en 1 clic y conciliación directa sin adjuntar soportes ni recibos.
- Bandejas operativas conectadas para Tesorería, Registro Académico y Dirección de Programa.
- Subida manual de archivos PDF por ítem con huella `SHA-256`, entrega única consolidada, notificaciones dentro de la aplicación e historial con contador de re-descargas.

**Fuera de alcance en el MVP (infraestructura pesada excluida):**
- Sin inicio de sesión único (SSO) institucional real (Microsoft Entra ID / LDAP).
- Sin integración con Banner ni bases de datos académicas reales de la UTB.
- Sin pasarela bancaria o botón PSE real; el recaudo es 100% simulado en entorno local.
- Sin almacenamiento de objetos en la nube ni servidores S3 / MinIO (se usa carpeta local controlada).
- Sin colas de tareas asíncronas ni brokers externos (sin Celery, sin Redis).
- Sin servidor SMTP externo real; todas las notificaciones se consultan dentro de la aplicación.

## 2. Roles en Modo Demo

El prototipo reemplaza la autenticación tradicional por una **barra selectora superior persistente** que cambia la sesión activa en un clic entre cuatro vistas operativas:

| Rol en Selector | Perfiles Precargados | Acción Principal en el Prototipo |
| :--- | :--- | :--- |
| `Estudiante / Egresado` | Estudiante activo (pregrado) y Egresado | Armar carrito, radicar orden, simular pago en 1 clic, ver notificaciones/estado y re-descargar vigentes. |
| `Tesorería` | Analista de Servicios Financieros | Consultar referencias pendientes y confirmar pagos manualmente en 1 clic sin revisar comprobantes. |
| `Auxiliar de Registro Académico` | Auxiliar de Certificaciones | Atender cola ordenada por SLA, pedir insumo opcional, marcar observaciones y subir el PDF de cada ítem. |
| `Dirección de Programa` | Coordinación Académica | Responder sub-requerimientos opcionales (`OPT`) adjuntando notas o avales de plan de estudio/contenidos. |

## 3. Reglas de Negocio Esenciales

- **`RN-01` — Subida manual por Registro Académico:**
  El software **no** autogenera los certificados PDF. La auxiliar elabora y verifica cada documento externamente —previniendo errores reales como **lugar de expedición** equivocado o diferencias de créditos entre el avance de carrera y la historia académica— y sube manualmente el archivo PDF final de cada ítem del carrito.
- **`RN-02` — Entrega única consolidada:**
  Cuando un carrito agrupa varios certificados en un mismo radicado, la promesa de entrega del trámite adopta el **SLA más largo** entre los ítems seleccionados. Los documentos se habilitan al estudiante en una **entrega única consolidada** (una sola Notificación #3 y apertura simultánea en el Historial) únicamente cuando el **100% de los ítems** alcanzan el estado `PDF_LISTO`.
- **`RN-03` — Pago previo referenciado (48 horas) sin comprobantes:**
  Primero se radica el carrito generando un `Numero_Radicado` y una referencia única de pago con vigencia exacta de **48 horas**. El pago se aprueba mediante un botón simulador desde la vista Estudiante o con un clic en Tesorería, eliminando por completo la subida de pantallazos o recibos bancarios.
- **`RN-04` — Modo Demo Multirrol:**
  La barra superior permite alternar instantáneamente entre `Estudiante / Egresado` (activo o egresado), `Tesorería`, `Auxiliar de Registro Académico` y `Dirección de Programa` sobre el mismo expediente compartido, sin pantallas de login complejas.
- **`RN-05` — Historial con vigencia, contador de re-descargas y casos borde:**
  El titular puede re-descargar sin costo sus certificados entregados mientras la fecha actual no supere `fecha_vigencia`, sumando cada clic al contador de telemetría de uso. Casos borde controlados:
  - *Ítem `OBSERVADO`:* Si la auxiliar detecta discrepancias en revisión (ej. **lugar de expedición** erróneo en ficha o cruce desigual de créditos entre avance e historia académica), marca el ítem como `OBSERVADO` con motivo interno hasta corregirlo y subir el PDF válido.
  - *Carrito parcial (`1 de N` listos):* Mientras existan ítems pendientes (`1 de N` en `PDF_LISTO`), los archivos ya subidos permanecen retenidos sin descarga estudiantil hasta completar `N de N`.
  - *Vencimiento a las 48 horas (`EXPIRADO`):* Si transcurren **48 horas** desde la radicación sin confirmación financiera, el radicado pasa a `EXPIRADO` e impide pagos posteriores sobre esa referencia.
  - *Bloqueo por vencimiento documental:* Cuando la fecha actual supera `fecha_vigencia`, el sistema deshabilita el botón de re-descarga en el Historial e informa que debe tramitarse una nueva solicitud.

## 4. Estados del Trámite

### 4.1 Estados del Radicado (Cabecera del Expediente)

| Estado | Descripción Operativa |
| :--- | :--- |
| `PENDIENTE_PAGO` | Solicitud radicada con referencia activa (vigencia máxima de **48 horas**). |
| `EN_ELABORACION` | Pago confirmado; expediente habilitado en la cola de Registro Académico bajo reloj SLA. |
| `EN_CONSULTA_OPT` | Al menos un ítem espera respuesta de Dirección de Programa; visible en el rastreador del estudiante. |
| `ENTREGADO` | El 100% de los ítems está en `PDF_LISTO`; se ejecuta la entrega única consolidada y pasa al Historial. |
| `EXPIRADO` | Orden anulada automáticamente por superar **48 horas** sin confirmación de pago. |

### 4.2 Estados del Ítem (Por cada certificado del carrito)

| Estado | Descripción Operativa |
| :--- | :--- |
| `PENDIENTE` | Ítem pagado en espera de verificación y subida manual del archivo PDF por Registro Académico. |
| `OBSERVADO` | Ítem retenido por inconsistencia académica o registral en validación (ej. créditos o lugar de expedición). |
| `EN_CONSULTA_OPT` | Sub-requerimiento escalado a Dirección de Programa esperando insumo o validación académica. |
| `PDF_LISTO` | Archivo PDF cargado manualmente con huella `SHA-256` verificada, en espera de cierre consolidado. |

### 4.3 Transiciones Clave de Control

1. Radicar carrito crea el expediente en `PENDIENTE_PAGO` (Notificación #1) con vencimiento de **48 horas**.
2. Aprobar pago antes de **48 horas** pasa el radicado a `EN_ELABORACION` (Notificación #2) e inicializa sus ítems en `PENDIENTE`; superar el plazo sin pago lo cierra en `EXPIRADO`.
3. Si algún ítem pasa a `EN_CONSULTA_OPT`, la cabecera refleja `EN_CONSULTA_OPT` hasta recibir el insumo y volver a `EN_ELABORACION`.
4. Subir el último PDF pendiente (`100%` en `PDF_LISTO`) transita el radicado automáticamente a `ENTREGADO` (Notificación #3).

## 5. Requerimientos Funcionales (MVP)

- **`RF-01` — Selector de rol y perfil en Modo Demo:** Barra superior fija para alternar entre `Estudiante / Egresado` (con cambio rápido entre perfil activo y egresado), `Tesorería`, `Auxiliar de Registro Académico` y `Dirección de Programa`.
- **`RF-02` — Catálogo tarifario dinámico:** Listado configurable de certificados con costo exacto en COP, promesa de entrega en días hábiles (SLA) y días de vigencia administrativa.
- **`RF-03` — Carrito múltiple y orden de pago previa:** Agrupación de uno o varios certificados en una misma solicitud, liquidación automática del total y creación de `Numero_Radicado` + orden referenciada (vigencia **48 horas**, SLA del radicado = máximo del carrito).
- **`RF-04` — Simulación de pago aprobado en 1 clic:** Confirmación inmediata del recaudo desde el botón simulador del Estudiante o confirmación manual en Tesorería, sin subir comprobantes.
- **`RF-05` — Bandeja de Registro Académico por SLA:** Cola de trabajo de trámites pagados ordenada por fecha límite SLA más próxima, mostrando contador de avance de ítems (`PDF_LISTO / total`).
- **`RF-06` — Consulta opcional y marcación de observaciones:** Acción por ítem para escalar solicitud de insumo (`EN_CONSULTA_OPT`) a Dirección de Programa, registrar respuesta interna o marcar `OBSERVADO` por discrepancias de datos/créditos.
- **`RF-07` — Carga manual de PDF por ítem:** Subida individual de archivo `.pdf` por parte de la auxiliar, calculando y almacenando su hash `SHA-256`, `fecha_expedicion`, `fecha_vigencia` y estado `PDF_LISTO`.
- **`RF-08` — Cierre y entrega única consolidada automática:** Transición automática del radicado a `ENTREGADO` únicamente cuando el 100% de sus ítems están en `PDF_LISTO`, registrando la marca de cumplimiento SLA.
- **`RF-09` — Bandeja de notificaciones in-app y rastreador:** Centro de mensajes interno con las tres notificaciones transaccionales (#1 radicado y referencia, #2 pago confirmado, #3 certificados listos) y consultor visual de avance por `Numero_Radicado`.
- **`RF-10` — Historial de re-descarga y panel de 3 métricas:** Repositorio estudiantil con botón de re-descarga habilitado solo mientras `fecha_actual <= fecha_vigencia` (sumando clics de telemetría) y vista resumen con 3 indicadores: trámites por estado, cumplimiento SLA y total de re-descargas.

## 6. Requerimientos No Funcionales (MVP)

- **`RNF-01` — Ejecución local simple sin nube:** Operación autónoma en equipo local mediante SQLite y sistema de archivos local, sin dependencias de servicios cloud, colas externas ni contenedores pesados.
- **`RNF-02` — Custodia en solo-lectura lógica y `SHA-256`:** Los archivos PDF emitidos se resguardan en ruta local controlada impidiendo su reemplazo tras la entrega, verificando integridad mediante huella criptográfica `SHA-256`.
- **`RNF-03` — Cálculos monetarios exactos en COP:** Liquidación de tarifas unitarias y totales del carrito empleando enteros exactos o decimales de precisión fija en pesos colombianos (`COP`), sin punto flotante binario.
- **`RNF-04` — Interfaz limpia y responsiva:** Diseño web ligero, claro y adaptable a escritorio y dispositivos móviles para todas las bandejas y vistas del Modo Demo.
- **`RNF-05` — Código modular listo para evolución:** Arquitectura desacoplada por servicios/adaptadores que permita sustituir a futuro los mocks del MVP (identidad, pagos, correo y custodia local) por integraciones institucionales reales.
