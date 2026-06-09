---
description: For one priority from content_priorities.json, generate a content brief with explicit slots for the human expert (founder/domain specialist) to fill with real cases, real data, and real opinions. This is the human-in-loop checkpoint — the moat that prevents the entire workflow from collapsing into "AI writing more AI-readable AI slop." Outputs briefs/<priority-id>.md. Use after 03-gap; consumed by 05-production ONLY after the expert has filled the marked slots.
argument-hint: "<client-folder, e.g. clients/acme>"
---

# 04 · Content Brief — Human-in-Loop Checkpoint

This is the most important command in the pipeline. Without it, the system
collapses into the same generic AI-content-mill that has saturated the
GEO commodity layer. With it, the system produces content AI engines
actually cite — because it contains things AI can't auto-generate.

**The principle**: the pipeline builds the scaffold; humans fill the soul.
This command outputs scaffold with explicit, named, schema-tight blank
spaces. Until those blanks are filled, 05-production refuses to run.

---

## Inputs

- `clients/<slug>/brand_context.json`
- `clients/<slug>/content_priorities.json`
- A specific `priority_id` (passed by user or auto-picked: highest unbriefed).

## Output

- `clients/<slug>/briefs/<priority-id>.md` — human-readable brief with
  REQUIRED-FILL slots clearly marked.
- `clients/<slug>/briefs/<priority-id>.meta.json` — machine-readable
  metadata: which slots are filled, by whom, when.
- `clients/<slug>/briefs/<priority-id>.html` — interactive fill-form for
  the client/expert (rendered by the `geo-review-html` skill; this is the
  artifact the reviewer actually opens, not the `.md`).

---

## Procedure

### Step 1 — Load context

```jq
jq --arg id "<priority-id>" '.priorities[] | select(.id==$id)' \
  clients/<slug>/content_priorities.json
```

Pull the priority record. Cross-reference brand_context for the relevant
ICP, voice samples, and competitor positioning.

### Step 2 — Choose the angle

Generate 2–3 candidate angles for the priority. An angle is a one-sentence
statement of the unique thesis the piece will defend. Bad angle: "Best CRM
for small business." Good angle: "Why bookkeepers (not sales teams) should
own CRM choice in firms under 20 people, based on our 200-firm dataset."

The angle MUST satisfy:
- Aligns with `core_differentiator` and `competitive_moat` from brand_context.
- Targets the priority's `intent` directly.
- Cannot be written without the brand's specific
  expertise/data/perspective (i.e., GPT-4 with a Google search couldn't
  produce it).

Present the candidate angles to the user. Wait for selection or for the
user to propose a fourth angle.

### Step 3 — Build the brief skeleton

Use the `recommended_format` from the priority to pick a template:

- `comparison-page` → table-driven, ≥3 alternatives, decision rubric.
- `deep-guide` → outline with H2/H3, FAQ block, glossary.
- `case-study` → setup → action → result → lessons.
- `data-report` → headline finding → methodology → data tables → caveats.
- `expert-essay` → POV statement → evidence → counter-arguments → conclusion.
- `definition-page` → canonical definition → variants → examples → related concepts.
- `how-to` → prerequisites → steps → verification → troubleshooting.
- `list-roundup` → criteria → ranked list → notes per item.
- `faq-block` → 8–15 Q&A pairs.

### Step 4 — Insert REQUIRED-FILL slots

For each `required_assets` entry in the priority record, insert a
clearly-marked slot in the brief. Each slot has:

```markdown
> **REQUIRED-FILL · {slot_id} · {asset_type}**
>
> **What goes here**: {1-2 sentence description of what the expert
> must provide. Be specific.}
>
> **Why it matters for GEO**: {1 sentence — what this real input does
> for citation-worthiness, e.g., "AI engines cite primary data 3.2× more
> than rephrased data." (cite Princeton KDD 2024 finding.)}
>
> **Bad fill (rejected)**: {example of what NOT to write — usually a
> generic placeholder or AI-paraphrased text.}
>
> **Good fill (accepted)**: {example showing the level of specificity
> required.}
>
> **(Expert: replace this entire block with your content. Do not delete
> the slot_id — 05-production reads it to verify the slot is filled.)**
```

Slot ids: `data-1`, `quote-1`, `case-1`, etc. — stable, sequential per type.

### Step 5 — Mandatory GEO elements

Every brief must include scaffolding for these (Princeton KDD 2024 shows
they boost AI citation rate):

1. **Statistics block** — at least 2 quantitative claims (REQUIRED-FILL
   slots if not already in brand_context).
2. **Quotation block** — at least 1 direct quote from a named expert
   (REQUIRED-FILL slot).
3. **Citation block** — list of 5–10 external authoritative sources the
   piece will cite. Pre-populate from brand_context Layer 2
   `citation_sources` where relevant; mark new ones as REQUIRED-FILL.
4. **FAQ block** — 5–8 Q&A pairs derived from `real_user_questions`.

### Step 6 — Voice-match notes

Pull `voice_samples` from brand_context. Add a "Voice notes" section at
the top of the brief instructing the writer (05-production or human) to
match: tone attributes, sentence length range, jargon level,
first-person vs third-person.

### Step 7 — Write the brief and meta

Brief MD layout:

```markdown
# Brief — <priority.query>

> Priority id: <id>
> Generated: <ISO ts>
> Format: <recommended_format>
> Status: awaiting-expert-fill

## Angle
<chosen angle, one paragraph>

## Voice notes
<bullet list>

## Outline
<H2/H3 structure with REQUIRED-FILL slots inline>

## Mandatory GEO elements
### Statistics
<slots>
### Quotations
<slots>
### Citations
<pre-populated + slots>
### FAQ
<slots derived from real_user_questions>

## Distribution targets
<from priority.recommended_format + intent — pre-suggested>

## Sign-off checklist (for expert)
- [ ] All REQUIRED-FILL slots replaced
- [ ] Angle still feels right after filling
- [ ] Statistics have sources or methodology notes
- [ ] Quotes have real attribution
- [ ] At least one element only THIS company could provide
```

Meta JSON layout:

```json
{
  "priority_id": "...",
  "brief_path": "clients/<slug>/briefs/<id>.md",
  "generated_at": "...",
  "status": "awaiting-expert-fill",
  "slots": [
    { "id": "data-1", "type": "original-data", "filled": false },
    { "id": "quote-1", "type": "expert-quote", "filled": false }
  ],
  "expert_assignee": null,
  "due_at": null
}
```

Then render the interactive fill-form HTML via the `geo-review-html` skill —
this is the artifact you hand to the client/expert (the `.md` is for the
operator). The skill keeps the interaction logic fixed and applies
`frontend-design` for visual quality:

```bash
python3 plugins/recomby-geo/skills/geo-review-html/scripts/render_html.py \
  --mode brief \
  --md   clients/<slug>/briefs/<id>.md \
  --meta clients/<slug>/briefs/<id>.meta.json \
  --brand clients/<slug>/brand_context.json \
  --out  clients/<slug>/briefs/<id>.html
```

Then (re)build the client entry page so the new brief shows up with live
progress:

```bash
python3 plugins/recomby-geo/skills/geo-review-html/scripts/render_html.py \
  --mode index --client-dir clients/<slug> \
  --brand clients/<slug>/brand_context.json \
  --out clients/<slug>/briefs/index.html
```

### Step 8 — Notify the user

Output: full brief file path, list of slot ids needing fill, suggested
assignee (if Recomby team has roles configured), suggested due date
(default: +5 days from generation).

---

## Hard Rules

1. **Brief never gets shipped without expert fill** — 05-production reads
   `briefs/<id>.meta.json` and refuses to run if `status !=
   ready-for-production`. The status flips only when all `slots[*].filled
   == true` (see Step 9). Validate `briefs/<id>.meta.json` against
   `schemas/brief_meta.schema.json` after every write — the status enum
   (`awaiting-expert-fill` | `ready-for-production`, lowercase, case-sensitive)
   is the production gate and must match exactly.
2. **No AI-fillable slots** — every REQUIRED-FILL slot must be something
   that requires the brand's specific knowledge. If GPT-4 with Google
   could fill it, replace it with a tighter slot.
3. **Voice samples consulted, not optional** — every brief includes a
   voice-notes section. Skipping = generic content.
4. **The angle test** — write the angle, then ask: "could a competitor
   write this exact angle convincingly?" If yes, sharpen until no.

### Step 9 — Filling protocol (run when expert returns the brief)

The expert can return work two ways: an edited `.md`, or a `*.feedback.json`
exported from the interactive HTML (preferred — it's what non-technical
reviewers use).

**If a `*.feedback.json` came back** (validate it against
`schemas/review_feedback.schema.json` first):
1. For each key in `answers`, replace the matching `REQUIRED-FILL · <id>`
   block in `briefs/<id>.md` with the expert's text, keeping the `<id>` so
   05-production can still read it. The `answers` values are the human's
   real input — paste them verbatim, do not rewrite them.
2. Preserve `comments` (overall + per-section) in the hand-off to the user
   so the operator sees the reviewer's notes.
3. Then run steps 1–4 below against the now-filled `.md`.

**General protocol (both paths):**
1. Re-read the brief. For each slot id, verify the REQUIRED-FILL block
   has been replaced with substantive content.
2. Update `briefs/<id>.meta.json` slots[].filled = true and record
   filled_by + filled_at.
3. If all slots filled: set `status: ready-for-production`. Else: keep
   `awaiting-expert-fill` and report which slots are still empty.
4. **Do NOT auto-fill empty slots with AI content.** That defeats the
   entire purpose of this command.

---

## Reference

- `content-writer` (vendored from nowork-studio/toprank) — outline
  scaffolding inspiration; we borrow structure and add slot discipline.
- `meta-tags-optimizer` (vendored from nowork-studio/toprank) — headline
  / title slot conventions.
- `seo-geo-optimizer` (vendored from 199-biotechnologies) — entity
  extraction (`scripts/entity_extractor.py`) for citation pre-population.
- `references/auriti/princeton-geo-methods.md` — empirical justification
  for the statistics + quotation + citation mandatory blocks.
- `geo-review-html` (original) — renders the interactive fill-form HTML in
  Step 7 and defines the `*.feedback.json` contract ingested in Step 9.
- `frontend-design` (vendored from anthropics/skills) — visual quality of
  the review HTML; restyle the template's CSS with it for client branding.

---

## Hand-off

When status flips to `ready-for-production`, signal:
*"Brief <id> filled and approved. Run 05-production to draft."*
