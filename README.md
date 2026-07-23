# SokoFresh Backend

SokoFresh is a Django REST API for marketplace, cold storage, and payments workflows in the agricultural supply chain.

## Included requirements

- [x] Authentication and authorization with Django REST Framework and JWT-based auth
- [x] REST API endpoints for accounts, marketplace, cold storage, and payments
- [x] Database schemas across 6 models: User, Produce, Order, ColdRoom, ColdStorageBooking, and MpesaTransaction
- [x] Docker support for local containerized development
- [x] Backend service and deployment-ready configuration
- [x] Database configuration via environment variables
- [x] GitHub Actions CI workflow for checks and tests
- [x] Frontend placeholder for API consumption
- [ ] Frontend deployment to a hosting platform (can be added once the UI is connected)
- [ ] Full production deployment of both frontend and backend (backend deployment config is in place)

## Project structure

- `apps/accounts` – user accounts, auth, and dashboard endpoints
- `apps/marketplace` – produce listings, orders, and analytics
- `apps/cold_storage` – cold room inventory and booking flows
- `apps/payments` – M-Pesa transaction endpoints

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Container development

```bash
docker compose up --build
```

## ERD

See [docs/erd.md](docs/erd.md) for the entity relationship diagram.

## Kanban board

See [docs/kanban-board.md](docs/kanban-board.md) for a lightweight project board.
