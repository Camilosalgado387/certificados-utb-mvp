# Documentación Ligera del Prototipo MVP — Certificados UTB Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rellenar `Docs/TRD.md`, `Docs/ARCHITECTURE.md`, `Docs/IMPLEMENTATION-PLAN.md` y `Docs/README.md` con documentación breve, clara y 100% enfocada en el Prototipo MVP individual (4 semanas), manteniendo intacto `Planificación certificados utb.md`.

**Architecture:** Cuatro documentos cortos (lectura de 3 a 5 minutos cada uno) diseñados para un único desarrollador trabajando a tiempo parcial: `TRD.md` fija 5 reglas de negocio, 10 requerimientos funcionales y 5 no funcionales del MVP; `ARCHITECTURE.md` aterriza un stack local sin infraestructura pesada (Next.js + FastAPI + SQLAlchemy con SQLite/PostgreSQL + carpeta local `storage/certificados/`); `IMPLEMENTATION-PLAN.md` organiza un cronograma semanal de 4 semanas sincronizable con GitHub Projects/Issues (vía MCP o CLI); y `README.md` sirve de índice rápido. Una prueba ligera en Python (`tests/test_docs_suite.py`) verifica que los archivos sean concisos, consistentes y que el documento raíz no se altere.

**Tech Stack:** Markdown + Mermaid; Python 3.13 (`unittest` para validación rápida). Stack objetivo del prototipo: Next.js (React + TypeScript), FastAPI + SQLAlchemy, SQLite local (compatible con PostgreSQL vía `DATABASE_URL`) y sistema de archivos local (`backend/storage/certificados/`).

**Spec:** `Planificación certificados utb.md`

## Global Constraints

- **Documento original intacto:** `Planificación certificados utb.md` **NO se modifica**.
- **Cero infraestructura pesada en el prototipo:** Prohibido incluir buckets S3/MinIO, Celery, Redis, servidores SMTP externos o integraciones reales con Banner/SSO Microsoft dentro de la arquitectura activa del prototipo. Los PDFs se guardan en una carpeta local (`backend/storage/certificados/`) junto con su hash `SHA-256` en base de datos, y las notificaciones se guardan en base de datos para verse dentro de la misma app.
- **Brevedad para trabajo individual:** Cada archivo en `Docs/` debe mantenerse directo y escaneable (entre 70 y 180 líneas por archivo, sin relleno académico ni burocracia).
- **Reglas de negocio esenciales del MVP (`RN-01`..`RN-05`):**
  - `RN-01` **Subida manual por Registro Académico:** El software **no** genera los PDFs; la auxiliar los elabora/verifica externamente (evitando errores reales como lugar de expedición equivocado o diferencias de créditos entre avance e historia académica) y sube el archivo PDF de cada ítem.
  - `RN-02` **Entrega única consolidada:** Si un carrito tiene varios certificados, se entregan todos juntos en una sola notificación y se habilitan en el Historial únicamente cuando el **100% de los ítems** tienen su PDF cargado; el tiempo estimado del radicado usa el SLA más largo del carrito.
  - `RN-03` **Pago previo referenciado (48h) sin comprobantes:** Primero se radica el carrito generando referencia única con vigencia de 48 horas; el pago se aprueba con un botón simulador o un clic en Tesorería, sin subir soportes.
  - `RN-04` **Modo Demo Multirrol:** Una barra superior permite cambiar en un clic entre `Estudiante/Egresado`, `Tesorería`, `Registro Académico` y `Dirección de Programa` sin pantallas de login complejas.
  - `RN-05` **Historial con vigencia y contador de re-descargas:** El estudiante puede re-descargar sus certificados mientras no superen su `fecha_vigencia`, sumando cada clic al contador de telemetría.

## Review Focus

1. **Inconsistencia en datos o créditos detectada por la auxiliar:** Registro Académico debe poder marcar un ítem como `OBSERVADO` (ej. error en lugar de expedición o créditos avance vs. historia) o enviarlo a `EN_CONSULTA_OPT` (Dirección de Programa) antes de subir el PDF definitivo (*validado en Task 1*).
2. **Carrito con varios certificados donde solo se ha subido 1 PDF:** El radicado permanece en `EN_ELABORACION` mostrando avance parcial (`1 de N listos`), sin disparar la entrega ni permitir descarga hasta subir todos los PDFs (*validado en Task 1 y Task 2*).
3. **Orden de pago que supera las 48 horas sin confirmación:** El radicado pasa a `EXPIRADO` impidiendo su paso a Registro Académico (*validado en Task 1*).
4. **Intento de re-descargar un certificado con `fecha_vigencia` vencida:** El botón de descarga aparece deshabilitado en el Historial indicando que perdió vigencia (*validado en Task 1*).
5. **Sobrecarga accidental de alcance o infraestructura:** Ningún documento del prototipo debe exigir configurar Docker multi-contenedor obligatorio, buckets S3/MinIO ni colas Redis/Celery para correr localmente (*validado en Task 2*).

---

## File Structure

- **Create:** `tests/test_docs_suite.py` — Validación ligera de estructura, concisión, exclusión de buckets/colas, reglas del MVP y enlaces válidos.
- **Modify:** `Docs/TRD.md` — Requisitos funcionales (`RF-01..10`), no funcionales (`RNF-01..05`), roles Demo, reglas `RN-01..05` y estados del prototipo MVP.
- **Modify:** `Docs/ARCHITECTURE.md` — Arquitectura ligera (Next.js + FastAPI + SQLite/PostgreSQL + carpeta local de PDFs), 2 diagramas Mermaid, 5 tablas de BD y endpoints REST del MVP.
- **Modify:** `Docs/IMPLEMENTATION-PLAN.md` — Planificación práctica de **4 semanas** con tareas semanales en checkboxes y guía corta para llevar el tablero en **GitHub Projects / Issues (MCP)**.
- **Modify:** `Docs/README.md` — Resumen de 1 página del proyecto y orden de lectura.

---

### Task 1: Requisitos Ligeros del Prototipo MVP (`Docs/TRD.md`)

**Files:**
- Create: `tests/test_docs_suite.py`
- Modify: `Docs/TRD.md`
- Test: `tests/test_docs_suite.py`

**Interfaces:**
- Consumes: Flujo To-Be de `Planificación certificados utb.md` acotado al MVP demostrativo.
- Produces:
  - Reglas `RN-01` a `RN-05`.
  - Requerimientos Funcionales `RF-01` a `RF-10` y No Funcionales `RNF-01` a `RNF-05`.
  - Estados del radicado: `PENDIENTE_PAGO`, `EN_ELABORACION`, `EN_CONSULTA_OPT`, `ENTREGADO`, `EXPIRADO`.
  - Estados del ítem: `PENDIENTE`, `OBSERVADO`, `EN_CONSULTA_OPT`, `PDF_LISTO`.

- [ ] **Step 1: Crear `tests/test_docs_suite.py` con las pruebas para `Docs/TRD.md` y la inmutabilidad del doc original**

```python
import hashlib
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "Docs"
ORIG_SPEC = ROOT / "Planificación certificados utb.md"


class TestLeanTRD(unittest.TestCase):
    def setUp(self):
        self.text = (DOCS / "TRD.md").read_text(encoding="utf-8")

    def test_concise_length_and_sections(self):
        lines = self.text.splitlines()
        self.assertGreaterEqual(len(lines), 70, "TRD.md no debe estar vacío")
        self.assertLessEqual(len(lines), 200, "TRD.md debe ser corto y manejable para 1 persona")
        for section in [
            "## 1. Objetivo y Alcance del Prototipo (MVP)",
            "## 2. Roles en Modo Demo",
            "## 3. Reglas de Negocio Esenciales",
            "## 4. Estados del Trámite",
            "## 5. Requerimientos Funcionales (MVP)",
            "## 6. Requerimientos No Funcionales (MVP)",
        ]:
            self.assertIn(section, self.text)

    def test_mvp_ids_and_edge_cases(self):
        for i in range(1, 6):
            self.assertRegex(self.text, rf"\bRN-{i:02d}\b")
        for i in range(1, 11):
            self.assertRegex(self.text, rf"\bRF-{i:02d}\b")
        for i in range(1, 6):
            self.assertRegex(self.text, rf"\bRNF-{i:02d}\b")
        for state in ["PENDIENTE_PAGO", "EN_ELABORACION", "EN_CONSULTA_OPT", "ENTREGADO", "EXPIRADO", "OBSERVADO", "PDF_LISTO"]:
            self.assertIn(state, self.text)
        self.assertIn("48 horas", self.text)
        self.assertRegex(self.text, r"(?i)entrega [uú]nica consolidada")
        self.assertRegex(self.text, r"(?i)lugar de expedici[oó]n")
```

- [ ] **Step 2: Ejecutar la prueba y verificar que falla porque `Docs/TRD.md` está vacío**

Run: `python -m unittest tests/test_docs_suite.py -v`
Expected: FAIL (`AssertionError: 0 not greater than or equal to 70`)

- [ ] **Step 3: Redactar `Docs/TRD.md` (entre 90 y 170 líneas, claro y directo)**

Incluir en `Docs/TRD.md`:
1. **Objetivo y Alcance del Prototipo (MVP):** Qué incluye el prototipo y lista explícita de **Fuera de alcance** (sin SSO real, sin Banner real, sin pasarela bancaria real, sin buckets S3/MinIO, sin colas Redis/Celery).
2. **Roles en Modo Demo:** Barra selectora superior con `Estudiante / Egresado` (perfiles precargados), `Tesorería`, `Auxiliar de Registro Académico` y `Dirección de Programa`.
3. **Reglas de Negocio (`RN-01`..`RN-05`):** Tal como están fijadas en Global Constraints, incluyendo los casos borde de `OBSERVADO` (errores de lugar de expedición o créditos avance vs. historia), carrito parcial (`1 de N`), vencimiento a las `48 horas` (`EXPIRADO`) y bloqueo de re-descarga cuando vence `fecha_vigencia`.
4. **Estados del Trámite:** Tabla corta para Radicado (`PENDIENTE_PAGO`, `EN_ELABORACION`, `EN_CONSULTA_OPT`, `ENTREGADO`, `EXPIRADO`) e Ítem (`PENDIENTE`, `OBSERVADO`, `EN_CONSULTA_OPT`, `PDF_LISTO`).
5. **Requerimientos Funcionales (`RF-01`..`RF-10`):**
   - `RF-01`: Selector de rol y perfil en Modo Demo (activo vs. egresado).
   - `RF-02`: Catálogo tarifario dinámico (costo, días hábiles SLA, días de vigencia).
   - `RF-03`: Carrito múltiple y generación de `Numero_Radicado` + orden de pago (vigencia 48 horas, SLA = máximo del carrito).
   - `RF-04`: Simulación de pago aprobado en 1 clic (desde vista Estudiante o confirmación manual en Tesorería, sin subir comprobantes).
   - `RF-05`: Bandeja de Registro Académico ordenada por fecha límite SLA.
   - `RF-06`: Solicitud de insumo opcional (`EN_CONSULTA_OPT`) a Dirección de Programa y marcación `OBSERVADO` por discrepancias de datos/créditos.
   - `RF-07`: Carga manual de PDF por cada ítem del carrito a cargo de la auxiliar, guardando `SHA-256` y marcando `PDF_LISTO`.
   - `RF-08`: Cierre y **entrega única consolidada** automática al llegar al 100% de ítems `PDF_LISTO`.
   - `RF-09`: Bandeja de notificaciones dentro de la app (Notificaciones #1 radicado, #2 pago confirmado, #3 certificados listos) y rastreador de estado.
   - `RF-10`: Historial de certificados con botón de re-descarga (solo si está vigente) y panel de 3 métricas básicas (trámites por estado, cumplimiento SLA y clics de re-descarga).
6. **Requerimientos No Funcionales (`RNF-01`..`RNF-05`):** Ejecución local simple sin servicios en la nube (`RNF-01`), guardado de PDFs en solo-lectura lógica + verificación `SHA-256` (`RNF-02`), cálculos de tarifas en enteros/decimales exactos COP (`RNF-03`), interfaz limpia y responsiva (`RNF-04`) y código modular listo para cambiar mocks por servicios reales a futuro (`RNF-05`).

- [ ] **Step 4: Ejecutar la prueba y verificar que pasa**

Run: `python -m unittest tests/test_docs_suite.py -v`
Expected: PASS

- [ ] **Step 5: Commit de la base del repositorio y `Docs/TRD.md`**

```bash
git add "Planificación certificados utb.md" Docs/TRD.md tests/test_docs_suite.py
git commit -m "docs(trd): add lean MVP requirements for solo prototype"
```

---

### Task 2: Arquitectura Simple sin Buckets (`Docs/ARCHITECTURE.md`)

**Files:**
- Modify: `Docs/ARCHITECTURE.md`
- Modify: `tests/test_docs_suite.py`
- Test: `tests/test_docs_suite.py`

**Interfaces:**
- Consumes: `RN-01..05`, `RF-01..10`, `RNF-01..05` y estados definidos en `Docs/TRD.md`.
- Produces:
  - Estructura de carpetas `frontend/` (Next.js) y `backend/` (FastAPI + SQLAlchemy + `backend/storage/certificados/`).
  - 5 tablas relacionales simples: `catalog_items`, `requests`, `request_items`, `documents`, `notifications`.
  - Endpoints REST base bajo `/api/...`.

- [ ] **Step 1: Añadir pruebas para `Docs/ARCHITECTURE.md` en `tests/test_docs_suite.py`**

```python
class TestLeanArchitecture(unittest.TestCase):
    def setUp(self):
        self.text = (DOCS / "ARCHITECTURE.md").read_text(encoding="utf-8")

    def test_concise_and_no_cloud_bloat(self):
        lines = self.text.splitlines()
        self.assertGreaterEqual(len(lines), 70)
        self.assertLessEqual(len(lines), 200)
        for tech in ["Next.js", "FastAPI", "SQLAlchemy", "SQLite", "PostgreSQL", "storage/certificados"]:
            self.assertIn(tech, self.text)
        # No exigir buckets ni colas pesadas como componentes activos
        self.assertNotIn("MinIO", self.text)
        self.assertNotIn("Celery", self.text)

    def test_tables_endpoints_and_mermaid(self):
        for table in ["catalog_items", "requests", "request_items", "documents", "notifications"]:
            self.assertIn(table, self.text)
        blocks = re.findall(r"```mermaid\s*\n(.*?)```", self.text, flags=re.DOTALL)
        self.assertGreaterEqual(len(blocks), 2)
```

- [ ] **Step 2: Ejecutar las pruebas y verificar que fallan sobre `Docs/ARCHITECTURE.md` vacío**

Run: `python -m unittest tests/test_docs_suite.py -v`
Expected: FAIL en `TestLeanArchitecture`

- [ ] **Step 3: Redactar `Docs/ARCHITECTURE.md` (entre 90 y 170 líneas, práctico y visual)**

Incluir en `Docs/ARCHITECTURE.md`:
1. **Stack del Prototipo y Por Qué es Ligero:**
   - Frontend: **Next.js (App Router + TypeScript + Tailwind)** con barra de **Modo Demo Multirrol**.
   - Backend: **FastAPI + SQLAlchemy + Pydantic**.
   - Base de datos: **SQLite** en un archivo local `utb_proto.db` para desarrollo inmediato sin instalar nada, 100% compatible para apuntar a **PostgreSQL** cambiando `DATABASE_URL`.
   - Custodia de archivos PDF: Carpeta local `backend/storage/certificados/` nombrando cada PDF por UUID inmutable y guardando en la tabla `documents` los metadatos clave (`id_documento`, `numero_radicado`, `id_titular`, `tipo_certificado`, `fecha_expedicion`, `fecha_vigencia`, `hash_sha256`, `ruta_archivo`, `contador_redescargas`).
2. **Diagramas Mermaid (2 diagramas limpios):**
   - `flowchart LR`: Navegador (Next.js + Selector de Rol) ↔ API REST FastAPI ↔ Base de Datos (`SQLite / PostgreSQL`) y Carpeta Local (`storage/certificados/`).
   - `sequenceDiagram`: Flujo resumido Estudiante → Pago Simulado/Tesorería → Registro Académico (con consulta opcional `OPT` a Dirección de Programa) → Subida de PDFs (`1..N`) → Entrega Única Consolidada → Re-descarga en Historial.
3. **Modelo de Datos Mínimo (5 tablas):** `catalog_items`, `requests`, `request_items`, `documents` y `notifications` (explicadas en una lista corta de columnas principales).
4. **Endpoints REST Principales (`/api/...`) y Estructura de Carpetas:** Tabla de 8–10 endpoints claros y árbol corto de `frontend/` y `backend/`.

- [ ] **Step 4: Ejecutar las pruebas y verificar que pasan**

Run: `python -m unittest tests/test_docs_suite.py -v`
Expected: PASS

- [ ] **Step 5: Commit de `Docs/ARCHITECTURE.md`**

```bash
git add Docs/ARCHITECTURE.md tests/test_docs_suite.py
git commit -m "docs(architecture): add lightweight local prototype architecture without cloud buckets"
```

---

### Task 3: Plan Semanal de 4 Semanas + Guía GitHub MCP (`Docs/IMPLEMENTATION-PLAN.md` y `Docs/README.md`)

**Files:**
- Modify: `Docs/IMPLEMENTATION-PLAN.md`
- Modify: `Docs/README.md`
- Modify: `tests/test_docs_suite.py`
- Test: `tests/test_docs_suite.py`

**Interfaces:**
- Consumes: `Docs/TRD.md` y `Docs/ARCHITECTURE.md`.
- Produces:
  - Cronograma práctico de **Semana 1 a Semana 4** con checkboxes `- [ ]` listos para convertirse en Issues de GitHub Projects.
  - Configuración lista para usar del **MCP de GitHub** en `~/.gemini/config/mcp_config.json`.
  - Índice ejecutivo en `Docs/README.md`.

- [ ] **Step 1: Añadir pruebas para `IMPLEMENTATION-PLAN.md`, `README.md` e integridad de enlaces en `tests/test_docs_suite.py`**

```python
import urllib.parse


class TestWeeklyPlanAndReadme(unittest.TestCase):
    def test_four_week_plan_and_github_mcp_guide(self):
        plan = (DOCS / "IMPLEMENTATION-PLAN.md").read_text(encoding="utf-8")
        lines = plan.splitlines()
        self.assertGreaterEqual(len(lines), 70)
        self.assertLessEqual(len(lines), 200)
        for week in ["Semana 1", "Semana 2", "Semana 3", "Semana 4"]:
            self.assertIn(week, plan)
        self.assertIn("- [ ]", plan)
        self.assertIn("GitHub Projects", plan)
        self.assertIn("mcp_config.json", plan)

    def test_readme_and_valid_links_and_untouched_spec(self):
        readme = (DOCS / "README.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(readme.splitlines()), 35)
        self.assertLessEqual(len(readme.splitlines()), 110)
        # Verificar que el documento original conserva intacta la línea 100 original
        orig = ORIG_SPEC.read_text(encoding="utf-8")
        self.assertIn("VI. REQUISITOS FUNCIONALES Y NO FUNCIONALES\n\n## VI. PLAN DE IMPLEMENTACIÓN", orig)
        # Verificar enlaces locales válidos en Docs/
        link_re = re.compile(r"(?<!!)\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)")
        for md in [DOCS / "README.md", DOCS / "TRD.md", DOCS / "ARCHITECTURE.md", DOCS / "IMPLEMENTATION-PLAN.md"]:
            for raw in link_re.findall(md.read_text(encoding="utf-8")):
                if raw.startswith(("http://", "https://", "mailto:")):
                    continue
                target = (md.parent / urllib.parse.unquote(raw)).resolve()
                self.assertTrue(target.exists(), f"Enlace roto en {md.name}: {raw}")
```

- [ ] **Step 2: Ejecutar las pruebas y verificar que fallan sobre `IMPLEMENTATION-PLAN.md` y `README.md` vacíos**

Run: `python -m unittest tests/test_docs_suite.py -v`
Expected: FAIL en `TestWeeklyPlanAndReadme`

- [ ] **Step 3: Redactar `Docs/IMPLEMENTATION-PLAN.md` y `Docs/README.md`**

1. En `Docs/IMPLEMENTATION-PLAN.md` (entre 90 y 170 líneas):
   - **Ritmo de trabajo:** 4 semanas a tiempo parcial (1 persona), cerrando cada semana con algo visible y funcional en pantalla.
   - **Desglose semanal con checkboxes (`- [ ]`):**
     - **Semana 1 — Base del Proyecto, Mockup Base y Solicitud Estudiante (`RF-01..03`):** Inicializar `backend/` (FastAPI + SQLite) y `frontend/` (Next.js + barra Modo Demo), sembrar catálogo UTB, construir carrito múltiple y generar `Numero_Radicado` + orden de pago con vigencia de 48h.
     - **Semana 2 — Simulador de Pago, Tesorería y Bandejas Operativas (`RF-04..06`):** Botón *"Simular pago aprobado"* y vista Tesorería, cola priorizada de Registro Académico, marcación `OBSERVADO` (lugar de expedición / créditos) y consulta opcional `EN_CONSULTA_OPT` con Dirección de Programa.
     - **Semana 3 — Carga Manual de PDFs, Entrega Consolidada e Historial (`RF-07..09`):** Subida de PDF a `storage/certificados/` con hash `SHA-256`, regla de **entrega única consolidada** al completar todos los ítems del carrito, bandeja de notificaciones en la app y línea de tiempo del trámite.
     - **Semana 4 — Re-descarga con Telemetría, Métricas y Tus Ideas Nuevas (`RF-10`):** Historial con control de `fecha_vigencia` y contador de re-descargas, 3 tarjetas de métricas simples, pulido visual de punta a punta y espacio para iterar tus ideas propias del prototipo.
   - **Cómo llevar tu control semanal en GitHub Projects + MCP en Antigravity:** Bloque corto mostrando cómo crear un repositorio remoto en GitHub, activar un tablero Kanban (*Todo / Esta Semana / Hecho*) y el snippet JSON exacto para conectar el servidor MCP de GitHub en `~/.gemini/config/mcp_config.json` (para pedirle al agente *"crea los issues de la Semana 1"* o *"marca como terminada la tarea X"*).
2. En `Docs/README.md` (entre 45 y 90 líneas):
   - Qué es este prototipo en 5 líneas.
   - Mapa de archivos (`Planificación certificados utb.md` como visión institucional intacta, y `TRD.md`, `ARCHITECTURE.md`, `IMPLEMENTATION-PLAN.md` como guía ligera del prototipo).
   - Resumen de las 4 semanas y cuál es el primer paso para arrancar la Semana 1.

- [ ] **Step 4: Ejecutar toda la suite de validación y confirmar que todo está en verde**

Run: `python -m unittest tests/test_docs_suite.py -v`
Expected: PASS (6 tests OK, 0 enlaces rotos, documento original intacto)

- [ ] **Step 5: Commit final de `Docs/` completado**

```bash
git add Docs/IMPLEMENTATION-PLAN.md Docs/README.md tests/test_docs_suite.py Docs/superpowers/plans/2026-11-24-documentacion-ingenieria-certificados-utb.md
git commit -m "docs: add 4-week solo roadmap with GitHub MCP setup and Docs README"
```
