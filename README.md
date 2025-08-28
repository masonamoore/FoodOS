# FoodOS

A full‑stack food platform that unifies **recipes**, **inventory & groceries**, **meal planning**, **restaurants**, and a BeReal‑style social feature called **Rate My Plate** — plus **camera‑based recipe capture (OCR)** and **AI‑assisted recipe generation & search**.

> **Audience:** Written like a senior dev spec with enough nuance for a junior dev to ramp up and contribute.
>
> **Status:** Planning → MVP execution.
>
> **Last updated:** 2025-08-28

---

## Table of Contents

1. [Project Origin & Initial Prompts](#project-origin--initial-prompts)
2. [Vision & Goals](#vision--goals)
3. [Feature Overview](#feature-overview)
4. [System Architecture](#system-architecture)
5. [Tech Stack](#tech-stack)
6. [Existing Assets to Reuse](#existing-assets-to-reuse)
7. [Data Model](#data-model)
8. [API Design (v0)](#api-design-v0)
9. [ML/AI Components](#mlai-components)
10. [Security, Privacy, and Abuse Prevention](#security-privacy-and-abuse-prevention)
11. [Networking, Scaling & Performance](#networking-scaling--performance)
12. [Testing Strategy](#testing-strategy)
13. [Developer Experience & Repo Layout](#developer-experience--repo-layout)
14. [Local Dev: Getting Started](#local-dev-getting-started)
15. [Roadmap & Milestones](#roadmap--milestones)
16. [Open Questions / Decisions Needed](#open-questions--decisions-needed)
17. [Contributing](#contributing)
18. [License](#license)

---

## Project Origin & Initial Prompts

- Build an "everything in one" food app: **restaurants + recipes + inventory + meal planning**.
- Add a **BeReal‑like daily photo** feature called **Rate My Plate** where users must post their plate once per day to participate.
- **Reuse an existing Foods app** (CLI + Tkinter + MySQL schema) as the core data layer and business logic.
- Add **camera‑based recipe capture** (OCR of cookbooks, screenshots, labels) to auto‑create structured recipes.
- Incorporate **AI** to generate recipes, substitutions, and **semantic search** across recipes and dishes.

This README lays out an implementable plan that grows from an MVP to a robust, scalable platform.

---

## Vision & Goals

**Vision:** FoodOS is a personal and social food operating system. It supports cooking at home, discovering restaurants, planning meals, keeping inventory, and sharing daily eating habits — with AI and OCR to minimize data entry and maximize discovery.

**Primary goals**
- **Unify workflows:** single app for planning, cooking, tracking, going out, and sharing.
- **Minimize friction:** OCR and AI turn photos/text into structured recipes and grocery actions.
- **Make it social:** Rate My Plate drives daily engagement and accountability.
- **Be extensible:** clean APIs, job workers, and modular services for future features.

**Non-goals (for now)**
- Calorie estimation from raw images (hard to do well without a sizable dataset). We’ll bootstrap via user tags + recipe mapping and consider computer vision later.
- Professional nutrition/medical advice.

---

## Feature Overview

### Recipes
- Browse/sort by name, category, cooking time, calories.
- **AI recipe generator** (prompt → JSON → DB insert).
- **OCR import**: capture from camera/photo; parse into ingredients + steps.
- **Semantic search** (“recipes like this”) via embeddings.
- Versioning for edited recipes (future).

### Inventory & Grocery
- Track items by location (fridge/freezer/pantry).
- Bulk updates; auto‑decrement when a meal is cooked.
- Generate **grocery lists** from recipes/meal plans.
- Optional store hints/tags (e.g., Costco/Trader Joe’s).

### Meal Planning
- Weekly calendar; attach recipes.
- Export CSV or shareable link.
- Macro/nutrient totals (computed from ingredients).

### Restaurants
- Nearby search via public APIs (Yelp/Places). Cache responses.
- Save favorites, tag dishes, link to “home recipe equivalents.”
- (Stretch) Turn a restaurant dish into an at‑home recipe suggestion.

### Social: Rate My Plate
- Daily posting window per user (configurable). One post/day enforced.
- Feed with friends’ posts; 1–5 ratings; comments.
- Streaks & gentle reminders (notifications/web push).
- Privacy: default to friends‑only; toggle per post.

### Camera Capture (OCR)
- Upload/Take photo; extract text with OCR.
- Parse quantities/units/ingredients → structured recipe.
- Map unknown ingredients to canonical set (fuzzy/embedding match).

---

## System Architecture

```
[ Web App (Next.js PWA) ]  <— OAuth/JWT —>  [ API Gateway (FastAPI) ]
          │                                     │
          │                                     ├── /recipes, /inventory, /mealplan, /grocery  →  SQL (MySQL→Postgres later)
          │                                     ├── /restaurants  → Public API proxy + cache
          │                                     ├── /rate-my-plate → S3/MinIO for images + DB
          │                                     ├── /import/ocr    → enqueue OCR jobs
          │                                     └── /ai            → recipe-gen, embeddings, search
          │
          └── WebSockets (feed/live updates)     [ Workers (Celery/RQ) ]
                                                  ├── OCR → parse → insert recipe
                                                  ├── Embeddings → vector index
                                                  └── ETL & maintenance jobs

[ Data Layer ]
- SQL DB: start with MySQL (reuse); consider Postgres + pgvector
- Object storage: S3/MinIO for uploads (images, exports)
- Cache/Queue: Redis (sessions, rate limits, queues)
- Observability: Prometheus + Grafana; Loki for logs (opt)
```

**Why FastAPI + Next.js?** Clear typing (Pydantic), good developer speed, Python ML ecosystem, great DX on the web side, easy WebSocket support, and incremental SSR/ISR.

---

## Tech Stack

- **Frontend:** Next.js, React, Tailwind, shadcn/ui, React Query. PWA for camera upload.
- **Backend:** FastAPI (Python 3.11+), Pydantic v2, SQLAlchemy, Alembic.
- **Workers:** Celery or RQ with Redis.
- **DB:** MySQL 8 (existing) → optional migration to Postgres 15 + pgvector.
- **Search/Vector:** FAISS or pgvector for embeddings.
- **OCR:** Tesseract (MVP), consider PaddleOCR for messy receipts.
- **Object Storage:** MinIO/S3 with signed URLs.
- **Auth:** OAuth (Auth.js/Clerk) → JWT to API.
- **CI/CD:** GitHub Actions (lint, tests, migrations). Docker Compose for dev.
- **Secrets:** .env files locally; managed secrets in production.

---

## Existing Assets to Reuse

- **MySQL schema + seed**: `Ingredient`, `Inventory`, `Recipe`, `RecipeIngredient`, `MealPlan`, `GroceryList`, `MealPlanView`.
- **CLI (main.py)**: working CRUD flows; CSV export; AI recipe generation (remove hardcoded API key; use env).
- **Tkinter UI (mainwfront.py)**: validates queries/flows; useful reference for first web screens.
- **meal_plan_report.csv**: export format we’ll reproduce in web.

Reusing this logic lets us deliver a credible MVP fast, then refactor incrementally.

---

## Data Model

### Existing Tables
- **Ingredient(IngredientID, name, description, cal, protein, fat, carb)**
- **Inventory(InventoryID, IngredientID, quantity, location)**
- **Recipe(RecipeID, name, instructions, cookTimeMin, servings, category)**
- **RecipeIngredient(RecipeIngredientID, IngredientID, RecipeID, quantity, unitMeasure)**
- **MealPlan(MealPlanID, MealDate, RecipeID)**
- **GroceryList(GroceryListID, RecipeIngredientID, store)**
- **MealPlanView** (view of recipes by date)

### New Tables (FoodOS)
- **User(user_id, handle, email, created_at, privacy_settings json)**
- **PlatePost(post_id, user_id, ts, image_url, caption, dish_tags json, posted_window_date, visibility)**
- **PlateRating(post_id, rater_user_id, score, comment, ts)**
- **Restaurant(rest_id, name, address, lat, lon, cuisines json, price_tier, source, source_id)**
- **UserRestaurant(user_id, rest_id, favorite, rating, last_visit_at)**
- **RecipeImport(import_id, user_id, ts, image_url, ocr_text, parse_json, status enum)**
- **RecipeEmbedding(recipe_id, embedding(vector))** (pgvector/FAISS)
- **UserPref(user_id, diet_flags json, allergies json, budget_level int)**

**Notes**
- Keep IDs stable and explicit (no ORM surprises in ingestion).
- Use `json/jsonb` columns for flexible metadata; normalize later if needed.
- Add FK indexes early; we’ll need them for feeds and joins.

---

## API Design (v0)

**Auth**
- `POST /auth/callback` (handled by OAuth provider) → issues JWT for API usage.

**Recipes**
- `GET /recipes?search=text&category=&maxTime=&calBand=`
- `GET /recipes/{id}`
- `POST /recipes` (manual add)
- `POST /recipes/import` → returns `import_id`; worker performs OCR → parse → insert
- `GET /recipes/similar/{id}` (embedding search)
- `POST /ai/recipe-generate` (server‑side key; returns JSON and optional DB insert)

**Inventory & Grocery**
- `GET /inventory?location=`
- `PATCH /inventory/{ingredientId}` → `{{ "quantity": 2 }}`
- `POST /grocery/from-recipe/{id}`

**Meal Plan**
- `GET /mealplan?week=YYYY-WW`
- `POST /mealplan` → add items
- `GET /mealplan/export.csv`

**Restaurants**
- `GET /restaurants/nearby?lat=&lon=&q=` (proxy + cache)
- `POST /restaurants/save` (fav/rating)

**Rate My Plate**
- `POST /plate` (enforce 1/day; signed URL upload then finalize metadata)
- `GET /plate/feed?cursor=`
- `POST /plate/{id}/rate` `{{ "score": 4, "comment": "🔥" }}`

**WebSockets**
- `/ws/feed` → push new posts/ratings/comments to subscribers.

**Error Model**
- JSON problem details RFC7807; consistent error codes; rate‑limit headers on relevant endpoints.

---

## ML/AI Components

1. **OCR → Parser → Recipe**
   - Pipeline: upload → OCR (Tesseract) → text blocks → unit/quantity parser → canonical ingredient mapping → DB insert.
   - Unknown ingredients: heuristic + embedding nearest‑neighbor; if still unknown, create placeholder with review flag.

2. **Recipe Generation**
   - Prompted generation for constraints (diet, time, budget). Always parse to strict JSON schema. Manual review toggle before insert.

3. **Embeddings for Search & “Similar”**
   - Offline job to embed recipe titles + instructions.
   - Cosine similarity for related recipes; use MMR for diverse results.

4. **Nutrition Aggregation**
   - Compute macros from `RecipeIngredient × Ingredient` at query‑time, cache aggregates in a materialized view for top recipes.

---

## Security, Privacy, and Abuse Prevention

- **Secrets**: Never ship hardcoded API keys. Use env vars; limit scope with per‑service tokens.
- **Auth**: OAuth for user auth; short‑lived JWT for API; rotate keys.
- **Access control**: Friends‑only default for Rate My Plate; private posts supported.
- **Uploads**: Validate MIME, size limits, content scanning (ClamAV container), signed URLs, object lifecycle policies.
- **Rate limiting**: Per IP + per user. Redis sliding window.
- **Abuse**: Basic image/text moderation hooks (queue suspicious posts for review).
- **PII**: Store only necessary fields; encrypt at rest where appropriate.
- **Audit logs**: For sensitive actions (deletes, privacy changes).

---

## Networking, Scaling & Performance

- **Caching**: Redis for hot recipe queries and restaurant lookups.
- **Pagination**: Cursor‑based for feeds and long lists.
- **Backpressure**: Queue ingestion (OCR/AI) via workers; retry with dead‑letter queues.
- **N+1**: Use `JOIN` + prefetch patterns in API; measure query plans.
- **Static/ISR**: Next.js for semi‑static content (docs, about).
- **Observability**: Request IDs, structured logs, RED metrics dashboards.

---

## Testing Strategy

- **Unit**: Pure functions (parsers, mappers, calorie calculators).
- **API Integration**: FastAPI TestClient with ephemeral DB (Docker).
- **Workers**: Task‑level tests with fake queues & fixtures.
- **E2E**: Playwright (web flows: login → post plate → rate → feed).
- **Data**: Seed datasets for deterministic tests; snapshot expected CSV exports.
- **Security**: Static analysis (bandit), dependency checks (pip‑audit).

---

## Developer Experience & Repo Layout

```
foodos/
├─ apps/
│  └─ web/                 # Next.js PWA
├─ services/
│  └─ api/                 # FastAPI app (REST + WS)
├─ workers/
│  ├─ ocr/                 # OCR + parsing pipeline
│  └─ ai/                  # embeddings, recipe-gen jobs
├─ packages/
│  └─ shared/              # shared types, DTOs, schema
├─ infra/
│  ├─ docker-compose.yml   # dev stack (db, redis, minio, api, web, workers)
│  └─ migrations/          # Alembic or SQL files
├─ db/
│  ├─ init/                # initial schema, seeds
│  └─ views/               # materialized views, helpful SQL
├─ docs/
│  └─ ADRs/                # architecture decisions
└─ README.md               # this file
```

**Conventions**
- Python: ruff/black; TypeScript: eslint/prettier.
- Commits: Conventional Commits (`feat:`, `fix:`…). PR templates enforced.

---

## Local Dev: Getting Started

1. **Prereqs**
   - Docker + Docker Compose, Node 20+, Python 3.11+, Make.

2. **Clone & Boot Dev Stack**
   ```bash
   git clone <repo> foodos && cd foodos
   cp .env.example .env  # fill in values
   docker compose -f infra/docker-compose.yml up -d
   ```

3. **Database**
   - For MVP, import the existing MySQL dump:
     ```bash
     mysql -h 127.0.0.1 -u root -p < db/init/data-dump.sql
     ```

4. **API**
   ```bash
   cd services/api
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

5. **Web**
   ```bash
   cd apps/web
   npm i
   npm run dev
   ```

6. **Workers**
   ```bash
   cd workers/ocr && pip install -r requirements.txt
   celery -A worker.app worker -l INFO
   ```

7. **Secrets**
   - Store API keys in `.env` and inject only server‑side. **Never** commit keys.

---

## Roadmap & Milestones

### Phase 1 — Foundation (Weeks 1–2)
- [ ] Bring up Docker Compose (DB, Redis, MinIO, API, Web).
- [ ] Import existing schema/seed; verify legacy queries.
- [ ] Wrap existing queries as FastAPI endpoints:
  - [ ] `/recipes`, `/inventory`, `/mealplan`, `/grocery`
- [ ] Web screens: Recipes list/detail, Meal Plan, Inventory.
- [ ] Replace hardcoded AI key with env; server‑side recipe‑gen.

### Phase 2 — Social & OCR (Weeks 3–5)
- [ ] *Rate My Plate*: tables, upload flow (signed URLs), feed.
- [ ] Enforce one post/day; comments/ratings; WebSocket feed.
- [ ] OCR ingestion: `/recipes/import` → worker → parse → insert.
- [ ] Ingredient canonicalization; review UI for unknowns.

### Phase 3 — Restaurants & Search (Weeks 6–7)
- [ ] Restaurant API proxy + caching; save favorites & ratings.
- [ ] Embeddings + semantic search; “similar recipes/dishes”.

### Phase 4 — Polish & Scale (Weeks 8+)
- [ ] Auth (OAuth, JWT), user settings/privacy.
- [ ] Notifications (daily plate window, reminders).
- [ ] Analytics: nutrient totals, grocery spend estimates.
- [ ] Optional: migrate to Postgres + pgvector; Helm charts for k8s.

**Stretch Ideas**
- Household sharing (shared inventory/grocery).
- Basic CV dish classifier; map to nearest recipe.
- Social graph growth tools (discover friends, weekly highlights).

---

## Open Questions / Decisions Needed

- **DB**: stay on MySQL for MVP or migrate early to Postgres + pgvector?
- **OCR**: Tesseract vs PaddleOCR — which performs better on our samples?
- **Mobile**: PWA vs React Native from day one?
- **Privacy defaults**: friends‑only posts by default?
- **Moderation**: proactive (models) vs reactive (report/queue)?
- **Restaurant APIs**: which provider & terms are acceptable for caching?

---

## Contributing

- Open a draft PR early; use task lists in PR descriptions.
- Add/Update ADRs for notable architectural decisions.
- Add tests for new endpoints and workers.
- Keep docs current (this README + `/docs`).

---

## License

TBD (e.g., MIT for code). Review third‑party API ToS before redistribution of their data.

