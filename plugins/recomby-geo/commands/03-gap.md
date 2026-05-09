---
description: Translate the visibility baseline + brand context into a ranked list of content actions that should move the needle. Identifies absent queries, contested queries, and competitor-displacement opportunities. Outputs content_priorities.json validated against schema. Use after 02-audit; consumed by 04-content-brief.
argument-hint: "<client-folder, e.g. clients/acme>"
---

# 03 · Gap & Opportunity — Prioritize What to Build

The decision skill. Takes raw baseline data + business context and returns:
"these are the N content pieces, in this order, with this expected impact,
because of this reason."

The framework: **CITE × CORE-EEAT** (borrowed from
`aaron-he-zhu/seo-geo-claude-skills` taxonomy):
- **C**itability — can we be cited as a primary source?
- **I**ntent match — does our angle match the searcher's job-to-be-done?
- **T**rustworthiness — do we have E-E-A-T signals (experience, expertise,
  authority, trust)?
- **E**xpansion — is this query a wedge into a larger query cluster?

---

## Inputs

- `clients/<slug>/brand_context.json`
- `clients/<slug>/visibility_baseline.json`

## Output

- `clients/<slug>/content_priorities.json` — validates against
  `schemas/content_priorities.schema.json`.

---

## Procedure

### Step 1 — Build the candidate set

Every `target_query` from brand_context becomes a candidate. Augment with:

- Queries surfaced in `layer_2_market_reality.real_user_questions` that
  weren't in `target_queries`.
- Queries from `layer_3_value_gaps[*].opportunity` if phrased as a question.

### Step 2 — Score each candidate (CITE × CORE-EEAT)

For each candidate, compute:

| Dimension | How to score |
|-----------|--------------|
| **Citability** | Does brand_context have first-party data, expert POV, or unique methodology that can be cited? +1 to +3. |
| **Intent match** | Does the brand's product directly serve the JTBD behind this query? +1 to +3. |
| **Trustworthiness** | Does the brand have E-E-A-T signals (author bios, credentials, citations elsewhere) for this topic? +0 to +3. |
| **Expansion** | Does winning this query wedge open a cluster (5+ adjacent queries)? +0 to +3. |
| **Current pain** | From baseline: absent (+3), contested (+2), winning-but-fragile (+1), winning-stable (0). |
| **Difficulty (penalty)** | Strong incumbent (-2), generic category leader entrenched (-3), policy-restricted topic (-3). |

Sum → `expected_impact.score` (clamp to 1–10).

### Step 3 — Determine `opportunity_type`

Pick the dominant move per query:
- `fill-absence` — query has mention_rate=0 AND brand has direct authority.
- `displace-competitor` — competitor wins this query but we have stronger
  E-E-A-T or fresher data.
- `deepen-existing` — we partially win but content is thin or outdated.
- `freshness-update` — we own a piece but freshness < 6 months stale.
- `claim-comparison` — comparison query where neither we nor competitors
  have a strong neutral comparison page.
- `first-party-data` — we have proprietary data nobody else has.
- `expert-pov` — our founder/team has unique POV; topic rewards expertise
  over data.

### Step 4 — Determine `recommended_format`

Map opportunity_type + intent to format:

| opportunity_type | intent | format |
|------------------|--------|--------|
| fill-absence | informational | `definition-page` or `deep-guide` |
| fill-absence | comparison | `comparison-page` |
| displace-competitor | comparison | `comparison-page` |
| deepen-existing | informational | `deep-guide` |
| first-party-data | * | `data-report` |
| expert-pov | * | `expert-essay` |
| freshness-update | * | (same as original format) |
| claim-comparison | comparison | `comparison-page` |

### Step 5 — Identify `required_assets`

For each priority, list the real-world inputs the human-in-loop step
(04-content-brief) must collect from the founder/expert:

- `original-data` — proprietary numbers
- `expert-quote` — founder/team POV
- `customer-case` — real customer story (with permission)
- `screenshots` — UI / product / methodology evidence
- `pricing-table` — current pricing
- `methodology-detail` — how exactly the product/service works

A priority that requires none of these is suspicious — it means we're
producing generic content that AI can already auto-generate, which won't
get cited. Flag it and reduce its expected_impact score.

### Step 6 — Rank and trim

Sort by expected_impact.score DESC, then by difficulty ASC (low first).
Take top 12–20 unless the user specifies otherwise.

For each rejected candidate that scored ≥6, list it under
`rejected_alternatives[]` on its closest sibling priority, with reason —
this gives 04-content-brief authors fallback ammunition.

### Step 7 — Write & validate

Write `clients/<slug>/content_priorities.json`. Validate:

```bash
python3 -c "import json,jsonschema; \
  s=json.load(open('plugins/recomby-geo/schemas/content_priorities.schema.json')); \
  d=json.load(open('clients/<slug>/content_priorities.json')); \
  jsonschema.validate(d,s); print('OK')"
```

---

## Hard Rules

1. **Reasoning, not just numbers** — every priority must have a
   `rationale` field that cites the specific brand_context value gap or
   baseline finding it's responding to. "Score 8" is not a reason.
2. **Required-assets discipline** — every priority must list at least one
   `required_asset` of type `original-data`, `expert-quote`,
   `customer-case`, or `methodology-detail`. Pure-LLM-generatable content
   is not GEO-defensible.
3. **No more than 5 priorities of the same `opportunity_type`** — forces
   diversification.
4. **Schema-validated output**.

---

## Reference

- `content-quality-auditor` (vendored from aaron-he-zhu/seo-geo-claude-skills)
  — CITE / CORE-EEAT scoring source.
- `keyword-research` (vendored from nowork-studio/toprank) — adjacent-query
  expansion for `expansion` scoring dimension.
- `references/auriti/princeton-geo-methods.md` — Princeton KDD 2024
  citation/statistics/quotation evidence underlying the rubric.

---

## Hand-off

Signal: *"<N> priorities ranked. Top 3: <q1>, <q2>, <q3>. Run
04-content-brief on the top priority next."*
