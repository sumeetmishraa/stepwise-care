# Stepwise Care — Post-Discharge Care Coordination

Stepwise Care is a care-coordination console for post-discharge care. It converts a discharge summary into a structured 30-day care plan, ranks patients by risk, supports a coordinator queue, patient detail/review workflows, check-ins, escalation, and an audit trail.

## Stack
- **Frontend:** React 19, Vite, TypeScript, React Router, TanStack Query, Lucide React, Recharts, Tailwind CSS v4
- **Backend:** FastAPI, Pydantic, SQLAlchemy, SQLite
- **AI:** Mock provider works out of the box; optional Ollama/Anthropic/AWS Bedrock adapters can be added behind the provider interface.
- **Safety:** This is a demo scaffold, not a clinical decision support system. AI-generated assessments are illustrative and require qualified human review.

## Quick start

### Requirements
- Node.js 20+
- Python 3.11+

### 1. Start the backend
```bash
cd Backend
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```
API docs: http://127.0.0.1:8000/docs

### 2. Start the frontend
In a second terminal:
```bash
cd Frontend
npm install
cp .env.example .env
npm run dev
```
Open http://localhost:5173

The API seeds seven demo patients on first run. Frontend can also run in mock mode with `VITE_USE_MOCKS=true`.

## Main routes
- `/` — dashboard
- `/queue` — urgency-ranked coordinator queue
- `/intake` — submit a discharge summary
- `/patient/:id` — patient detail, plan, risk, messages, and check-ins
- `/review/:id` — review and approve/edit the generated care plan
- `/tasks` — follow-up tasks
- `/outcomes` — outcome metrics

## API endpoints
- `GET /api/health`
- `GET /api/patients`
- `GET /api/patients/{patient_id}`
- `POST /api/intake`
- `GET /api/queue`
- `GET /api/tasks`
- `POST /api/patients/{patient_id}/checkins`
- `POST /api/patients/{patient_id}/escalations`
- `POST /api/patients/{patient_id}/approve`
- `GET /api/metrics`
- `GET /api/audit`

## Important next steps
1. Replace the demo/mock agent with a validated clinical workflow and approved model/provider.
2. Add authentication, role-based access, encrypted storage, retention policies, and PHI-safe logging before using real patient data.
3. Add tests, migrations, observability, deployment configuration, and clinical governance.
4. Validate all outputs with qualified clinicians. Never use this demo for real patient care.
