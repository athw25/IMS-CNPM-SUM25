# IMS-BE (Flask + SQLAlchemy + JWT) — Modular Refactor of `ims_api.py`

This project is a 1:1 modular refactor of the original single-file app **ims_api.py**.
All endpoints, models, RBAC, state machines, pagination, error schema, seeds, and environment behavior are **identical**.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate        # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt

# optional overrides
# export DATABASE_URL="sqlite:///ims.db"

flask --app src/app.py db       # create tables
flask --app src/app.py seed     # seed demo
python -m src.app               # run dev server (reads .env if present)
```

## Environment (.env)
- `SECRET_KEY` (default: `change-me`)
- `JWT_SECRET_KEY` (default: `change-me-too`)
- `DATABASE_URL` (default: `sqlite:///ims.db`)
- `CORS_ORIGINS` (default: `*`)
- `INIT_DB` (default: `0`, set `1` to auto create tables on start)
- `PORT` (default: `5000`)

## Notes
- JSON error schema: `{"error":{"code":<http>, "message":""}}`
- Pagination envelope: `{"items":[], "page":, "limit":, "total":}`
- Assignment state machine: **Pending → Doing → Done** (only forward)
- Delete-guards:
  - Program cannot be deleted if it has Projects
  - Project cannot be deleted if it has Assignments
  - Campaign cannot be deleted if it has Applications
- Seed is idempotent.
