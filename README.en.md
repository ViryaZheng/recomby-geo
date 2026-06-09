# recomby-geo

## An open-source AI-employee solution for the GEO domain

A curated hub that bundles Agents, office CLIs, and GEO domain skills into a **collaborative AI-employee solution**—equip your agent with GEO skills, then let it collaborate with your business expert on real GEO work.

> alpha · zero external deps · zero API keys · [Changelog](CHANGELOG.md) · [中文版](README.md)

---

## What "AI Employee Solution" means

Not "AI replacing employees", but **a virtual role assembled from four parts**. All four required:

```
       Business expert                    Agent
   (you / client team, owns)     (CC / Codex / ..., local model-capable)
              │                              │
              └──────────── ╳ ───────────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
        Office CLI layer             GEO Skills
   (Lark / DingTalk / Slack /     (← this project's
    Notion ...)                     primary focus)
   Data source + scaffolding      Expertise enablement
```

| Role | Provided by | This project's collection / dev |
|------|-------------|---------------------------------|
| Business expert | You / client team | — |
| Agent | CC / Codex / OpenCode / ... ecosystem | ✓ Collection → [`agents.md`](agents.md) |
| Data + CLI scaffolding | Lark / DingTalk / Slack / Notion ... | ✓ Collection → [`clis.md`](clis.md) |
| **GEO Skills** | **Maintained by Recomby + vendored OSS** | ✓ Primary focus → [`plugins/recomby-geo/skills/`](plugins/recomby-geo/skills/) |

We do three things: **curate mainstream Agent CLIs, curate office CLIs (CN + global), package GEO domain skills**.

---

## Our primary focus: GEO Skills

> **`plugins/recomby-geo/` (commands + skills + schemas) is the area we actively maintain and continue to invest in** — MIT-licensed, commercial-use OK, modify-and-redistribute OK.

What we do is package GEO domain knowledge into agent-callable skills, plus a complete 7-stage collaborative workflow. Much of the underlying structure and methodology draws from open-source work — Princeton KDD 2024 GEO paper, Auriti Labs, awesome-geo, and the vendored skills' upstream authors. What we add is the assembly, polish, and re-packaging for the AI-employee context.

`agents.md` and `clis.md` are **not separate products** — they are **solution architecture pages**: they show where the GEO Skills fit in the "Business expert + Agent + Office CLI + Skills" AI-employee stack, and which agents / CLIs to pair them with. They give readers the ecosystem picture, but **the primary focus is the Skills**.

---

## Local-first deployment · data never leaves local

This solution is **Local-first** by design—the key differentiator vs cloud SaaS GEO tools (SurferSEO / Frase / Clearscope) that require uploading client data to their cloud:

- **Agent runs local models** — CC / Codex etc. all support local LLMs (Ollama / vLLM / LM Studio)
- **Office data stays local** — Lark / DingTalk etc. CLIs run in your environment, business data never hits third-party clouds
- **Whole stack open source** — all vendored skills are MIT / Apache 2.0, auditable and customizable
- **Compliance-friendly** — required for CN data compliance, regulated industries, internal-only material

---

## GEO Skills inventory (core)

Under `plugins/recomby-geo/skills/` we package 6 GEO domain skills, **model-invoked automatically by description match**—you don't call them directly:

| Skill | Source | Purpose |
|-------|--------|---------|
| `seo-geo-optimizer` | [199-biotechnologies](https://github.com/199-biotechnologies/claude-skill-seo-geo-optimizer) (MIT) | Workhorse, 13 Python scripts |
| `content-writer` | [toprank](https://github.com/nowork-studio/toprank) (MIT) | Content production |
| `content-quality-auditor` | [aaron-he-zhu](https://github.com/aaron-he-zhu/seo-geo-claude-skills) (Apache 2.0) | E-E-A-T / citation audit |
| `internal-linking-optimizer` | aaron-he-zhu (Apache 2.0) | Internal links |
| `keyword-research` | toprank (MIT) | Keyword expansion |
| `meta-tags-optimizer` | toprank (MIT) | Title / meta |

Plus 7 GEO workflow commands under `plugins/recomby-geo/commands/` (`/01-intake` through `/07-reaudit`) — together they form the complete GEO AI-employee capability pack. **This is our primary focus area going forward.**

Licensing: [`LICENSE`](LICENSE) and [`THIRD_PARTY_LICENSES.md`](THIRD_PARTY_LICENSES.md).

---

## Ecosystem context: Agent + Office CLI

Which agent runs the Skills, which office CLIs feed the data—these two pages are the **solution architecture context**, not separate products:

- **[Agent collection → `agents.md`](agents.md)** — Mainstream AI agent CLIs that can load skills: CC, Codex CLI, OpenCode, Cline, Goose, ByteDance Trae, etc.
- **[Office CLI collection → `clis.md`](clis.md)** — Letting agents access business data: Lark / DingTalk / WeCom / Yuque (CN) + Slack / Notion / GitHub / Linear / Google Workspace / Jira (Global)

These two pages show the full AI-employee stack (agent = body, office CLI = limbs), but **what you actually install is the GEO Skills**.

---

## Why GEO is the best testbed for the "AI employee" paradigm

GEO is **inherently non-fully-automatable**—and that's the advantage:

- Generative search engines actively penalize AI-generated slop; only real business insight gets cited
- Business insight can only come from business experts—no AI substitute exists
- So an "AI employee" in GEO **must be collaborative**; "AI replaces employee" is a non-starter

Result: client decision-makers grasp it instantly, low landing friction (no replacement anxiety for the expert), clear value attribution.

GEO is the showcase battleground for the collaborative AI-employee paradigm.

---

## Getting started

```bash
# 1. Install the plugin in Claude Code (GEO Skills + 7-stage workflow commands)
/plugin marketplace add recomby-ai/recomby-geo
/plugin install recomby-geo

# 2. Prepare a project folder
mkdir -p clients/<your-project>/inputs
# Drop materials (PDF / URL / notes) into inputs/

# 3. Start the collaborative workflow
/01-intake clients/<your-project>
# Then: /02-audit → /03-gap → /04-content-brief → ...
```

Full run flow: [`plugins/recomby-geo/orchestrator/run.md`](plugins/recomby-geo/orchestrator/run.md)

> **Not on Claude Code?** — In any other skill/plugin-loading agent (see [`agents.md`](agents.md)), copy `plugins/recomby-geo/skills/` into your loader directly.

---

## Collaborative workflow (business-expert view)

The GEO workflow has 7 stages. The **middle stage—"expert fills the brief"—is the point**: the agent prepares the scaffold; the business insight must come from a human. This embodies the collaborative essence:

```
  /01-intake → /02-audit → /03-gap → /04-content-brief
                                            │
                                  ┌─────────┘
                                  ▼
                       [Business expert fills insight slots]
                                  │
                                  ▼
  /05-production → /06-distribution → publish → 7+ days later /07-reaudit
```

Stage docs: [`plugins/recomby-geo/commands/`](plugins/recomby-geo/commands/)

**Hard constraints**:
- `/05-production` hard-refuses when brief status ≠ `ready-for-production`—if expert slots aren't filled, the agent will NOT auto-fill with AI content. This is the collaboration gate.
- `/02-audit` runs queries via a sub-agent with NO client context, simulating a stranger asking an AI engine.
- Every stage output validates against a JSON Schema before the next stage proceeds.

---

## Repo layout

```
recomby-geo/
├── README.md                         # 中文 (this file's counterpart)
├── README.en.md                      # this file
├── agents.md                         # Agent collection (curated)
├── clis.md                           # Office CLI collection (CN + global)
├── LICENSE                           # MIT
├── plugins/recomby-geo/
│   ├── plugin.json
│   ├── orchestrator/run.md           # full run flow
│   ├── commands/                     # 7 workflow commands
│   ├── skills/                       # 7 vendored + original skills
│   ├── schemas/                      # 8 JSON Schemas
│   └── references/                   # Princeton GEO, etc.
├── THIRD_PARTY_LICENSES.md
└── .gitignore
```

---

## License

This repo is maintained by Recomby.ai. Our primary focus going forward is `plugins/recomby-geo/` (commands, 8 schemas, orchestrator, skills selection) and the two architecture pages `agents.md` / `clis.md`. The assembly and packaging are ours (much of the underlying material is drawn from open-source community work; see below and `THIRD_PARTY_LICENSES.md`). The whole repo is released under the **MIT License**—see [`LICENSE`](LICENSE).

The 7 vendored skills retain their original licenses (MIT / Apache 2.0); the original skill (geo-review-html) ships under the repo's MIT license; see [`THIRD_PARTY_LICENSES.md`](THIRD_PARTY_LICENSES.md).

---

# Appendix · Plugin internals reference

The sections below document the GEO Skills package in detail — useful if you want to extend / debug / fork the commands or schemas.

## The 7 commands

Each command is a slash command typed in Claude Code. Each writes a specific JSON output the next command reads.

| # | Command | Reads | Writes | If it breaks, check |
|---|---------|-------|--------|---------------------|
| 01 | `/01-intake <client>` | `inputs/` (PDF/DOCX/PPTX/URL/notes) | `brand_context.json`, `intake-log.md` | Layer-1 fields all substantive (no "TBD"); competitors WebFetched |
| 02 | `/02-audit <client>` | `brand_context.json` | `visibility_baseline.json`, `baselines/round-N.json`, `baseline-report.md` | Every cited URL has `verified_live` set; sub-agent had NO client context |
| 03 | `/03-gap <client>` | `brand_context.json` + `visibility_baseline.json` | `content_priorities.json` | Every priority has ≥1 `required_asset` of type `original-data`/`expert-quote`/`customer-case`/`methodology-detail` |
| 04 | `/04-content-brief <client> --priority <id>` | `content_priorities.json` | `briefs/<id>.md` (with REQUIRED-FILL slots), `briefs/<id>.meta.json` | Status starts as `awaiting-expert-fill`; expert returns it filled; re-run command Step 9 to flip to `ready-for-production` |
| 05 | `/05-production <client> --priority <id>` | `briefs/<id>.md` (filled) | `drafts/<id>.md`, `drafts/<id>.meta.json` | Hard-refuses if brief status ≠ `ready-for-production`; verifies slot fills are substantive |
| 06 | `/06-distribution <client> --priority <id>` | `drafts/<id>.md` | `distribution/<id>.json` (schema + links + llms.txt), `distribution/<id>.publish-bundle.md`, append to `distribution/log.jsonl` | JSON-LD validates via Rich Results Test URL embedded in publish-bundle |
| 07 | `/07-reaudit <client>` | previous `visibility_baseline.json` + `distribution/log.jsonl` | `reaudit/round-N.json`, `reaudit/round-N.report.md`, fresh `visibility_baseline.json` | 7-day re-index buffer respected; same query set across rounds |

Full procedures: [`plugins/recomby-geo/commands/`](plugins/recomby-geo/commands/).

## Per-client folder layout (single source of truth)

```
clients/<slug>/
├── inputs/                          # raw materials you drop in
├── brand_context.json               # ← /01-intake writes
├── intake-log.md                    # ← /01-intake appends
├── visibility_baseline.json         # ← /02-audit writes (latest round)
├── baselines/round-N.json           # historical baselines preserved
├── baseline-report.md
├── content_priorities.json          # ← /03-gap writes
├── briefs/<priority-id>.md          # ← /04-content-brief writes
├── briefs/<priority-id>.meta.json   # tracks slot fill status
├── drafts/<priority-id>.md          # ← /05-production writes
├── distribution/<priority-id>.json  # ← /06-distribution writes
├── distribution/log.jsonl           # append-only action log
└── reaudit/round-N.json             # ← /07-reaudit writes
```

`clients/<slug>/` lives in the **consumer's** project tree, not this plugin repo. Gitignored by default.

## The 4 schema contracts

JSON Schemas (Draft 2020-12) under `plugins/recomby-geo/schemas/`. Each command validates its output before signaling readiness—a malformed artifact never reaches the next stage.

| Schema | Owner stage |
|--------|-------------|
| `brand_context.schema.json` | 01-intake |
| `visibility_baseline.schema.json` | 02-audit + 07-reaudit |
| `content_priorities.schema.json` | 03-gap |
| `attribution_diff.schema.json` | 07-reaudit |

Validate any client output anytime:

```bash
python3 -c "import json,jsonschema; \
  s=json.load(open('plugins/recomby-geo/schemas/brand_context.schema.json')); \
  d=json.load(open('clients/<slug>/brand_context.json')); \
  jsonschema.validate(d,s); print('OK')"
```

## Invariants you must not violate

1. **Brief status state machine** — `awaiting-expert-fill` → `ready-for-production` (only after every REQUIRED-FILL slot is replaced with substantive content). 05-production hard-refuses if status ≠ `ready-for-production`. **Never auto-fill expert slots with AI content.**
2. **WebFetch before trust** — every competitor URL, every cited URL must be WebFetch-verified. AI engines hallucinate URLs.
3. **02-audit sub-agent has NO client context** — measuring visibility means "what would Claude tell a stranger?". Pass NO brand_context into the query runner.
4. **Same query set across audit rounds** — diff requires apples-to-apples. New queries are flagged but adopted next round.
5. **7-day re-index buffer** — actions shipped <7 days before re-audit are diagnosed `too-recent`, not `weak-content`.
6. **Append-only log** — `clients/<slug>/distribution/log.jsonl` is the ONLY input 07-reaudit uses for action attribution.

## Handoff — for the next agent picking this up

**The 30-second mental model**:
> Per-client folder + 7 numbered slash commands that each write a JSON file with a schema contract. Stages CALL the 7 vendored commodity skills (plus the original geo-review-html renderer). Brief status is a hard gate—drafts won't generate from an unfilled brief. Audit baselines are Claude-only; 7-day re-index buffer; same query set across rounds for diff-ability.

**Where to look first when something seems wrong**:
1. `clients/<slug>/<stage>.json` — does it validate against the schema?
2. The corresponding `commands/0N-*.md` — the procedure is the source of truth.
3. `CLAUDE.md` (gitignored, maintainer-only) — has the WHY behind non-obvious choices.

**Things that look like bugs but are intentional**:
- 02-audit sub-agent doesn't know about the client → that's the whole point.
- 04-content-brief refuses to start drafts → the human must fill slots first.
- Slot annotations (`<!-- slot: ... -->`) survive into 05-production drafts → 06-distribution audits them; publish-bundle has a "strip before publishing" step.

**What's NOT done yet**:
- No end-to-end smoke test on a real client.
- The 7 `commands/0N-*.md` were converted from SKILL.md format; "this skill" residues have been patched.
- Optional cross-engine audit (ChatGPT/Perplexity/Gemini) is documented in 02-audit but not implemented.
- No CI / hooks enforcing schema validation beyond the per-command Step.
