---
description: Run a Claude-native visibility audit. For each query in brand_context.target_queries, ask Claude to answer the query as a real user would (using WebSearch + WebFetch), then record whether the client brand is mentioned, at what position, and which URLs were cited. Outputs visibility_baseline.json validated against schema. This is the BASELINE — the reference point for 07-reaudit. Use after 01-intake; rerun for re-audit rounds.
argument-hint: "<client-folder, e.g. clients/acme>"
---

# 02 · Audit — Claude Visibility Baseline

This command measures **what Claude tells real users** when they ask the
brand's target queries — without telling Claude who the client is.

We deliberately scope the baseline to Claude only. Multi-LLM coverage
(ChatGPT / Perplexity / Gemini / AI Overviews) sounds appealing but
requires per-engine API keys and per-engine output normalization, which
turns the plugin into a heavy ops project. Single-engine + reproducible
beats multi-engine + flaky.

If you later need cross-engine coverage, the vendored
`seo-geo-optimizer` (199-bio) skill has multi-engine analysis paths
(see its `scripts/platform_optimizer.py`).

---

## Inputs

- `clients/<slug>/brand_context.json` — required. Reads `target_queries`,
  `layer_1_business_identity.company.name`, `competitors`.

## Output

- `clients/<slug>/visibility_baseline.json` (round 1) — validates against
  `schemas/visibility_baseline.schema.json`.
- `clients/<slug>/baselines/round-N.json` (round 2+) — preserved snapshots
  for 07-reaudit diff.
- `clients/<slug>/baseline-report.md` — human-readable summary.

---

## Procedure

### Step 1 — Prepare query list

```bash
jq '.target_queries | map({query, query_id: (.query | gsub(" "; "-") | ascii_downcase), priority, intent})' \
  clients/<slug>/brand_context.json > /tmp/queries.json
```

Strip P2 if budget-tight. Default: run all P0 + P1 + P2.

### Step 2 — Define the unbiased query runner

For each query, spawn a **fresh sub-agent context** that does NOT see the
brand_context. The sub-agent answers the query like a normal user — it
uses WebSearch + WebFetch as Claude does by default, no system prompt
nudging it toward our client.

Procedure for each query (loop):

```
Sub-agent task prompt (template):
  "You are answering a user's question. The user asked: <query>.
   Search the web (WebSearch + WebFetch as needed), then write a
   substantive answer (300-600 words) the way you would if asked
   conversationally. List specific brands/companies/products by
   name when relevant. Include the URLs you actually cited."
```

Use the `Agent` tool with a generic subagent (`general-purpose` or
`Explore`). Capture:
- `raw_response` — full answer text.
- `cited_urls` — every URL the sub-agent fetched or referenced.
- `model_id` — `claude-opus-4-7` (or whichever model the runtime uses).
- `captured_at` — ISO timestamp.

### Step 3 — Brand & competitor extraction

For each query result, extract:

| Field | How |
|-------|-----|
| `mentioned` | regex: `\b(<company.name>|<aliases>)\b` (case-insensitive, word-boundary) |
| `position` | If response is list-formatted (numbered, bulleted, ranked), find rank of first brand mention; else `null` |
| `description_quoted` | Sentence containing the brand name (full sentence, not snippet) |
| `competitors_mentioned` | List of competitor names (from `brand_context.competitors[*].name`) found in response |
| `is_owned_by_client` (per citation) | Domain match: parse URL, check against `company.url` |

If brand has aliases or alternate names in `brand_context.layer_1_business_identity.company`, include them in the regex.

### Step 4 — Verify cited URLs are live

For each unique URL across all `cited_urls[]`:

```
WebFetch <url> with prompt "summarize this page in one sentence; flag
if 404, redirect, or off-topic from query"
```

Set `verified_live: true` if the page resolves and is on-topic. `false`
otherwise. Skip URLs already verified in this client's previous baseline
(cache file: `clients/<slug>/.url-verify-cache.json`).

This step is non-negotiable. AI hallucinated citations are common, and
they will silently corrupt 07-reaudit's attribution if not pruned.

### Step 5 — Compute summary metrics

```python
mention_rate = sum(1 for r in runs if r.mentioned) / len(runs)
positions = [r.position for r in runs if r.mentioned and r.position]
avg_position_when_mentioned = sum(positions)/len(positions) if positions else None
total_citations = sum(len(r.citations) for r in runs)
owned_citations = sum(1 for r in runs for c in r.citations if c.is_owned_by_client)
owned_citation_rate = owned_citations / total_citations if total_citations else 0

overall_visibility_score = round(
  100 * (
    0.5 * mention_rate +
    0.3 * (1 / (avg_position_when_mentioned or 10)) +
    0.2 * owned_citation_rate
  ),
  1
)
```

Per-query verdict:
- `winning` — `mention_rate >= 0.6` AND `avg_position <= 3` (across N≥2 runs of the same query, if you choose to run repeats; default is N=1 per query)
- `contested` — `0 < mention_rate < 0.6`
- `absent` — `mention_rate == 0`
- `regressing` — only set in re-audit rounds, when `mention_rate < previous_round_rate - 0.1`

**Note**: with N=1 per query, `mention_rate` per query is binary (0 or 1). The summary `mention_rate` is across all queries. If you want per-query stability, set `runs_per_query` ≥ 3 in `meta` and average.

### Step 6 — Write outputs

- Round 1: `clients/<slug>/visibility_baseline.json`
- Round N≥2: write to `clients/<slug>/baselines/round-N.json` AND replace
  `visibility_baseline.json`.

Set `meta.tool_used = "claude-native-subagent"` and
`meta.audit_round = N`.

### Step 7 — Generate baseline-report.md

```markdown
# Baseline Report — <client> — round <N>
> captured: <ISO ts>
> tool: claude-native-subagent (model: <model_id>)

## Headline
- Overall visibility: **<score>/100**
- Mention rate: <pct>%
- Avg position when mentioned: <num>
- Owned citation rate: <pct>%

## Top wins
<table of queries with verdict=winning>

## Top gaps
<table of queries with verdict=absent and high-priority>

## Competitor landscape
<table: competitor name | times mentioned | queries where mentioned>

## Citation quality
- Total cited URLs: <N>
- Verified-live: <X> / dead: <Y>
- Owned-domain citations: <Z>
```

### Step 8 — Validate against schema

```bash
python3 -c "import json,jsonschema; \
  s=json.load(open('plugins/recomby-geo/schemas/visibility_baseline.schema.json')); \
  d=json.load(open('clients/<slug>/visibility_baseline.json')); \
  jsonschema.validate(d,s); print('OK')"
```

---

## Hard Rules

1. **Schema-validated output**.
2. **No fabricated runs** — if the sub-agent fails on a query, skip and document; do not synthesize.
3. **Citation freshness** — every URL in `citations[]` has `verified_live` set. Hallucinated URLs do not enter the baseline.
4. **Preserve raw_response** — required for 07-reaudit diff.
5. **Round numbering** — `meta.audit_round` is 1 the first time, increments only when 07-reaudit calls back.
6. **Sub-agent has no client context** — never pass brand_context into the query runner. The whole point is measuring what Claude says when it does NOT know about us.

---

## Reference

- `seo-geo-optimizer` (vendored from 199-biotechnologies) — comprehensive
  audit with platform-specific recommendations + 13 Python scripts.
  `scripts/audit_report.py` is the closest off-the-shelf approach if
  you ever need a JSON/MD/HTML triple-format dashboard.
- `references/auriti/princeton-geo-methods.md` — Princeton KDD 2024
  citability factors; useful for interpreting verdict patterns.

---

## Hand-off

Signal: *"Baseline captured. round=<N>, score=<X>/100. Run 03-gap next."*
