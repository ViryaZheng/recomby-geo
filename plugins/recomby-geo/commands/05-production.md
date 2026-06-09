---
description: Convert an expert-filled brief into a publishable draft. Applies Princeton KDD 2024 GEO techniques (statistics, quotations, citations, authoritative language) to maximize AI citation likelihood. Refuses to run on briefs that haven't been filled by the expert. Outputs drafts/<id>.md. Use after 04-content-brief produces a brief with status=ready-for-production.
argument-hint: "<client-folder, e.g. clients/acme>"
---

# 05 · Production — Draft Generation

This command orchestrates `content-writer` (vendored) plus Princeton GEO
rewrite techniques and CITE/EEAT quality scoring via `content-quality-auditor`
(vendored). It does NOT generate content from scratch — that work happened
in 04-content-brief where the expert filled REQUIRED-FILL slots. Production
assembles the filled brief into a polished draft and applies GEO-optimization
rewrite rules.

---

## Inputs

- `clients/<slug>/brand_context.json` (for voice + extended context)
- `clients/<slug>/content_priorities.json` (to pull the priority record)
- `clients/<slug>/briefs/<id>.md` (the expert-filled brief)
- `clients/<slug>/briefs/<id>.meta.json` (must have `status:
  ready-for-production`)

## Output

- `clients/<slug>/drafts/<id>.md` — publishable Markdown draft.
- `clients/<slug>/drafts/<id>.meta.json` — machine-readable metadata
  (word count, citation count, statistics count, quote count, voice-match
  score, GEO-readiness checklist).
- `clients/<slug>/drafts/<id>.html` — interactive review version for the
  client (section-level comments + approve-as-is), rendered by the
  `geo-review-html` skill.

---

## Procedure

### Step 1 — Hard refusal gate

```bash
status=$(jq -r '.status' clients/<slug>/briefs/<id>.meta.json)
if [ "$status" != "ready-for-production" ]; then
  echo "REFUSE: brief <id> status=$status. Run 04-content-brief Step 9 first."
  exit 1
fi
```

If status is not `ready-for-production`, refuse to draft. Do not auto-fill
slots. Send the user back to 04-content-brief.

### Step 2 — Verify slot fills are substantive

Re-read the brief. For each former REQUIRED-FILL slot:
- Reject if content is `<100 chars` for `original-data` slots.
- Reject if `expert-quote` slot lacks attribution (name + role).
- Reject if `customer-case` slot lacks identifying detail (industry,
  approximate size, outcome metric).
- Flag (don't auto-reject) if content sounds AI-generated (hedging
  language, "in conclusion", "moreover", repeated bigrams).

If any rejection: stop, report to user, suggest re-filling. Do not draft.

### Step 3 — Assemble the draft

Use the brief outline as the skeleton. Replace each filled slot inline.
Do NOT remove slot id annotations — keep them as HTML comments
(`<!-- slot: data-1 -->`) so 06-distribution can audit them later.

Apply transitions, intros, and connective tissue. This is the only
generative work — keep it light. Heuristic: if you'd be embarrassed to
say it out loud, delete it.

### Step 4 — Apply Princeton GEO rewrite techniques

The KDD 2024 paper showed these rewrite operations boost AI citation rate
by up to 40%. Apply each pass:

1. **Quotation injection** — wherever a claim could be stated by a
   recognized expert, rewrite to attribute it to the named expert from the
   filled brief.
2. **Statistics surfacing** — promote numbers from prose into standalone
   sentences. "We saw 23% improvement" → "Across 200 firms, **23% saw
   improvement** within 60 days."
3. **Citation densification** — every external claim gets a citation
   anchor `[^N]` linking to the brief's citations block. Aim for 1
   citation per ~150 words of factual content.
4. **Authoritative phrasing** — rewrite hedged language ("could be",
   "might suggest") to direct phrasing where the brief's data supports it.
   Don't fake confidence; do remove unjustified hedging.
5. **Fluency optimization** — short sentences for declarations, longer
   for explanations. Vary sentence length (Princeton finding: monotone
   sentence length correlates with lower citation rate).

### Step 5 — Voice match

Compare draft tone against `brand_context.voice_samples`. Adjust:
- Sentence length distribution
- Jargon density
- First-person vs third-person
- Use of rhetorical questions / direct reader address

Voice-match scoring: pick 5 random sentences from voice_samples and 5 from
draft. Score 1–5 on similarity (sentence shape, vocabulary, formality).
Record in meta.

### Step 6 — Generate metadata

```json
{
  "priority_id": "...",
  "draft_path": "clients/<slug>/drafts/<id>.md",
  "generated_at": "...",
  "word_count": 0,
  "stats": {
    "citations": 0,
    "statistics_count": 0,
    "quotes_count": 0,
    "internal_link_slots": 0,
    "external_links": 0
  },
  "voice_match_score": 0,
  "geo_readiness": {
    "has_definition_block": false,
    "has_faq_block": false,
    "has_comparison_table": false,
    "has_methodology_section": false,
    "answer_first_within_200_words": false
  },
  "status": "draft-ready"
}
```

### Step 7 — Write outputs

- `clients/<slug>/drafts/<id>.md`
- `clients/<slug>/drafts/<id>.meta.json` — validate against
  `schemas/draft_meta.schema.json` before continuing.

Then render the client review HTML via the `geo-review-html` skill (draft
mode: read-only prose, per-section comment toggles, `✓ Approve as-is`):

```bash
python3 plugins/recomby-geo/skills/geo-review-html/scripts/render_html.py \
  --mode draft \
  --md   clients/<slug>/drafts/<id>.md \
  --meta clients/<slug>/drafts/<id>.meta.json \
  --brand clients/<slug>/brand_context.json \
  --out  clients/<slug>/drafts/<id>.html
```

A returned `*.feedback.json` (status `approved-as-is` or
`reviewed-with-comments`) validates against
`schemas/review_feedback.schema.json`; route comments back into a revision
or to 06-distribution.

### Step 8 — Self-review

Run a second pass on the draft asking: "would I cite this if I were
ChatGPT answering the priority query?" Flag weak sections. Do NOT
silently rewrite — surface to user as suggested edits.

---

## Hard Rules

1. **Refuse on unfilled briefs** — Step 1 is a hard gate.
2. **Never auto-fill expert slots** — if a slot looks empty, return to
   04-content-brief.
3. **Slot annotations preserved** — keep `<!-- slot: ... -->` comments
   for downstream attribution.
4. **Citations only for facts that came from somewhere** — don't fabricate
   citations to inflate citation count.
5. **No claim without source** — every numeric claim either has a
   citation or is from `original-data` (own data).

---

## Reference

- `content-writer` (vendored from nowork-studio/toprank) — outline-to-prose
  mechanics for Step 3 assembly.
- `content-quality-auditor` (vendored from aaron-he-zhu/...) — CITE
  framework for citation density heuristics in Step 4; also the Step 8
  self-review pass.
- `seo-geo-optimizer/scripts/voice_optimizer.py` (vendored from
  199-biotechnologies) — automatable voice-match scoring for Step 5.
- `seo-geo-optimizer/scripts/citation_enhancer.py` — citation
  densification helper for Step 4 step 3.
- `references/auriti/princeton-geo-methods.md` — Princeton KDD 2024
  rewrite passes (Step 4) empirical foundation.
- `geo-review-html` (original) — renders the draft review HTML in Step 7
  (draft mode) and defines the `*.feedback.json` approve/comment contract.

---

## Hand-off

Signal: *"Draft <id> ready. word_count=<N>, citations=<C>,
voice_match=<S>/5. Run 06-distribution next, or send to client review."*
