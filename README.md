# recomby-geo

A Claude Code plugin that turns GEO (Generative Engine Optimization) into a
reproducible 7-stage pipeline. You drop client materials into a folder,
type `/01-intake clients/<name>` through `/07-reaudit`, and each stage
writes a JSON file the next stage reads.

> **Status**: v0.3.0 · alpha · zero external deps · zero API keys

---

## Who this is for

- **GEO consultants** who want a reproducible workflow instead of ad-hoc
  prompting per client.
- **In-house marketing teams** running monthly visibility audits across
  AI search engines.
- **Future agents picking this up cold** — the [Handoff section](#handoff--for-the-next-agent-picking-this-up) at the bottom is explicitly for you.

---

## Install (60 seconds)

```bash
# In a Claude Code session:
/plugin marketplace add recomby-ai/recomby-geo
/plugin install recomby-geo
```

That's it. No API keys to configure. No upstream skills to install.
The plugin bundles 6 canonical open-source skills plus the 7 workflow
commands.

**Local development**:
```bash
git clone https://github.com/recomby-ai/recomby-geo.git
# In Claude Code:
/plugin marketplace add /absolute/path/to/recomby-geo
/plugin install recomby-geo
```

---

## Quickstart — 5-minute walkthrough on a fake client

```bash
# 1. Make a client folder somewhere in your project
mkdir -p clients/demo-co/inputs

# 2. Drop materials in. For the demo, just one URL list works:
cat > clients/demo-co/inputs/urls.txt <<'EOF'
https://demo-co.example/about
https://demo-co.example/blog/best-crm-2026
EOF
```

Now in Claude Code:

```
/01-intake clients/demo-co
```

What happens:
1. The command reads `inputs/`, runs WebFetch on each URL.
2. Asks you targeted questions for the 5 hard-required Layer-1 fields
   (company name, ICP, competitors, differentiator, moat).
3. Spawns a Claude sub-agent to scout AI perception of your category
   (Layer 2).
4. Writes `clients/demo-co/brand_context.json` (validated against
   schema) and appends to `intake-log.md`.

**Verify**: `cat clients/demo-co/brand_context.json | jq '.layer_1_business_identity.company.name'`

Then:

```
/02-audit clients/demo-co
```

This spawns a fresh Claude sub-agent (with NO client context) for each
target query, captures what it answers, regex-extracts brand mentions,
WebFetch-verifies cited URLs are live. Outputs:
- `visibility_baseline.json` — machine-readable
- `baseline-report.md` — human-readable headline numbers

**Verify**: `cat clients/demo-co/baseline-report.md`

Continue: `/03-gap` → `/04-content-brief --priority <id>` → expert fills
the brief → `/05-production --priority <id>` → `/06-distribution
--priority <id>` → publish → next month: `/07-reaudit`.

**Full per-client run cycle visualized**: see [`plugins/recomby-geo/orchestrator/run.md`](plugins/recomby-geo/orchestrator/run.md).

---

## The 7 commands

Each command is a slash command you type in Claude Code. Each writes a
specific JSON output that the next command reads.

| # | Command | Reads | Writes | If it breaks, check |
|---|---------|-------|--------|---------------------|
| 01 | `/01-intake <client>` | `inputs/` (PDF/DOCX/PPTX/URL/notes) | `brand_context.json`, `intake-log.md` | Layer-1 fields all substantive (no "TBD"); competitors WebFetched |
| 02 | `/02-audit <client>` | `brand_context.json` | `visibility_baseline.json`, `baselines/round-N.json`, `baseline-report.md` | Every cited URL has `verified_live` set; sub-agent had NO client context |
| 03 | `/03-gap <client>` | `brand_context.json` + `visibility_baseline.json` | `content_priorities.json` | Every priority has ≥1 `required_asset` of type `original-data`/`expert-quote`/`customer-case`/`methodology-detail` |
| 04 | `/04-content-brief <client> --priority <id>` | `content_priorities.json` | `briefs/<id>.md` (with REQUIRED-FILL slots), `briefs/<id>.meta.json` | Status starts as `awaiting-expert-fill`; expert returns it filled; re-run command Step 9 to flip to `ready-for-production` |
| 05 | `/05-production <client> --priority <id>` | `briefs/<id>.md` (filled) | `drafts/<id>.md`, `drafts/<id>.meta.json` | Hard-refuses if brief status ≠ `ready-for-production`; verifies slot fills are substantive |
| 06 | `/06-distribution <client> --priority <id>` | `drafts/<id>.md` | `distribution/<id>.json` (schema + links + llms.txt), `distribution/<id>.publish-bundle.md`, append to `distribution/log.jsonl` | JSON-LD validates via Rich Results Test URL embedded in publish-bundle |
| 07 | `/07-reaudit <client>` | previous `visibility_baseline.json` + `distribution/log.jsonl` | `reaudit/round-N.json`, `reaudit/round-N.report.md`, fresh `visibility_baseline.json` | 7-day re-index buffer respected; same query set across rounds |

Full procedures live under [`plugins/recomby-geo/commands/`](plugins/recomby-geo/commands/).

---

## The 6 bundled skills (commodity capabilities)

Skills are model-invoked — Claude picks them up automatically based on
description matching when a command's procedure calls for them. You
don't invoke them directly.

| Skill | Source | Used by |
|-------|--------|---------|
| `seo-geo-optimizer` | [`199-biotechnologies/...`](https://github.com/199-biotechnologies/claude-skill-seo-geo-optimizer) (MIT) | 02-audit, 04 (entity), 05 (voice/citation), 06 (schema/entity), 07 (freshness) — its 13 stdlib Python scripts are the workhorse |
| `content-writer` | [`nowork-studio/toprank`](https://github.com/nowork-studio/toprank) (MIT) | 05-production prose engine |
| `content-quality-auditor` | [`aaron-he-zhu/...`](https://github.com/aaron-he-zhu/seo-geo-claude-skills) (Apache 2.0) | 03-gap CITE/EEAT scoring; 05 self-review |
| `internal-linking-optimizer` | aaron-he-zhu (Apache 2.0) | 06-distribution internal links |
| `keyword-research` | toprank (MIT) | 03-gap cluster expansion |
| `meta-tags-optimizer` | toprank (MIT) | 06-distribution title / meta description |

License attribution: [`THIRD_PARTY_LICENSES.md`](THIRD_PARTY_LICENSES.md).

---

## Per-client folder layout (single source of truth)

```
clients/<slug>/
├── inputs/                          # raw materials you drop in
│   ├── company-deck.pdf
│   ├── urls.txt
│   └── founder-notes.md
├── brand_context.json               # ← /01-intake writes
├── intake-log.md                    # ← /01-intake appends
├── visibility_baseline.json         # ← /02-audit writes (latest round)
├── baselines/                       # historical baselines preserved
│   └── round-N.json
├── baseline-report.md               # ← /02-audit writes
├── content_priorities.json          # ← /03-gap writes
├── briefs/
│   ├── <priority-id>.md             # ← /04-content-brief writes (with slots)
│   └── <priority-id>.meta.json      # tracks slot fill status
├── drafts/
│   ├── <priority-id>.md             # ← /05-production writes
│   └── <priority-id>.meta.json
├── distribution/
│   ├── <priority-id>.json           # ← /06-distribution writes
│   ├── <priority-id>.publish-bundle.md
│   └── log.jsonl                    # append-only action log
└── reaudit/
    ├── round-N.json                 # ← /07-reaudit writes
    └── round-N.report.md
```

`clients/<slug>/` lives in the **consumer's** project tree, not inside
this plugin repo. By default it's gitignored (each client's data is
private).

---

## The 4 schema contracts

JSON Schemas (Draft 2020-12) under `plugins/recomby-geo/schemas/`. Each
command validates its output before signaling readiness — a malformed
artifact never reaches the next stage.

| Schema | Owner stage |
|--------|-------------|
| `brand_context.schema.json` | 01-intake |
| `visibility_baseline.schema.json` | 02-audit + 07-reaudit |
| `content_priorities.schema.json` | 03-gap |
| `attribution_diff.schema.json` | 07-reaudit |

Validate any client output any time:

```bash
python3 -c "import json,jsonschema; \
  s=json.load(open('plugins/recomby-geo/schemas/brand_context.schema.json')); \
  d=json.load(open('clients/<slug>/brand_context.json')); \
  jsonschema.validate(d,s); print('OK')"
```

---

## Invariants you must not violate

These are the things that, if you break, the pipeline silently produces
garbage. They're enforced inside each command but documented here for
visibility.

1. **Brief status state machine** — `awaiting-expert-fill` →
   `ready-for-production` (only after every REQUIRED-FILL slot is
   replaced with substantive content). 05-production hard-refuses if
   status ≠ `ready-for-production`. **Never auto-fill expert slots
   with AI content.** That defeats the entire human-in-loop purpose.

2. **WebFetch before trust** — every competitor URL, every cited URL,
   every citation source must be WebFetch-verified. AI engines
   hallucinate URLs. A baseline polluted with hallucinated citations
   ruins 07-reaudit's attribution forever.

3. **02-audit sub-agent has NO client context** — the whole point of
   measuring visibility is "what would Claude tell a stranger?". If
   the sub-agent knows the brand, the answer is biased. Pass NO
   brand_context into the query runner.

4. **Same query set across audit rounds** — diff requires
   apples-to-apples. New queries are flagged but adopted next round.

5. **7-day re-index buffer** — actions shipped <7 days before re-audit
   are diagnosed `too-recent`, not `weak-content`. Don't over-credit
   yourself or under-credit work that hasn't had time to land.

6. **Append-only log** — `clients/<slug>/distribution/log.jsonl` is the
   ONLY input 07-reaudit uses for action attribution. Skip a log
   entry → that action gets credited to nobody.

---

## Common gotchas

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `/01-intake` produces "TBD" / single-word entries in Layer 1 | Materials too thin; command should have asked, didn't | Re-run; it will ask now that schema validation fails |
| `/02-audit` mention_rate = 0 across all queries | Brand name regex too narrow (no aliases) | Add `aliases` to `layer_1_business_identity.company` in brand_context.json, re-run |
| `/03-gap` produces 30 priorities all of one `opportunity_type` | The 5-per-type cap wasn't enforced | Re-run; the command sorts and trims |
| `/05-production` refuses with "status=awaiting-expert-fill" | Brief slots haven't been filled by the expert | Have the expert fill REQUIRED-FILL slots, run `/04-content-brief --verify <id>` to flip status |
| `/07-reaudit` reports all queries `attribution_confidence: unknown` | `distribution/log.jsonl` missing entries for shipped actions | Append the missing log lines, re-run |
| Plugin install but commands don't show as `/01-intake` etc. | Stale plugin cache | `/plugin marketplace update recomby-ai/recomby-geo` then re-install |

---

## Architecture in one diagram

```
inputs/  →  /01-intake  →  brand_context.json
                              │
                              ▼
                          /02-audit  →  visibility_baseline.json
                              │             │
                              └────┬────────┘
                                   ▼
                                /03-gap  →  content_priorities.json
                                   │
                                   ▼
                       /04-content-brief  →  briefs/<id>.md (with slots)
                                   │
                            [EXPERT FILLS]
                                   │
                                   ▼
                          /05-production  →  drafts/<id>.md
                                   │
                                   ▼
                         /06-distribution  →  distribution/<id>.json
                                   │
                            [PUBLISH + WAIT 7+ days]
                                   │
                                   ▼ (monthly)
                              /07-reaudit  →  reaudit/round-N.json
                                   │
                                   └──→ feeds next /03-gap run
```

Two-tier Claude Code architecture:
- `commands/` — workflow entrypoints user types (`/01-intake`)
- `skills/` — commodity capabilities the model picks up automatically

Stages CALL skills. Stages are NOT skills.

---

## Why these design choices

- **Claude-only 02-audit** (not multi-LLM) — BYOK across ChatGPT/
  Perplexity/Gemini turns this into an ops project. Single-engine
  reproducible beats multi-engine flaky. The vendored
  `seo-geo-optimizer` has multi-engine paths if you later need them.
- **Human-in-loop in 04-content-brief** — every priority must include
  ≥1 expert input slot. AI-fillable content doesn't get cited by AI
  engines (Princeton KDD 2024). The slot discipline is the moat.
- **Per-client folder convention, not multi-tenant DB** — moving from
  one client to N is a directory copy, not a schema migration. Optimize
  for first-hire / first-client legibility.
- **6 canonical skills, no overlap** — `one tool per job` Unix
  discipline. v0.2 had 21 vendored skills with 5 redundant pairs;
  cutting drift risk + UX noise was worth more than "options".

---

## Handoff — for the next agent picking this up

If you (Claude or human) are inheriting this codebase cold, read this
section first.

**The 30-second mental model**:
> Per-client folder + 7 numbered slash commands that each write a JSON
> file with a schema contract. Stages CALL the 6 vendored commodity
> skills. Brief status is a hard gate — drafts won't generate from an
> unfilled brief. Audit baselines are Claude-only; 7-day re-index
> buffer; same query set across rounds for diff-ability.

**Where to look first when something seems wrong**:
1. `clients/<slug>/<stage>.json` — does it validate against the schema?
   Run the validator one-liner in the [Schemas](#the-4-schema-contracts)
   section.
2. The corresponding `commands/0N-*.md` — the procedure is the source
   of truth for what each stage SHOULD do.
3. `CLAUDE.md` (gitignored, maintainer-only) — has the WHY behind
   non-obvious choices, vendor decisions, and known limits not yet in
   the public README.

**Key conventions, in priority order**:
1. **Schema validation is the boundary** — every stage validates its
   output before signaling readiness. If you bypass validation, you're
   poisoning every downstream stage.
2. **Append, never overwrite logs** — `intake-log.md`,
   `distribution/log.jsonl`. 07-reaudit reads them.
3. **Round numbers in baselines never reset** — `meta.audit_round` is
   monotonic. 07-reaudit increments it.
4. **Confirm before write** — 01-intake asks the user before persisting
   `brand_context.json`. Don't bypass; the moat sentence + AI perception
   findings need human sign-off.

**Things that look like bugs but are intentional**:
- 02-audit sub-agent doesn't know about the client → that's the whole
  point. Don't "improve" it by passing brand_context.
- 04-content-brief refuses to start drafts → the human must fill slots
  first. Don't "fix" by auto-generating.
- `meta.audit_round` field exists in round-1 baseline → yes, it starts
  at 1, increments only via 07-reaudit.
- Slot annotations (`<!-- slot: ... -->`) survive into 05-production
  drafts → 06-distribution audits them and the publish-bundle checklist
  has a "strip before publishing" step. Don't strip them earlier.

**What's NOT done yet** (real future work, not bike-shedding):
- No end-to-end smoke test on a real client. SEA-CICSIC W2 audit
  (deadline 2026-05-13) is the first real run; protocol mismatches
  between commands and vendored skills will surface there.
- The 7 `commands/0N-*.md` were converted from SKILL.md format. The
  body prose still occasionally says "this skill" — search and patch
  if you spot it.
- Optional cross-engine audit (ChatGPT/Perplexity/Gemini) is documented
  in 02-audit but not implemented. `seo-geo-optimizer/scripts/
  platform_optimizer.py` has the per-engine logic if you wire it up.
- No CI / hooks enforcing schema validation. Every command documents
  it as a Step but agents reliably running that step is unverified.

**Repo conventions**:
- `CLAUDE.md` at repo root is gitignored — maintainer notes only.
- `README.md` (this file) is the public face.
- Vendored skills' original LICENSE is preserved either inside the
  skill folder or referenced from `THIRD_PARTY_LICENSES.md`.
- Bump `plugin.json` version on any change to vendored skills or
  command procedures.

---

## Repo layout

```
recomby-geo/
├── .claude-plugin/marketplace.json
├── plugins/recomby-geo/
│   ├── plugin.json
│   ├── orchestrator/run.md
│   ├── commands/                        # 7 slash commands (workflow)
│   │   └── 0{1..7}-*.md
│   ├── skills/                          # 6 commodity skills (capabilities)
│   │   ├── seo-geo-optimizer/
│   │   ├── content-writer/
│   │   ├── content-quality-auditor/
│   │   ├── internal-linking-optimizer/
│   │   ├── keyword-research/
│   │   └── meta-tags-optimizer/
│   ├── schemas/                         # 4 JSON schemas
│   └── references/                      # docs (auriti/, awesome-geo.md)
├── README.md                            # this file
├── CLAUDE.md                            # gitignored maintainer notes
├── THIRD_PARTY_LICENSES.md
└── .gitignore
```

---

## License

The Recomby.ai originals (the 7 commands, 4 schemas, orchestrator, this
README) are private alpha — license finalized before public release.

The 6 bundled skills and 2 reference doc sets retain their original
licenses (MIT / Apache 2.0 / CC0); see [`THIRD_PARTY_LICENSES.md`](THIRD_PARTY_LICENSES.md).
