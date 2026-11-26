# Reglas del Repositorio — Certificados Académicos UTB

## 1. Compuerta Obligatoria de Mockups Frontend (`<MOCKUP-GATE>`)

Antes de crear la aplicación `frontend/` o programar cualquier vista, pantalla, flujo o rediseño visual en **Next.js + TypeScript + Tailwind CSS**, el agente **DEBE** generar primero mockups navegables y recibir la aprobación explícita del usuario:

1. **Diseñar antes de programar (Cero código de producto sin aprobación):**
   - Está prohibido crear componentes en `frontend/src/`, instalar paquetes de UI o maquetar páginas definitivas mientras el mockup de esa vista no haya sido revisado y aprobado por el usuario.
   - *Excepción única:* Correcciones puntuales de bugs, textos o ajustes menores de una línea solicitados directamente sobre una vista ya aprobada.

2. **Cómo presentar los mockups para revisión:**
   - **Vía principal — Visual Companion (`brainstorming`):** Usar el servidor visual interactivo en el navegador (guardando las pantallas en `.superpowers/brainstorm/` con `--project-dir` para conservar el historial de iteraciones `*-v1.html`, `*-v2.html` y capturar selecciones del usuario). *Nota en Windows:* iniciar el servidor fuera del sandbox cuando el usuario deba abrir la URL local en su propio navegador.
   - **Vía alternativa — Prototipos HTML autocontenidos:** Si el usuario prefiere revisar archivos estáticos sin servidor, generar prototipos HTML previsualizables en `Docs/mockups/<vista>.html` listos para abrir directamente en el navegador.
   - **Fidelidad y contenido real:** Los mockups deben usar datos reales del dominio UTB (radicados, tarifas exactas en `COP`, roles del Modo Demo, estados SLA y tipos de certificados reales de `Docs/TRD.md`), nunca *lorem ipsum* ni plantillas genéricas.

3. **Iteración y paso a implementación:**
   - Presentar entre 2 y 3 alternativas claras cuando existan decisiones abiertas de distribución o estilo visual, iterar según el feedback del usuario y **solo tras su visto bueno explícito** pasar al plan e implementación en `frontend/`.

---

## 2. Uso Combinado de Skills de Diseño Frontend (`.agents/skills/`)

Al diseñar mockups o implementar interfaces en `frontend/`, combinar siempre las skills locales instaladas en `.agents/skills/`:

- **`ui-ux-pro-max`** (`.agents/skills/ui-ux-pro-max/SKILL.md`):
  - Ejecutar su buscador local con **`python`** (en Windows usar `python`, no `python3`):
    `python .agents/skills/ui-ux-pro-max/scripts/search.py "<consulta>" --design-system` (o `--domain ux`, `--stack nextjs`, `--stack html-tailwind`).
  - Usarla para fundamentar paleta accesible (contraste `>= 4.5:1`), pares tipográficos, densidad de tablas operativas (`--density`), validación de formularios y accesibilidad de teclado/foco.
- **`frontend-design`** (`.agents/skills/frontend-design/SKILL.md`):
  - Usarla como dirección estética para garantizar jerarquía visual intencional, tipografía con carácter institucional académico/administrativo, microinteracciones sobrias con propósito y cero apariencia de plantilla genérica de IA (*AI slop*).
- **Iconografía y activos:** Prohibido usar emojis como iconos estructurales de interfaz; emplear exclusivamente iconos vectoriales SVG consistentes (p. ej., `lucide-react` o `@phosphor-icons/react`) con `aria-hidden="true"` cuando acompañen texto visible.

---

## 3. Restricciones de Dominio en la Interfaz (MVP UTB)

Toda propuesta visual y componente en `frontend/` debe respetar `Docs/TRD.md` y `Docs/ARCHITECTURE.md`:

- **Barra persistente de Modo Demo Multirrol (`RF-01`, `RN-04`):** Cambio en 1 clic entre `Estudiante / Egresado` (activo o egresado), `Tesorería`, `Auxiliar de Registro Académico` y `Dirección de Programa`.
- **Exactitud monetaria (`RNF-03`):** Mostrar y calcular valores únicamente en pesos colombianos enteros (`COP`), sin decimales flotantes.
- **Trazabilidad y estados (`RN-01`..`RN-05`):** Representar con semántica visual inequívoca (no dependiente solo del color) los estados del radicado (`PENDIENTE_PAGO`, `EN_ELABORACION`, `EN_CONSULTA_OPT`, `ENTREGADO`, `EXPIRADO`) y de cada ítem (`PENDIENTE`, `OBSERVADO`, `EN_CONSULTA_OPT`, `PDF_LISTO`), incluyendo reloj de pago de 48h, avance `N de N` para entrega única consolidada y bloqueo por vencimiento documental.
- **Responsividad (`RNF-04`):** Diseño limpio, claro y adaptable tanto a escritorio (bandejas operativas) como a móvil (consulta y descarga estudiantil).
