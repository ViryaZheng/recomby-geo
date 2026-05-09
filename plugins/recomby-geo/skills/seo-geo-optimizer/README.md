# SEO/GEO/AEO Optimizer

Analysis and optimization toolkit for content visibility across search engines (SEO), AI platforms (GEO - Generative Engine Optimization), answer engines (AEO - Answer Engine Optimization), voice assistants, and social media.

**Author**: Boris Djordjevic, [199 Biotechnologies](https://199.bio)
**Status**: Phase 2 Complete (Content Implementation)
**License**: MIT
**Repository**: [github.com/199-biotechnologies/claude-skill-seo-geo-optimizer](https://github.com/199-biotechnologies/claude-skill-seo-geo-optimizer)

---

## Purpose

This skill audits and optimizes content for discoverability across:

- **Search engines**: Google, Bing (traditional SEO)
- **AI platforms**: ChatGPT, Perplexity, Claude, Gemini, Grokipedia (GEO - Generative Engine Optimization)
- **Answer engines**: Google AI Overviews, Bing Copilot, featured snippets (AEO - Answer Engine Optimization)
- **Voice assistants**: Google Assistant, Siri, Alexa
- **Social media**: Facebook, Twitter, LinkedIn, WhatsApp, Instagram

Supports HTML, Markdown, and React/JSX files.

---

## Key Statistics (2025)

AI-referred traffic grew 527% between January and May 2025. Content optimized for AI citation shows 33-40% higher visibility. Key findings:

- 40.58% of AI citations come from top 10 SERP results
- Content with author credentials: +40% citation probability
- Featured snippets: 40.7% of voice search answers
- Statistics addition: +41% citation improvement
- Freshness (<30 days): 3.2x more citations

---

## Installation

Clone to Claude skills directory:

```bash
cd ~/.claude/skills/
git clone https://github.com/199-biotechnologies/claude-skill-seo-geo-optimizer.git
```

Requirements: Python 3.7+, no external dependencies (stdlib only).

Verify installation:
```bash
python ~/.claude/skills/seo-geo-optimizer/scripts/analyze_content.py --help
```

---

## Usage

### Phase 1: Analysis

Audit existing content, generate recommendations:

```bash
# Comprehensive audit with all reports
python scripts/audit_report.py ~/project/page.html --format all

# Analyze specific aspects
python scripts/analyze_content.py ~/project/page.html
python scripts/metadata_validator.py ~/project/page.html
python scripts/keyword_analyzer.py ~/project/page.html
python scripts/entity_extractor.py ~/project/page.html
```

### Phase 2: Implementation

Apply optimizations automatically:

```bash
# Full optimization pipeline for specific platform
python scripts/auto_implementer.py page.html perplexity

# Individual optimization steps
python scripts/content_optimizer.py page.html
python scripts/platform_optimizer.py page.html chatgpt
python scripts/voice_optimizer.py page.html
python scripts/freshness_monitor.py page.html
python scripts/citation_enhancer.py page.html
```

### Keyword Clustering

Group related keywords into semantic clusters for topical authority:

```bash
# Analyze with keyword clusters (default)
python scripts/keyword_analyzer.py ~/project/page.html

# Fast mode without clustering
python scripts/keyword_analyzer.py ~/project/page.html --no-clusters
```

Output includes:
- Semantic clusters grouped by TF-IDF similarity
- Topic identification for each cluster
- Recommendations for pillar content strategy

### IndexNow Instant Indexing

Submit URLs directly to search engines for immediate indexing (critical for GEO/AEO):

```bash
# Generate IndexNow key
python scripts/indexnow_submit.py --generate-key --output ./public

# Submit single URL
python scripts/indexnow_submit.py https://example.com/new-page --key YOUR_KEY

# Batch submit from file
python scripts/indexnow_submit.py --batch urls.txt --key YOUR_KEY
```

Benefits for GEO:
- Bing index feeds AI platforms (ChatGPT, Perplexity, Claude)
- Fresh content indexed in minutes vs weeks
- 3.2x citation boost for content <30 days old

### Generate Schema Markup

```bash
# FAQ schema (highest AI citation probability)
python scripts/schema_generator.py faq \
  --question "What is longevity medicine?" \
  --answer "Longevity medicine optimizes biomarkers like LDL <70 mg/dL to reduce cardiovascular risk by 30-40%."

# Article schema with E-E-A-T signals
python scripts/schema_generator.py article \
  --title "Understanding Biomarkers" \
  --author "Dr. Sarah Johnson" \
  --credentials "MD, PhD" \
  --date "2025-01-15"
```

---

## Architecture

### Phase 1: Analysis (Complete)

Six Python scripts analyze content and generate recommendations:

| Script | Purpose | Output |
|--------|---------|--------|
| `analyze_content.py` | Extract metadata, schema, structure | JSON analysis |
| `metadata_validator.py` | Validate meta tags, OG, Twitter | Validation report |
| `keyword_analyzer.py` | Extract keywords (5 types) | Keyword list |
| `entity_extractor.py` | Extract persons, orgs, places | Entity map |
| `schema_generator.py` | Generate JSON-LD schemas | Schema files |
| `audit_report.py` | Orchestrate analysis, generate reports | JSON, MD, HTML |

### Phase 2: Implementation (Complete)

Six Python scripts implement optimizations:

| Script | Purpose | Impact |
|--------|---------|--------|
| `content_optimizer.py` | Meta descriptions, FAQ, data tables | Structure optimization |
| `platform_optimizer.py` | ChatGPT, Perplexity, Claude, Gemini | Platform-specific |
| `voice_optimizer.py` | Speakable schema, featured snippets | Voice search ready |
| `freshness_monitor.py` | Content age tracking | 3.2x citations when fresh |
| `citation_enhancer.py` | Statistics, quotation opportunities | +41% and +28% impact |
| `auto_implementer.py` | Full pipeline orchestration | Complete automation |
| `indexnow_submit.py` | Instant search engine indexing | Minutes vs weeks |

### Phase 3: Advanced Features (Planned)

- Competitive analysis (SERP top 10 comparison)
- Automated monitoring (SQLite time-series tracking)
- A/B testing framework (statistical significance)
- Analytics integration (Google Search Console, Plausible)

---

## Features

### Content Analysis

**File Types**:
- HTML (`.html`)
- Markdown (`.md`, `.mdx`)
- React/JSX (`.jsx`, `.tsx`)

**Extraction**:
- Meta tags (title, description, keywords)
- Open Graph (og:title, og:description, og:image)
- Twitter Cards (twitter:card, twitter:title)
- JSON-LD schema markup
- Content structure (headings, word count, author)

### Keyword Analysis

Five keyword types extracted:

1. **Primary**: Main topic (H1, meta title, URL, first 100 words)
2. **Semantic**: Related terms (H2/H3, body)
3. **LSI**: Co-occurring terms (natural language)
4. **Long-tail**: 3-8 word phrases (FAQ, H3)
5. **Question**: Who/what/where/when/why/how (FAQ schema)

**Keyword Clustering**: TF-IDF + cosine similarity groups keywords into semantic clusters for topical authority and pillar content strategy.

### Schema Generation

JSON-LD schemas with validation:

- **FAQPage**: Highest AI citation probability
- **Article**: E-E-A-T signals (credentials, dates)
- **HowTo**: Voice search optimized (ISO 8601 durations)
- **BreadcrumbList**: Site hierarchy
- **Organization/LocalBusiness**: Entity recognition
- **Person**: Author profiles with credentials
- **Speakable**: Voice assistant optimization

### Platform Optimization

**ChatGPT** (40-60% of LLM traffic):
- Authority and credentials (+40% citation boost)
- 1500-2500 words comprehensive coverage
- Primary source citations (PubMed, arXiv)
- Answer-first structure

**Perplexity** (Freshness-focused):
- Content updated within 30 days (3.2x citations)
- Inline citations with [1], [2] format
- H2→H3→bullets structure (40% more citations)
- Update frequency: 2-3 days (aggressive) or 90 days (minimum)

**Claude** (Accuracy-focused):
- Primary sources only (91.2% attribution accuracy)
- 5-8 citations with publisher and year
- Transparent methodology
- Acknowledged limitations

**Gemini** (Community-focused):
- Google Business Profile integration
- User reviews and testimonials
- Local citations (NAP consistency)
- Traditional authority signals

**Grokipedia** (xAI, launched Oct 2025):
- RAG-based citations (20-30% better factual consistency)
- Transparent version history and licensing
- Primary source attribution (publisher + year)
- Wikipedia-derived content requires CC-BY-SA attribution

### Voice Search

- Featured snippet optimization (30-40 words)
- Speakable schema (20-30 second segments)
- FAQ schema (natural language questions)
- Question keyword extraction

### Social Media Previews

- Open Graph tags (Facebook, LinkedIn, WhatsApp, Instagram Stories)
- Twitter Cards (summary, summary_large_image)
- Image specifications (1200×630px optimal, 1080×1920px for Instagram Stories)
- Instagram: Limited OG support (Stories only), bio link optimization, 85%+ mobile users
- iMessage optimization

---

## Output

### Report Location

```
~/Documents/SEO_Audit_[YYYY-MM-DD]_[HHMM]/
├── audit_report.json          # Structured data
├── audit_report.md            # Markdown report
├── audit_report.html          # Visual dashboard
└── generated_schemas/         # JSON-LD files
    ├── faq_schema.json
    ├── article_schema.json
    └── howto_schema.json
```

### Report Structure

1. **Executive Summary**: Overall score (0-100), top issues, top wins
2. **Metadata Analysis**: Meta tags, Open Graph, Twitter Cards, schema
3. **Content Structure**: Headings, word count, TL;DR, FAQ, author
4. **Keyword Analysis**: Primary, semantic, LSI, long-tail, question
5. **Platform Optimization**: ChatGPT, Perplexity, Claude, Gemini recommendations
6. **Action Items**: Prioritized by criticality (critical, high, medium, low)
7. **Generated Assets**: Copy-paste ready schema markup

---

## Reference Documentation

Located in `reference/` directory:

- `citation-optimization-guide.md`: AI citation strategies (+35-40% boost)
- `entity-seo-guide.md`: Knowledge Graph optimization
- `platform-strategies.md`: Platform-specific tactics
- `voice-search-guide.md`: Voice assistant optimization (29-word answers)
- `social-preview-guide.md`: Open Graph, Twitter Cards (1200×630px)
- `schema-library.md`: Complete JSON-LD reference

Templates in `templates/` directory:

- `meta-tags-template.html`: Complete meta tag set
- Schema templates: FAQ, Article, HowTo, Breadcrumb, Organization, Person

Industry examples in `examples/` directory:

- `medical-clinic/`: Healthcare optimization (15/100 → 92/100)
- `consulting-firm/`: B2B entity SEO (22/100 → 89/100)
- `saas-landing-page/`: LLMO optimization (18/100 → 94/100)

---

## Configuration

### Optimization Profiles

Located in `profiles/` directory:

**chatgpt_authority.json**:
- Target: ChatGPT citation optimization
- Focus: Authority, credentials, depth
- Word count: 1500-2500
- Expected: +40% citation probability

**perplexity_fresh.json**:
- Target: Perplexity visibility
- Focus: Freshness, inline citations
- Update: Every 2-3 days
- Expected: 3.2x citations

**multi_platform.json**:
- Target: Balanced optimization
- Platforms: ChatGPT, Perplexity, Claude, Gemini, Grokipedia
- Word count: 1200-2000
- Update: Monthly

**voice_optimized.json**:
- Target: Voice assistants
- Focus: Featured snippets, FAQ
- Answer length: 30-40 words
- Schema: Speakable, FAQPage, HowTo

---

## Performance

### Script Execution Times

- `analyze_content.py`: <1 second
- `metadata_validator.py`: <1 second
- `keyword_analyzer.py`: <2 seconds (with clustering)
- `entity_extractor.py`: <1 second
- `schema_generator.py`: <1 second
- `audit_report.py`: 3-5 seconds
- `auto_implementer.py`: 10-15 seconds (full pipeline)
- `indexnow_submit.py`: 1-3 seconds (network dependent)

All scripts: Python stdlib only, no external dependencies, offline operation (except IndexNow which requires network).

---

## Development Status

### Phase 1: Core Functionality (Complete)
- Content analysis and extraction
- Schema markup generation
- Metadata validation
- Keyword and entity extraction
- Multi-format report generation

### Phase 2: AI Optimization (Complete)
- Content rewriting for AI citation
- Platform-specific optimization (ChatGPT, Perplexity, Claude, Gemini)
- Voice search enhancement
- Freshness monitoring
- Citation enhancement (+41% statistics, +28% quotations)
- Auto-implementation pipeline

### Phase 3: Advanced Features (Planned)
- Competitive analysis (SERP top 10 comparison)
- Automated monitoring (SQLite time-series database)
- Change detection and alerting (email, webhook, Slack)
- A/B testing framework (statistical significance testing)
- Analytics integration (Google Search Console API, Plausible)
- Unified dashboard (multi-source data visualization)

### Phase 4: Ecosystem Integration (Planned)
- Seamless workflow with minimalist-website-mvp skill
- Automatic PDF report generation via generating-pdf skill
- Export to SEO tools (Ahrefs, SEMrush format)
- API mode for CI/CD pipelines
- MCP server for persistent multi-site monitoring

---

## Research Foundation

Based on 2025 analysis:
- 41M AI search results analyzed
- 680M citations across platforms
- 527% AI traffic growth (Jan-May 2025)

Key findings implemented:
- Statistics Addition: +41% improvement (Princeton/Georgia Tech)
- Quotation Addition: +28% improvement
- Freshness (<30 days): 3.2x citations (Ahrefs study)
- Author credentials: +40% citation probability
- H2→H3→bullets structure: 40% more citations
- Featured snippets: 40.7% of voice answers

Platform citation patterns:
- ChatGPT: Wikipedia (1.3M citations), G2 (196K), Forbes (181K)
- Perplexity: Update frequency critical (3.2x citations when fresh)
- Claude: 91.2% correct source attribution (Q2 2025)
- AI Overviews: 13.14% of queries (March 2025), up from 6.49% (January 2025)

---

## Contributing

This project follows semantic versioning (major.minor.patch).

Report issues: [GitHub Issues](https://github.com/199-biotechnologies/claude-skill-seo-geo-optimizer/issues)

---

## License

MIT License - See LICENSE file for complete terms.

Copyright (c) 2025 Boris Djordjevic, 199 Biotechnologies
