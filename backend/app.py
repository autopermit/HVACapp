import csv
import io
import os
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, g, jsonify, request, Response
from flask_cors import CORS

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = os.environ.get("DATABASE_PATH", str(BASE_DIR / "submissions.db"))
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN")
ALLOWED_ORIGINS = [
    o.strip()
    for o in os.environ.get(
        "ALLOWED_ORIGINS",
        "https://hvacapp.us,https://www.hvacapp.us,https://autopermit.github.io,http://localhost:8000,http://127.0.0.1:8000",
    ).split(",")
    if o.strip()
]

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

REQUIRED_FIELDS = ["first_name", "last_name", "email", "phone", "company"]
OPTIONAL_FIELDS = ["license", "jurisdiction"]

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ALLOWED_ORIGINS}})


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            company TEXT NOT NULL,
            license TEXT,
            jurisdiction TEXT
        )
        """
    )
    db.commit()
    db.close()


def require_admin():
    if not ADMIN_TOKEN:
        return jsonify(error="admin_not_configured"), 503
    auth = request.headers.get("Authorization", "")
    if auth != f"Bearer {ADMIN_TOKEN}":
        return jsonify(error="unauthorized"), 401
    return None


@app.get("/api/health")
def health():
    return jsonify(status="ok")


@app.post("/api/early-access")
def create_submission():
    data = request.get_json(silent=True) or {}

    values = {}
    for field in REQUIRED_FIELDS:
        value = str(data.get(field) or "").strip()
        if not value:
            return jsonify(error=f"missing_field", field=field), 400
        values[field] = value

    if not EMAIL_RE.match(values["email"]):
        return jsonify(error="invalid_email"), 400

    for field in OPTIONAL_FIELDS:
        raw = data.get(field)
        values[field] = str(raw).strip() if raw else None

    db = get_db()
    db.execute(
        """
        INSERT INTO submissions
            (created_at, first_name, last_name, email, phone, company, license, jurisdiction)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.now(timezone.utc).isoformat(),
            values["first_name"],
            values["last_name"],
            values["email"],
            values["phone"],
            values["company"],
            values["license"],
            values["jurisdiction"],
        ),
    )
    db.commit()

    return jsonify(ok=True), 201


@app.get("/api/submissions")
def list_submissions():
    auth_error = require_admin()
    if auth_error:
        return auth_error

    db = get_db()
    rows = db.execute(
        "SELECT * FROM submissions ORDER BY id DESC"
    ).fetchall()
    return jsonify([dict(row) for row in rows])


@app.get("/api/submissions.csv")
def export_submissions_csv():
    auth_error = require_admin()
    if auth_error:
        return auth_error

    db = get_db()
    rows = db.execute("SELECT * FROM submissions ORDER BY id DESC").fetchall()

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    if rows:
        writer.writerow(rows[0].keys())
        for row in rows:
            writer.writerow(list(row))
    else:
        writer.writerow(
            ["id", "created_at", "first_name", "last_name", "email",
             "phone", "company", "license", "jurisdiction"]
        )

    return Response(
        buffer.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=submissions.csv"},
    )


init_db()


if __name__ == "__main__":
    app.run(debug=True, port=1990)
