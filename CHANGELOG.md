# Changelog

All notable changes to **recomby-geo** are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Each release is a git tag — fall back to any version with
`git checkout vX.Y.Z`, or browse/download it from the
[Releases page](https://github.com/recomby-ai/recomby-geo/releases).

## [Unreleased]

_Nothing yet._

## [0.4.2] — 2026-06-09

Whole-project review follow-up: closes the gaps that undercut the
"every artifact is schema-validated" guarantee, plus a brief-render fix.

### Added
- Three JSON schemas (Draft 2020-12): `brief_meta`, `draft_meta`,
  `distribution` — the brief status state machine (the human-in-loop
  production gate `05-production` enforces) and the draft/distribution
  artifacts previously had no schema despite the docs claiming validation.
  Total now 8 schemas; CI's glob picks them up automatically.

### Changed
- Brief `status` pinned to `awaiting-expert-fill` / `ready-for-production`
  (lowercase, case-sensitive) and wired explicit "validate against
  `schemas/X`" steps into commands 04 / 05 / 06.
- All four manifests bumped to 0.4.2; `.claude-plugin/marketplace.json`
  (stale at 0.3.0) corrected, skill/schema counts synced across README
  (zh/en) and `THIRD_PARTY_LICENSES.md` (6→7 vendored skills, 4→8 schemas).

### Fixed
- `render_html.py`: brief prose sections lost their headings —
  `parse_brief` stripped the heading line from the html and the template
  renders only `s.html` (never `s.heading`). Headings are now kept in the
  html (verified end-to-end).
- 07-reaudit: documented `query_id` immutability across rounds (the id is
  derived from the query text; editing it silently drops the query from
  the diff).

## [0.4.1] — 2026-06-01

### Added
- **Interactive client-review HTML** (refs #1): new `geo-review-html` skill
  (fixed templates + stdlib `render_html.py`, brief fill-form / draft
  review / index modes, self-contained output) and vendored
  `frontend-design` skill (Apache 2.0) for visual quality. New
  `review_feedback.schema.json`; CI schema check now globs all schemas.
- **OpenAI Codex CLI support**: `.codex-plugin/plugin.json`,
  `.agents/plugins/marketplace.json`, and a `geo-pipeline` orchestrator
  skill as the Codex entry point (Codex scans `skills/`; Claude keeps its
  explicit list, no overlap). `INSTALL.md` documents both runtimes.

### Changed
- Wired the review HTML into 04-content-brief (Step 7 render + Step 9
  feedback-JSON ingest) and 05-production (Step 7 review HTML).

## [0.4.0] — 2026-05-16

Positioning pivot: the project is a **GEO AI-employee open-source hub**.
`plugins/recomby-geo/` (GEO Skills) is the primary focus going forward;
`agents.md` / `clis.md` are solution-architecture context, not parallel
products.

### Added
- `LICENSE` (MIT), `CONTRIBUTING.md`, PR template, CI workflow (schema
  validation + `py_compile` + lychee link lint).
- `agents.md` (13 mainstream agent CLIs) and `clis.md` (13 office
  CLIs/MCP servers, CN + global).

### Changed
- README rewritten (CN + EN) around a single getting-started flow.
- `plugin.json` → 0.4.0; `.gitignore` excludes local-only material.

## [0.3.0] — 2026-05-09

Three architecture-grade fixes in one push.

### Added
- Bundles 6 canonical open-source skills directly under
  `plugins/recomby-geo/skills/` — zero external deps, zero API keys for
  the default flow (previously assumed users pre-installed them).
- `THIRD_PARTY_LICENSES.md`; Auriti Labs reference docs under
  `references/auriti/`.

### Changed
- Restructured workflow stages from `SKILL.md` into proper slash commands
  (`commands/0N-*.md`) — skills are model-invoked, commands are user-typed.
- 02-audit rewritten Claude-only (no multi-LLM BYOK); sub-agent runs with
  no client context.

### Removed
- Deduped 21 vendor skills down to 6 (one canonical impl per capability).
- `gego` (GPL v3) rejected to avoid license contagion.

## [0.1.0] — 2026-05-09

Initial 7-stage GEO orchestration plugin: 01-intake → 02-audit → 03-gap →
04-content-brief → 05-production → 06-distribution → 07-reaudit. Per-client
folder convention. Schemas (Draft 2020-12): `brand_context`,
`visibility_baseline`, `content_priorities`, `attribution_diff`.

[Unreleased]: https://github.com/recomby-ai/recomby-geo/compare/v0.4.2...HEAD
[0.4.2]: https://github.com/recomby-ai/recomby-geo/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/recomby-ai/recomby-geo/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/recomby-ai/recomby-geo/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/recomby-ai/recomby-geo/compare/v0.1.0...v0.3.0
[0.1.0]: https://github.com/recomby-ai/recomby-geo/releases/tag/v0.1.0
