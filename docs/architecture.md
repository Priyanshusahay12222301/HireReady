# HireReady Architecture (Phase 1)

## Separated Layers

- `frontend/`: UI pages, styling, and browser-side API integration.
- `backend/`: Flask API, business logic, data models, and tests.

## Initial API Endpoints

- `GET /api/health`
- `POST /api/auth/register`
- `POST /api/auth/login`

## Readiness Service

Weighted formula (0-100):

- Profile completeness: 20%
- Tests attempted: 30%
- Average test score: 30%
- Mock interviews: 20%

## Next Implementation Slice

1. Add full schema models (`questions`, `test_results`, `jobs`, `applications`, `readiness_score`).
2. Build Flask migrations and seed scripts.
3. Connect dashboard cards to real backend data endpoints.
4. Add session auth with Flask-Login route guards.
