import asyncio
import json
import pathlib
import sys
import tempfile
import unittest

from sqlalchemy import create_engine, event, inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

ROOT = pathlib.Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.models import CatalogItem, RequestItem  # noqa: E402
from app.services.seed import DEMO_PROFILES, INITIAL_CATALOG, seed_catalog  # noqa: E402


def asgi_get(target_app, path: str) -> tuple[int, dict | list]:
    """Ejecuta una petición GET directa sobre la app ASGI sin requerir clientes HTTP externos."""

    async def _call():
        messages = []

        async def receive():
            return {"type": "http.request", "body": b"", "more_body": False}

        async def send(message):
            messages.append(message)

        scope = {
            "type": "http",
            "asgi": {"version": "3.0"},
            "http_version": "1.1",
            "method": "GET",
            "scheme": "http",
            "path": path,
            "raw_path": path.encode("utf-8"),
            "query_string": b"",
            "headers": [(b"host", b"localhost:8000")],
            "client": ("127.0.0.1", 50000),
            "server": ("127.0.0.1", 8000),
        }
        await target_app(scope, receive, send)
        start = next(m for m in messages if m["type"] == "http.response.start")
        body = b"".join(
            m.get("body", b"") for m in messages if m["type"] == "http.response.body"
        )
        return start["status"], json.loads(body.decode("utf-8"))

    return asyncio.run(_call())


class TestBackendS1(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        db_file = pathlib.Path(self.tmp_dir.name) / "test_utb.db"
        self.engine = create_engine(
            f"sqlite:///{db_file.as_posix()}",
            connect_args={"check_same_thread": False},
        )

        @event.listens_for(self.engine, "connect")
        def _fk_on(dbapi_conn, _rec):
            cur = dbapi_conn.cursor()
            cur.execute("PRAGMA foreign_keys=ON")
            cur.close()

        Base.metadata.create_all(bind=self.engine)
        self.TestingSession = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

        def _override_get_db():
            db = self.TestingSession()
            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = _override_get_db

    def tearDown(self):
        app.dependency_overrides.clear()
        self.engine.dispose()
        self.tmp_dir.cleanup()

    def test_five_tables_and_foreign_keys_enforced(self):
        tables = set(inspect(self.engine).get_table_names())
        self.assertEqual(
            tables,
            {
                "catalog_items",
                "requests",
                "request_items",
                "documents",
                "notifications",
            },
        )
        with self.TestingSession() as db:
            db.add(
                RequestItem(
                    request_id=9999,
                    catalog_item_id=9999,
                    precio_unitario_cop=18500,
                )
            )
            with self.assertRaises(IntegrityError):
                db.commit()

    def test_health_endpoint(self):
        status, payload = asgi_get(app, "/health")
        self.assertEqual(status, 200)
        self.assertEqual(payload["status"], "ok")
        self.assertTrue(payload["storage_ready"])

    def test_seed_idempotency_and_catalog_endpoint(self):
        with self.TestingSession() as db:
            seed_catalog(db)
            seed_catalog(db)
            self.assertEqual(db.query(CatalogItem).count(), len(INITIAL_CATALOG))
            # Desactivar uno para comprobar filtrado activo=True
            inactivo = (
                db.query(CatalogItem)
                .filter(CatalogItem.codigo == "CERT-CONDUCTA")
                .first()
            )
            inactivo.activo = False
            db.commit()

        status, items = asgi_get(app, "/api/catalog")
        self.assertEqual(status, 200)
        self.assertEqual(len(items), len(INITIAL_CATALOG) - 1)
        for item in items:
            self.assertIsInstance(item["precio_cop"], int)
            self.assertTrue(item["activo"])
        contenidos = next(i for i in items if i["codigo"] == "CERT-CONTENIDOS")
        self.assertTrue(contenidos["requiere_opt"])

    def test_demo_profiles_endpoint_covers_four_roles(self):
        status, profiles = asgi_get(app, "/api/catalog/demo-profiles")
        self.assertEqual(status, 200)
        self.assertEqual(len(profiles), len(DEMO_PROFILES))
        roles = {p["rol"] for p in profiles}
        self.assertEqual(roles, {"ESTUDIANTE", "TESORERIA", "REGISTRO", "DIRECCION"})
        titulares = {p["perfil_titular"] for p in profiles if p["rol"] == "ESTUDIANTE"}
        self.assertEqual(titulares, {"ESTUDIANTE", "EGRESADO"})


if __name__ == "__main__":
    unittest.main()
