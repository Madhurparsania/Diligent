#!/usr/bin/env python3
"""
Batch-ingest source files into a SQLite database with metadata support.
Uses only Python's standard library for portability.
"""

import argparse
import hashlib
import json
import os
import sqlite3
from datetime import datetime, timezone
from typing import Dict, Iterable, Optional

EXTENSION_LANG_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".java": "Java",
    ".cs": "C#",
    ".cpp": "C++",
    ".c": "C",
    ".rb": "Ruby",
    ".go": "Go",
    ".php": "PHP",
    ".rs": "Rust",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".m": "Objective-C",
    ".scala": "Scala",
    ".sql": "SQL",
    ".html": "HTML",
    ".css": "CSS",
    ".json": "JSON",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".md": "Markdown",
}


def infer_language(path: str) -> Optional[str]:
    return EXTENSION_LANG_MAP.get(os.path.splitext(path)[1].lower())


def compute_checksum(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def safe_read_text(path: str) -> str:
    """Read file using utf-8 with fallback encodings."""
    encodings = ["utf-8", "utf-8-sig", "latin-1"]
    for enc in encodings:
        try:
            with open(path, "r", encoding=enc) as fh:
                return fh.read()
        except UnicodeDecodeError:
            continue
    with open(path, "rb") as fh:
        return fh.read().decode("utf-8", errors="ignore")


SCHEMA_SQL = open(os.path.join(os.path.dirname(__file__), "schema.sql"), "r", encoding="utf-8").read()


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_SQL)
    conn.commit()


def upsert_file(
    conn: sqlite3.Connection,
    root_dir: str,
    file_path: str,
    metadata: Optional[Dict[str, str]] = None,
) -> None:
    metadata = metadata or {}
    abs_path = os.path.abspath(file_path)
    rel_path = os.path.relpath(abs_path, root_dir)
    filename = os.path.basename(abs_path)
    extension = os.path.splitext(filename)[1].lower()
    stat = os.stat(abs_path)
    last_modified = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()
    file_size = stat.st_size

    raw_bytes = None
    content = None
    try:
        raw_bytes = open(abs_path, "rb").read()
        content = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        content = safe_read_text(abs_path)
        raw_bytes = content.encode("utf-8", errors="ignore")
    checksum = compute_checksum(raw_bytes)

    language = metadata.get("language") or infer_language(filename)
    tags = metadata.get("tags")
    author = metadata.get("author")
    date_added = metadata.get("date_added") or datetime.now(tz=timezone.utc).isoformat()

    conn.execute(
        """
        INSERT INTO code_files (
            filename, rel_path, abs_path, extension, language,
            author, tags, date_added, last_modified,
            file_size_bytes, checksum_sha256, content
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(abs_path) DO UPDATE SET
            extension = excluded.extension,
            language = COALESCE(excluded.language, code_files.language),
            author = COALESCE(excluded.author, code_files.author),
            tags = COALESCE(excluded.tags, code_files.tags),
            date_added = code_files.date_added,
            last_modified = excluded.last_modified,
            file_size_bytes = excluded.file_size_bytes,
            checksum_sha256 = excluded.checksum_sha256,
            content = excluded.content;
        """,
        (
            filename,
            rel_path,
            abs_path,
            extension,
            language,
            author,
            tags if isinstance(tags, str) else json.dumps(tags) if tags else None,
            date_added,
            last_modified,
            file_size,
            checksum,
            content,
        ),
    )

    file_id = conn.execute(
        "SELECT id FROM code_files WHERE abs_path = ?", (abs_path,)
    ).fetchone()[0]
    extra_attrs = metadata.get("attributes") or {}
    for key, value in extra_attrs.items():
        conn.execute(
            """
            INSERT INTO file_attributes (file_id, attr_key, attr_value)
            VALUES (?, ?, ?)
            ON CONFLICT(file_id, attr_key)
            DO UPDATE SET attr_value = excluded.attr_value;
            """,
            (file_id, key, json.dumps(value) if isinstance(value, (dict, list)) else value),
        )


def ingest_files(
    db_path: str,
    file_paths: Iterable[str],
    metadata_by_path: Optional[Dict[str, Dict[str, str]]] = None,
    project_root: Optional[str] = None,
) -> None:
    metadata_by_path = metadata_by_path or {}
    project_root = project_root or os.path.commonpath(file_paths)
    os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        init_db(conn)

        for fp in file_paths:
            if not os.path.isfile(fp):
                print(f"Skipping non-file path: {fp}")
                continue
            try:
                upsert_file(conn, project_root, fp, metadata_by_path.get(os.path.abspath(fp)))
                conn.commit()
                print(f"Ingested: {fp}")
            except Exception as exc:
                conn.rollback()
                print(f"Failed to ingest {fp}: {exc}")


def parse_args():
    parser = argparse.ArgumentParser(description="Ingest code files into SQLite.")
    parser.add_argument("files", nargs="+", help="Paths to code files to ingest.")
    parser.add_argument("--db", default="code_archive.db", help="SQLite database file.")
    parser.add_argument("--metadata-json", help="Path to JSON file mapping absolute paths to metadata.")
    parser.add_argument("--root", help="Project root for computing relative paths.")
    return parser.parse_args()


def main():
    args = parse_args()
    metadata = {}
    if args.metadata_json:
        with open(args.metadata_json, "r", encoding="utf-8") as fh:
            metadata = json.load(fh)
    ingest_files(args.db, args.files, metadata, args.root)


if __name__ == "__main__":
    main()

