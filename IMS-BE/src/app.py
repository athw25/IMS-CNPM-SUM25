from __future__ import annotations
import os
from flask import Flask
from create_app import create_app as _create_app
from config import AppConfig
from infrastructure.databases import db
from infrastructure.seeds import seed_demo

import click


app: Flask = _create_app()

@app.cli.command("db")
def _db():
    with app.app_context():
        db.create_all()
        print("DB: create_all done.")

@app.cli.command("seed")
def _seed():
    with app.app_context():
        seed_demo()
        print("DB: seed done.")

# ---------- Bootstrap khi khởi động server ----------
def _should_seed() -> bool:
    """
    Chỉ seed khi:
      - SEED_ON_START=1 (hoặc true), và
      - Chưa có Admin nào trong DB (idempotent guard)
    """
    if os.getenv("SEED_ON_START", "0").lower() not in ("1", "true", "yes"):
        return False

    try:
        # Tránh import vòng, import muộn trong app_context
        from .domain.models.identity import User  # type: ignore
        return User.query.filter_by(role="Admin").count() == 0
    except Exception:
        # Nếu lỗi trong lần chạy đầu tiên (chưa có bảng), cứ cho phép seed
        return True

def _bootstrap_if_needed():
    with app.app_context():
        if os.getenv("INIT_DB", "0").lower() in ("1", "true", "yes"):
            db.create_all()
            print("[INIT_DB] create_all done.")

        if _should_seed():
            seed_demo()
            print("[SEED_ON_START] demo data seeded.")

def main():
    cfg = AppConfig.load()
    with app.app_context():
        if cfg.INIT_DB == "1":
            db.create_all()
            print("INIT_DB=1: tables created.")
    app.run(host="0.0.0.0", port=cfg.PORT, debug=True)

if __name__ == "__main__" or os.getenv("RUN_BOOTSTRAP", "1").lower() in ("1", "true", "yes"):
    _bootstrap_if_needed()
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
