# Third-Party Licenses

`recomby-geo` bundles 7 open-source Claude skills and 2 sets of reference
documentation, all under permissive licenses (MIT / Apache 2.0 / CC0).

The original `LICENSE` file from each upstream is preserved either inside
the vendored skill folder (where the upstream put it) or referenced
below by repo URL.

---

## Vendored skills (7, one per capability)

### `seo-geo-optimizer`
- **Upstream**: [`199-biotechnologies/claude-skill-seo-geo-optimizer`](https://github.com/199-biotechnologies/claude-skill-seo-geo-optimizer)
- **License**: MIT, © 2025 Boris Djordjevic, 199 Biotechnologies
- **What it brings**: comprehensive SEO/GEO/AEO toolkit with 13 pure-stdlib
  Python scripts (audit_report, entity_extractor, schema_generator,
  voice_optimizer, citation_enhancer, freshness_monitor, etc.) plus
  JSON-LD templates and platform-specific profile presets.
- **LICENSE preserved at**: `plugins/recomby-geo/skills/seo-geo-optimizer/LICENSE`

### `content-writer`
- **Upstream**: [`nowork-studio/toprank`](https://github.com/nowork-studio/toprank) (MIT, © 2026 Toprank Contributors / NotFair)
- **What it brings**: outline-to-prose generation patterns + content templates.
- **Source path**: `seo/content-writer/`

### `keyword-research`
- **Upstream**: [`nowork-studio/toprank`](https://github.com/nowork-studio/toprank) (MIT, © 2026 Toprank Contributors / NotFair)
- **What it brings**: keyword clustering and intent taxonomy.
- **Source path**: `seo/keyword-research/`

### `meta-tags-optimizer`
- **Upstream**: [`nowork-studio/toprank`](https://github.com/nowork-studio/toprank) (MIT, © 2026 Toprank Contributors / NotFair)
- **What it brings**: title-tag and meta-description formulas with CTR data.
- **Source path**: `seo/meta-tags-optimizer/`

### `content-quality-auditor`
- **Upstream**: [`aaron-he-zhu/seo-geo-claude-skills`](https://github.com/aaron-he-zhu/seo-geo-claude-skills)
- **License**: Apache 2.0, © Aaron He Zhu
- **What it brings**: CITE × CORE-EEAT scoring framework for 03-gap.
- **Source path**: `cross-cutting/content-quality-auditor/`

### `internal-linking-optimizer`
- **Upstream**: [`aaron-he-zhu/seo-geo-claude-skills`](https://github.com/aaron-he-zhu/seo-geo-claude-skills) (Apache 2.0, © Aaron He Zhu)
- **What it brings**: link-equity-aware internal linking framework.
- **Source path**: `optimize/internal-linking-optimizer/`

### `frontend-design`
- **Upstream**: [`anthropics/skills`](https://github.com/anthropics/skills/tree/main/skills/frontend-design)
- **License**: Apache 2.0, © Anthropic (commit `da20c92`)
- **What it brings**: prompt-only design guidance (typography, color,
  motion, spatial composition) that steers the model away from generic
  "AI slop" aesthetics when generating the client-review HTML in
  `04-content-brief` / `05-production`. Pure markdown, no scripts.
- **LICENSE preserved at**: `plugins/recomby-geo/skills/frontend-design/LICENSE.txt`

---

## Vendored reference documentation

### `references/auriti/`
- **Upstream**: [`Auriti-Labs/geo-optimizer-skill`](https://github.com/Auriti-Labs/geo-optimizer-skill)
- **License**: MIT, © 2026 Juan Camilo Auriti
- **Vendored files**: `princeton-geo-methods.md`, `ai-bots-list.md`,
  `schema-templates.md`, `LICENSE`
- **Why only docs (not the SKILL.md)**: Auriti's SKILL.md delegates to
  a `geo` Python CLI built from its `src/` package. We didn't vendor
  the CLI — its docs are the high-leverage part.

### `references/awesome-geo.md`
- **Upstream**: [`luka2chat/awesome-geo`](https://github.com/luka2chat/awesome-geo)
- **License**: CC0 1.0 Universal
- **What it is**: annotated index of GEO papers, tools, and resources.

---

## How to refresh a vendored skill

```bash
# Example: refresh content-writer from upstream
git clone --depth=1 https://github.com/nowork-studio/toprank.git /tmp/toprank
rm -rf plugins/recomby-geo/skills/content-writer
cp -r /tmp/toprank/seo/content-writer plugins/recomby-geo/skills/content-writer
# Bump plugin.json version after any vendor refresh
```

---

## Recomby.ai original code

Commands `01-intake`, `02-audit`, `03-gap`, `04-content-brief`,
`05-production`, `06-distribution`, `07-reaudit`, the `geo-review-html`
and `geo-pipeline` skills, the JSON schemas, the orchestrator, and `THIRD_PARTY_LICENSES.md`
itself are © Recomby.ai
and licensed under the same terms as this plugin's top-level LICENSE
(see repository root, finalized before public release).
