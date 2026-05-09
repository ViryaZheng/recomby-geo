---
description: Build the GEO brand context for a client by ingesting provided materials (PDF/DOCX/PPTX/XLSX, URLs, raw notes) and conducting structured AI-perception + competitor + community research. Writes brand_context.json validated against schemas/brand_context.schema.json. Use when starting a new client (clients/<slug>/inputs/ has materials but no brand_context.json), or when brand_context.json is marked status=stale. Downstream consumers: 02-audit, 03-gap, 04-content-brief, 05-production.
argument-hint: "<client-folder, e.g. clients/acme>"
---

# 01 · Intake — Build the Brand Context

The single source of truth for the entire pipeline. Every downstream skill
reads `brand_context.json`. If this is wrong or thin, every later skill
amplifies the error.

**Core principle**: AI recommends whoever best answers the question. The
richer and more precise this profile, the more accurately the rest of the
pipeline can identify the exact questions this business should own.

---

## Inputs

- `clients/<slug>/inputs/` — materials provided by the client (any of: PDF,
  DOCX, PPTX, XLSX, image, plaintext notes, URL list).
- The user may also provide context conversationally during this skill run.

## Output

- `clients/<slug>/brand_context.json` — validates against
  `schemas/brand_context.schema.json` (3 layers + extended).
- `clients/<slug>/intake-log.md` — append-only human-readable log of what
  was extracted from which source.

---

## Procedure

Run sequentially. Do not signal readiness to 02-audit until every gate passes.

### Step 1 — Ingest materials

For each file in `clients/<slug>/inputs/`:

| Input type | Approach |
|------------|----------|
| `*.pdf`    | Read with the `Read` tool (built-in PDF support up to 10 pages; for larger PDFs, pass `pages` ranges) |
| `*.docx`   | `unzip -p file.docx word/document.xml \| sed 's/<[^>]*>/ /g'` then `tr -s ' ' '\n'` |
| `*.pptx`   | Same as docx but `ppt/slides/slide*.xml` |
| `*.xlsx` / `*.csv` | `python3 -c "import pandas; print(pandas.read_excel(...).to_csv())"` |
| URL list   | `WebFetch` each URL with extraction prompt |
| `*.png` / `*.jpg` | `Read` (multimodal) — extract text and structural info |
| Notes      | Read directly |

**Do not dump raw content into brand_context.json.** Apply the extraction
filter: keep only signals that map to a schema field. Discard the rest.

### Step 2 — Layer 1 (Business Identity) — 5 hard-required fields

Fill these from materials. If any is missing or thin (single word, "TBD",
generic-quality phrase), ASK the user a targeted question. Don't continue
with placeholder values.

1. `company.name` + URL + one-line description
2. `product_or_service.category` + description + core_offerings
3. `target_customer.primary_icp` — Forrester-style: persona_label,
   demographics (role/segment, geography, size/age), jobs_to_be_done (≥1),
   pain_points, search_behavior
4. `competitors[]` — 1–3 entries. **Verify each via `WebFetch` on their
   public site** before recording. Don't trust user-named competitors blindly.
5. `core_differentiator` (concrete, ≥10 chars, not "we provide quality")
6. `competitive_moat` (one-sentence why-AI-should-recommend-us)

### Step 3 — Layer 2 (Market Reality) — three-dimensional scan

Do all three independently. Don't ask the user; the user doesn't have this data.

**3a. AI Perception Scan**
- Pick 5–8 representative queries from the category (definition, top-X,
  comparison, how-to, status). Use `target_queries` if present, else
  generate from category + ICP.
- Run a Claude-native scout: spawn a sub-agent with NO client context
  and ask it each query. Same mechanism as 02-audit Step 2 (see
  `skills/02-audit/SKILL.md`). For multi-engine coverage you may
  optionally invoke `seo-geo-optimizer` (vendored).
- Record into `layer_2_market_reality.ai_recommends[]`: model, query,
  recommended brands, whether us mentioned, position, captured_at.
- For every URL the AI cites, `WebFetch` it. Verify it's real, recent,
  on-topic. Record into `citation_sources[]`.

**3b. Competitor Reality**
- For each competitor named in Layer 1, `WebFetch` their homepage + key
  pages. Record core_approach, strengths, weaknesses, ai_visibility_notes,
  key_differentiator_vs_us, verified_at.
- **Cross-check**: if the AI in 3a recommends competitors the user didn't
  name, surface this: "You named X, Y, but AI recommends A, B for this
  category. Track both sets or focus on one?" Then update Layer 1 competitors
  accordingly.

**3c. Community Voice**
- `WebSearch`: `"<category> reddit recommendation"`, `"<category> vs
  <competitor> forum"`, `"<category> review hacker news"`.
- `WebFetch` top 2–3 threads. Read actual user language.
- Record into `real_user_questions[]` with source URL and intent
  classification.

### Step 4 — Layer 3 (Value Gaps) — synthesize opportunities

From Layer 1 + Layer 2, identify question types where this business CAN
win but currently isn't. At least one entry. Each entry must include
`opportunity` + `rationale` + supporting_evidence (cite specific Layer 2
findings).

### Step 5 — Target queries

Build `target_queries[]`. Sources:
- Queries from 3a that the brand currently loses on but matches Layer 3.
- Queries surfaced in 3c real_user_questions.
- Long-tail derived from `product_or_service.category` × ICP `jobs_to_be_done`.

Each entry needs query, intent, priority (P0/P1/P2), rationale,
expected_answer_shape.

Minimum 10 entries. Aim for 25–40 to give 02-audit a robust baseline.

### Step 6 — Voice samples + content assets

- Pick 2–3 canonical voice samples from materials (homepage hero, top blog
  post, founder note). Record source + excerpt + voice_attributes.
- Walk the client site (or list of provided URLs). Catalog every existing
  asset into `content_assets[]` with type + freshness.

### Step 7 — Confirm with user before writing

Before persisting brand_context.json, present to user:
- One-sentence competitive_moat
- AI's current view of the brand (from 3a)
- Information gaps still unfilled
- Any conflicts between user-claimed and AI-discovered competitors

User confirms → write JSON.

### Step 8 — Validate against schema

```bash
python3 -c "import json,jsonschema; \
  s=json.load(open('plugins/recomby-geo/schemas/brand_context.schema.json')); \
  d=json.load(open('clients/<slug>/brand_context.json')); \
  jsonschema.validate(d,s); print('OK')"
```

If validation fails: do not signal readiness. Fix.

---

## Hard Rules

1. **5 core field gate** — all 5 Layer 1 required fields must have substantive
   content. No "TBD", no single-word entries.
2. **WebFetch before trust** — never record competitor info or citation sources
   based on AI's claim alone. Verify the URL exists and is on-topic.
3. **Confirm before write** — never persist brand_context.json without showing
   the user the moat sentence + AI-perception summary first.
4. **Schema-validated output** — if `jsonschema.validate` fails, do not signal
   readiness. Fix the data.
5. **Append, don't overwrite intake-log.md** — every run appends a section
   with timestamp + sources processed + fields touched.

---

## Reference

- **`seo-geo-optimizer`** (vendored from 199-biotechnologies) — its
  `scripts/entity_extractor.py` is useful for pre-populating Layer 2
  citation_sources from already-known authority pages.
- **Schema.org `Organization` / `Brand` / `Event`** — Layer 1 field
  names align with public structured-data conventions; helps 06-distribution.
- **`references/auriti/princeton-geo-methods.md`** — defines what a
  "winnable query" looks like; informs Step 5 priority assignment.
- **Forrester ICP template** — Layer 1 `target_customer` field shape.

---

## Hand-off

When all 8 steps pass, write to `clients/<slug>/intake-log.md`:

```
## <ISO timestamp>
- Sources processed: <list>
- Fields populated: layer_1 ✅, layer_2 ✅, layer_3 ✅
- Target queries: <count>
- Schema validation: PASS
- Ready for: 02-audit
```

Then signal: *"brand_context.json built. Run 02-audit next."*
