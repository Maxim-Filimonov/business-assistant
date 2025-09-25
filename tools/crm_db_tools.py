"""CRM database tools providing SQLite-backed storage with markdown exports."""

from __future__ import annotations

import difflib
import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

from crewai.tools import BaseTool


DEFAULT_DB_PATH = Path("data/clients.db")
DEFAULT_EXPORT_DIR = Path("exports/clients")
LEGACY_MARKDOWN_PATH = Path("data/clients.md")


def _ensure_directories(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _slugify(value: str) -> str:
    """Return a filesystem-safe slug for the provided value."""

    safe = [c.lower() if c.isalnum() else "-" for c in value.strip()]
    slug = "".join(safe)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-") or "client"


def _render_markdown(client: Dict[str, Any]) -> str:
    """Render a markdown snapshot for a client record."""

    lines = [
        f"# Client: {client['name']}",
        f"- Parent: {client.get('parent') or 'Not specified'}",
        f"- Phone: {client.get('phone') or 'Not specified'}",
        f"- Email: {client.get('email') or 'Not specified'}",
    ]

    notes = client.get("notes")
    if notes:
        lines.extend(["", "## Notes"])
        for note_line in notes.splitlines():
            if note_line.strip():
                lines.append(f"- {note_line.strip()}")

    return "\n".join(lines).strip() + "\n"


def _dict_from_row(row: sqlite3.Row) -> Dict[str, Any]:
    return {
        "id": row["id"],
        "name": row["name"],
        "parent": row["parent"],
        "phone": row["phone"],
        "email": row["email"],
        "notes": row["notes"],
        "updated_at": row["updated_at"],
    }


def _normalize_notes(value: Any) -> Optional[str]:
    """Convert arbitrary note payloads to a normalized string."""

    if value is None:
        return None
    if isinstance(value, str):
        return value.strip() or None
    if isinstance(value, (list, tuple, set)):
        lines = [str(item).strip() for item in value if str(item).strip()]
        return "\n".join(lines) or None
    return str(value)


def _initialise_schema(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            parent TEXT,
            phone TEXT,
            email TEXT,
            notes TEXT,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )


def _maybe_import_legacy_markdown(conn: sqlite3.Connection) -> None:
    """Populate the database from the legacy markdown file if available."""

    if not LEGACY_MARKDOWN_PATH.exists():
        return

    cursor = conn.execute("SELECT COUNT(1) FROM clients")
    (count,) = cursor.fetchone()
    if count:
        return

    try:
        from tools.markdown_tools import ClientParser
    except Exception:
        return

    content = LEGACY_MARKDOWN_PATH.read_text(encoding="utf-8")
    parser = ClientParser()
    clients = parser._run(content=content)  # type: ignore[attr-defined]

    for client in clients.values():
        notes = "\n".join(client.get("raw_data", [])) if client.get("raw_data") else None
        conn.execute(
            """
            INSERT OR IGNORE INTO clients (name, parent, phone, email, notes)
            VALUES (:name, :parent, :phone, :email, :notes)
            """,
            {
                "name": client.get("name") or "Unknown",
                "parent": client.get("parent"),
                "phone": client.get("phone"),
                "email": client.get("email"),
                "notes": notes,
            },
        )


@dataclass(slots=True)
class _CRMContext:
    """Shared helpers for CRM tools."""

    db_path: Path = DEFAULT_DB_PATH
    export_dir: Path = DEFAULT_EXPORT_DIR

    def connection(self) -> sqlite3.Connection:
        _ensure_directories(self.db_path)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        _initialise_schema(conn)
        _maybe_import_legacy_markdown(conn)
        return conn

    def export_markdown(self, client: Dict[str, Any]) -> Path:
        """Write the client's markdown snapshot to disk."""

        export_dir = self.export_dir
        export_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{_slugify(client['name']) or 'client'}.md"
        export_path = export_dir / filename
        export_path.write_text(_render_markdown(client), encoding="utf-8")
        return export_path


class CRMClientReader(BaseTool):
    """Read clients from the SQLite database."""

    name: str = "CRM Client Reader"
    description: str = (
        "Read client records from the local SQLite CRM database. "
        "Provide an optional 'name' parameter for case-insensitive lookup."
    )

    def __init__(
        self,
        db_path: Path | str = DEFAULT_DB_PATH,
    ) -> None:
        super().__init__()
        self._context = _CRMContext(Path(db_path))

    def _run(self, name: Optional[str] = None) -> str:
        with self._context.connection() as conn:
            if name:
                row = conn.execute(
                    "SELECT * FROM clients WHERE lower(name) = lower(?)",
                    (name,),
                ).fetchone()
                if not row:
                    return json.dumps({"error": f"Client '{name}' not found"})
                return json.dumps(_dict_from_row(row), ensure_ascii=False, indent=2)

            rows = conn.execute("SELECT * FROM clients ORDER BY name COLLATE NOCASE").fetchall()
            clients = [_dict_from_row(row) for row in rows]
            return json.dumps(clients, ensure_ascii=False, indent=2)


class CRMClientDiffPreview(BaseTool):
    """Generate a diff preview for a proposed client upsert."""

    name: str = "CRM Client Diff Preview"
    description: str = (
        "Preview changes to a client's record without applying them. "
        "Provide a 'client' dictionary containing at least the client name, and "
        "optional fields to update (parent, phone, email, notes)."
    )

    def __init__(
        self,
        db_path: Path | str = DEFAULT_DB_PATH,
    ) -> None:
        super().__init__()
        self._context = _CRMContext(Path(db_path))

    def _run(self, client: Dict[str, Any]) -> str:
        if not isinstance(client, dict):
            return "Error: 'client' payload must be a dictionary."
        name = (client.get("name") or "").strip()
        if not name:
            return "Error: Client name is required for diff preview."

        with self._context.connection() as conn:
            existing_row = conn.execute(
                "SELECT * FROM clients WHERE lower(name) = lower(?)",
                (name,),
            ).fetchone()

        baseline = _dict_from_row(existing_row) if existing_row else None
        merged = baseline.copy() if baseline else {"name": name, "parent": None, "phone": None, "email": None, "notes": None}

        for key in ("parent", "phone", "email", "notes"):
            if key in client and client[key] is not None:
                merged[key] = _normalize_notes(client[key]) if key == "notes" else client[key]

        if "notes" not in client and baseline:
            merged["notes"] = baseline.get("notes")

        old_markdown = _render_markdown(baseline) if baseline else ""
        new_markdown = _render_markdown(merged)

        diff_lines = list(
            difflib.unified_diff(
                old_markdown.splitlines(),
                new_markdown.splitlines(),
                fromfile="current.md" if existing else "(new client)",
                tofile="proposed.md",
                lineterm="",
            )
        )

        if not diff_lines:
            return "No changes detected."

        return "\n".join(diff_lines)


class CRMClientApplyUpdate(BaseTool):
    """Apply a client upsert after review, exporting a markdown snapshot."""

    name: str = "CRM Client Apply Update"
    description: str = (
        "Persist approved client updates to the SQLite CRM database. "
        "Use the same payload reviewed via the diff preview."
    )

    def __init__(
        self,
        db_path: Path | str = DEFAULT_DB_PATH,
        export_dir: Path | str = DEFAULT_EXPORT_DIR,
    ) -> None:
        super().__init__()
        self._context = _CRMContext(Path(db_path), Path(export_dir))

    def _run(self, client: Dict[str, Any]) -> str:
        if not isinstance(client, dict):
            return "Error: 'client' payload must be a dictionary."
        name = (client.get("name") or "").strip()
        if not name:
            return "Error: Client name is required to apply updates."

        with self._context.connection() as conn:
            existing_row = conn.execute(
                "SELECT * FROM clients WHERE lower(name) = lower(?)",
                (name,),
            ).fetchone()

            baseline = _dict_from_row(existing_row) if existing_row else None
            record = baseline.copy() if baseline else {"name": name, "parent": None, "phone": None, "email": None, "notes": None}

            for key in ("parent", "phone", "email", "notes"):
                if key in client and client[key] is not None:
                    record[key] = _normalize_notes(client[key]) if key == "notes" else client[key]

            if "notes" not in client and baseline:
                record["notes"] = baseline.get("notes")

            old_markdown = _render_markdown(baseline) if baseline else ""
            new_markdown = _render_markdown(record)

            if baseline:
                conn.execute(
                    """
                    UPDATE clients
                    SET parent = :parent,
                        phone = :phone,
                        email = :email,
                        notes = :notes,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = :id
                    """,
                    {
                        "id": baseline["id"],
                        "parent": record.get("parent"),
                        "phone": record.get("phone"),
                        "email": record.get("email"),
                        "notes": record.get("notes"),
                    },
                )
            else:
                cursor = conn.execute(
                    """
                    INSERT INTO clients (name, parent, phone, email, notes)
                    VALUES (:name, :parent, :phone, :email, :notes)
                    """,
                    {
                        "name": record["name"],
                        "parent": record.get("parent"),
                        "phone": record.get("phone"),
                        "email": record.get("email"),
                        "notes": record.get("notes"),
                    },
                )
                record["id"] = cursor.lastrowid

            conn.commit()

        export_path = self._context.export_markdown(record)

        diff_lines = list(
            difflib.unified_diff(
                old_markdown.splitlines(),
                new_markdown.splitlines(),
                fromfile="current.md" if baseline else "(new client)",
                tofile="updated.md",
                lineterm="",
            )
        )
        diff = "\n".join(diff_lines) if diff_lines else "No changes detected."

        return (
            "Update applied successfully. Markdown snapshot saved to "
            f"{export_path}.\nDiff:\n{diff}"
        )


class CRMClientListMarkdownExporter(BaseTool):
    """Export markdown snapshots for all clients."""

    name: str = "CRM Markdown Exporter"
    description: str = (
        "Regenerate markdown exports for every client in the database. "
        "Returns the list of written files."
    )

    def __init__(
        self,
        db_path: Path | str = DEFAULT_DB_PATH,
        export_dir: Path | str = DEFAULT_EXPORT_DIR,
    ) -> None:
        super().__init__()
        self._context = _CRMContext(Path(db_path), Path(export_dir))

    def _run(self) -> str:
        written: Iterable[str]
        with self._context.connection() as conn:
            rows = conn.execute("SELECT * FROM clients ORDER BY name COLLATE NOCASE").fetchall()
            paths = []
            for row in rows:
                client = _dict_from_row(row)
                path = self._context.export_markdown(client)
                paths.append(str(path))
        written = paths
        return json.dumps(list(written), ensure_ascii=False, indent=2)


__all__ = [
    "CRMClientReader",
    "CRMClientDiffPreview",
    "CRMClientApplyUpdate",
    "CRMClientListMarkdownExporter",
]

