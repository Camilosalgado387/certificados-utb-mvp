import hashlib
import pathlib
import re
import unittest
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "Docs"
ORIG_SPEC = ROOT / "Planificación certificados utb.md"
ORIG_SPEC_SHA256 = "b2a7a8b525060fa45b909b7335fa59a438b3329200811ca488cfa70e16299cde"


class TestOriginalSpecImmutability(unittest.TestCase):
    def test_original_spec_untouched(self):
        self.assertTrue(ORIG_SPEC.exists(), "El documento fuente institucional debe existir")
        digest = hashlib.sha256(ORIG_SPEC.read_bytes()).hexdigest()
        self.assertEqual(
            digest,
            ORIG_SPEC_SHA256,
            "Planificación certificados utb.md no debe modificarse",
        )


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
        for state in [
            "PENDIENTE_PAGO",
            "EN_ELABORACION",
            "EN_CONSULTA_OPT",
            "ENTREGADO",
            "EXPIRADO",
            "PENDIENTE",
            "OBSERVADO",
            "PDF_LISTO",
        ]:
            self.assertIn(state, self.text)
        self.assertIn("48 horas", self.text)
        self.assertRegex(self.text, r"(?i)entrega [uú]nica consolidada")
        self.assertRegex(self.text, r"(?i)lugar de expedici[oó]n")


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


if __name__ == "__main__":
    unittest.main()
