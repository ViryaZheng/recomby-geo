---
description: Re-run 02-audit, diff against the previous baseline, attribute movement to specific content/distribution actions. Outputs reaudit/round-N.json validated against attribution_diff.schema.json. This is the closing-of- loop artifact that proves (or disproves) what's actually working. Run monthly after the previous month's distribution actions have had time to be indexed.
argument-hint: "<client-folder, e.g. clients/acme>"
---

# 07 · Re-audit & Attribution

Closes the loop. Without this skill, the pipeline is open-loop — actions
go out, no proof they did anything. With this skill, every action gets
graded: did it move queries, which queries, by how much, with what
confidence.

---

## Inputs

- `clients/<slug>/visibility_baseline.json` (current — about to be replaced)
- `clients/<slug>/baselines/round-<N-1>.json` (previous round)
- `clients/<slug>/distribution/log.jsonl` (every action since previous round)

## Output

- `clients/<slug>/reaudit/round-<N>.json` — validates against
  `schemas/attribution_diff.schema.json`.
- `clients/<slug>/reaudit/round-<N>.report.md` — human-readable monthly
  review.
- (side effect) `clients/<slug>/baselines/round-<N>.json` — new baseline
  preserved.
- (side effect) Updates `clients/<slug>/visibility_baseline.json` to the
  new round.

---

## Procedure

### Step 1 — Snapshot previous baseline

Before re-running audit, copy current `visibility_baseline.json` to
`baselines/round-<N-1>.json` if not already there. Idempotent.

### Step 2 — Invoke 02-audit

Call 02-audit with `meta.audit_round = N`. Use the SAME `target_queries`
list as the previous round (do not silently drop or add queries — that
breaks the diff). If brand_context.target_queries has changed, log the
delta but keep the audit on the union for one round; signal to user that
next round will adopt the new list.

After 02-audit completes, the new baseline is at
`clients/<slug>/visibility_baseline.json`.

### Step 3 — Load both rounds + the action log

```bash
PREV=clients/<slug>/baselines/round-<N-1>.json
CURR=clients/<slug>/visibility_baseline.json
LOG=clients/<slug>/distribution/log.jsonl
```

Filter log entries to those with `shipped_at` between PREV.captured_at
and CURR.captured_at. These are the actions in this round's window.

### Step 4 — Per-query diff

For each query in PREV.summary.per_query:
- Look up matching query in CURR.summary.per_query (by query_id, fall
  back to query string).
- Compute delta: mention_rate_delta, position_delta.
- Determine verdict_change:
  - `improved` — mention_rate up by ≥10pp OR position improved by ≥1.
  - `regressed` — mention_rate down by ≥10pp OR position worse by ≥1.
  - `newly-won` — was 0 mention_rate, now > 0.3.
  - `newly-lost` — was > 0.3 mention_rate, now 0.
  - `stable` — within ±10pp and ±1 position.

### Step 5 — Action attribution

For each query with movement (improved / regressed / newly-won /
newly-lost):
- Search action log for actions where `targets_query_ids` includes this
  query_id.
- Among matched actions, weight by recency (more recent = more likely
  cause), publication date vs measurement date (need ≥7 days for AI
  re-indexing typically).
- Set `attributed_actions[]` = matched action ids.
- Set `attribution_confidence`:
  - `high` — exactly one matched action published 7–30 days ago, no
    confounding factors.
  - `medium` — one matched action with caveats (recent re-audit gap,
    competitor also moved).
  - `low` — multiple candidate actions, or movement direction
    inconsistent with action.
  - `unknown` — no matched actions; movement is unexplained (could be
    competitor change, AI model update, market drift).

### Step 6 — Per-action audit (reverse direction)

For each action in this round's window:
- Find queries it was supposed to move (targets_query_ids).
- Did any of them improve? If yes → action goes in
  `summary.actions_with_impact`.
- If no targeted query improved (or worse, regressed) → action goes in
  `summary.actions_without_impact` with a `diagnosis` field.

Diagnosis options:
- `too-recent` — published <7 days before re-audit; not enough re-index
  time.
- `wrong-target` — action targeted query the brand had no shot at given
  competitor entrenchment.
- `weak-content` — published but low citation density / no first-party
  data; probably not getting cited.
- `distribution-gap` — published but no internal links / no llms.txt /
  no external mentions; AI engines didn't find it.
- `competitor-counter` — action would have worked but a competitor
  shipped a stronger piece.
- `unknown` — needs human review.

Diagnosis feeds into the next 03-gap run.

### Step 7 — Compute summary

```python
queries_improved = count(verdict_change in {"improved", "newly-won"})
queries_regressed = count(verdict_change in {"regressed", "newly-lost"})
queries_stable = count(verdict_change == "stable")
overall_score_delta = CURR.summary.overall_visibility_score - PREV.summary.overall_visibility_score
```

`next_round_recommendations[]` — plain-language hand-off. Examples:
- "Doubled down on `<query>` produced 0 movement; diagnosis: too-recent.
  Hold next round before re-prioritizing."
- "`<competitor>` started winning `<query>`; consider displace-competitor
  brief next round."
- "Consider adding `<new query>` to target_queries — surfaced 4 times in
  Layer 2 user questions but not yet tracked."

### Step 8 — Write outputs

- `clients/<slug>/reaudit/round-<N>.json` (machine)
- `clients/<slug>/reaudit/round-<N>.report.md` (human)

Report layout:

```markdown
# Re-audit Round <N> — <client>
> previous: round <N-1> @ <ts> — score <X>/100
> current:  round <N>   @ <ts> — score <Y>/100
> delta: <±Z>

## Headline movements
<table: query | prev → curr | delta | verdict | attributed action(s)>

## What worked
<list: actions_with_impact>

## What didn't (and why)
<list: actions_without_impact with diagnosis>

## Recommendations for next round
<from summary.next_round_recommendations>
```

### Step 9 — Validate

```bash
python3 -c "import json,jsonschema; \
  s=json.load(open('plugins/recomby-geo/schemas/attribution_diff.schema.json')); \
  d=json.load(open('clients/<slug>/reaudit/round-<N>.json')); \
  jsonschema.validate(d,s); print('OK')"
```

---

## Hard Rules

1. **Same query set across rounds** — diff requires apples-to-apples.
   Adding/removing queries is signaled but takes effect next round.
2. **Honest attribution** — when movement is unexplained, mark
   `attribution_confidence: unknown`. Do not invent causal stories.
3. **7-day re-index buffer** — actions shipped <7 days before re-audit
   are diagnosed `too-recent`, not `weak-content`.
4. **Schema-validated output**.
5. **Preserve raw_response in baselines** — the 04-content-brief expert
   may want to read what AI actually said about us last month vs now.

---

## Reference

- `skills/02-audit/SKILL.md` — re-invoked with `meta.audit_round = N`
  (Claude-native subagent path; no external shim).
- `seo-geo-optimizer/scripts/freshness_monitor.py` (vendored from
  199-biotechnologies) — for `freshness-update` action diagnosis.
- `references/auriti/princeton-geo-methods.md` — empirical basis for
  "what kind of content moves visibility" used in
  `actions_without_impact` diagnosis (weak-content vs distribution-gap
  vs wrong-target).

---

## Hand-off

Signal: *"Round <N> reaudit complete. Score <X>→<Y>. <N improved>/<N
regressed>. Recommendations written. Run 03-gap next round on the new
priorities."*
