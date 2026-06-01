#!/usr/bin/env python3
"""Render self-contained interactive review HTML for GEO briefs and drafts.

Three modes (issue #1, battle-tested in SEA-CICSIC):
  - brief : fill-form HTML for a 04-content-brief with REQUIRED-FILL slots
  - draft : review HTML for a 05-production publish-ready draft
  - index : entry page listing every brief/draft in a client folder

The interaction logic (localStorage auto-save, JSON export, progress, the
approve/comment state machine) lives in templates/review.html and is FIXED
so it is always correct. This script only parses the Markdown + meta into a
structured payload and injects it. The visual layer is the template's CSS,
which is where the vendored `frontend-design` skill applies (see SKILL.md).

Pure standard library — no third-party deps, mirrors the seo-geo-optimizer
script convention so CI's py_compile pass covers it.
"""
import argparse
import json
import os
import re
import sys

TEMPLATE = os.path.join(os.path.dirname(__file__), "..", "templates", "review.html")

# ---------------------------------------------------------------------------
# Minimal Markdown -> HTML (stdlib only). Covers what briefs/drafts emit:
# headings, bold/italic/code, links, bullet + ordered lists, blockquotes,
# pipe tables, fenced code, paragraphs. Not a general Markdown engine.
# ---------------------------------------------------------------------------
def _esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _inline(s):
    s = _esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" rel="noopener" target="_blank">\1</a>', s)
    return s


def _table(rows):
    # rows: list of raw "| a | b |" lines; row[1] is the --- separator
    def cells(line):
        return [c.strip() for c in line.strip().strip("|").split("|")]
    head = cells(rows[0])
    body = [cells(r) for r in rows[2:]]
    out = ['<table><thead><tr>']
    out += [f"<th>{_inline(c)}</th>" for c in head]
    out.append("</tr></thead><tbody>")
    for r in body:
        out.append("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in r) + "</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def md_to_html(text):
    lines = text.split("\n")
    out, i, n = [], 0, len(lines)
    while i < n:
        line = lines[i]
        if line.strip().startswith("```"):
            buf, i = [], i + 1
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i]); i += 1
            out.append("<pre><code>" + _esc("\n".join(buf)) + "</code></pre>")
            i += 1; continue
        m = re.match(r"^(#{1,4})\s+(.*)", line)
        if m:
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{_inline(m.group(2))}</h{lvl}>"); i += 1; continue
        if line.strip().startswith("|") and i + 1 < n and re.match(r"^\s*\|?[\s:|-]+\|?\s*$", lines[i + 1]):
            tbl = []
            while i < n and lines[i].strip().startswith("|"):
                tbl.append(lines[i]); i += 1
            out.append(_table(tbl)); continue
        if re.match(r"^\s*[-*]\s+", line):
            items = []
            while i < n and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(_inline(re.sub(r"^\s*[-*]\s+", "", lines[i]))); i += 1
            out.append("<ul>" + "".join(f"<li>{it}</li>" for it in items) + "</ul>"); continue
        if re.match(r"^\s*\d+\.\s+", line):
            items = []
            while i < n and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(_inline(re.sub(r"^\s*\d+\.\s+", "", lines[i]))); i += 1
            out.append("<ol>" + "".join(f"<li>{it}</li>" for it in items) + "</ol>"); continue
        if line.strip().startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i])); i += 1
            out.append(f"<blockquote>{_inline(' '.join(buf))}</blockquote>"); continue
        if line.strip() == "":
            i += 1; continue
        para = [line]; i += 1
        while i < n and lines[i].strip() and not re.match(r"^(#{1,4}\s|[-*]\s|\d+\.\s|>|\||```)", lines[i].strip()):
            para.append(lines[i]); i += 1
        out.append(f"<p>{_inline(' '.join(para))}</p>")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Brief parsing: split into ordered sections; REQUIRED-FILL blocks become
# slot sections (yellow textareas), everything else becomes prose (green).
# ---------------------------------------------------------------------------
SLOT_HEADER = re.compile(r"REQUIRED-FILL\s*[·|]\s*([A-Za-z0-9_-]+)\s*[·|]\s*([A-Za-z0-9_-]+)")
FIELD = {
    "what": re.compile(r"What goes here\**:?\s*(.*)", re.I),
    "why": re.compile(r"Why it matters[^:]*:?\s*(.*)", re.I),
    "bad": re.compile(r"Bad fill[^:]*:?\s*(.*)", re.I),
    "good": re.compile(r"Good fill[^:]*:?\s*(.*)", re.I),
}


def parse_brief(md, slot_ids):
    """Return ordered list of {type: prose|slot, ...}. Splits the brief on
    REQUIRED-FILL blockquote blocks; the slot list from meta is authoritative
    for which ids exist and their fill state."""
    sections, buf, cur_heading = [], [], None

    def flush_prose():
        nonlocal buf
        body = "\n".join(buf).strip()
        if body:
            sid = re.sub(r"[^a-z0-9]+", "-", (cur_heading or "section").lower()).strip("-")
            sections.append({
                "type": "prose",
                "id": "filled-" + (sid or "section"),
                "heading": cur_heading or "",
                "html": md_to_html(body),
            })
        buf = []

    lines = md.split("\n")
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        m = SLOT_HEADER.search(line)
        if m and line.strip().startswith(">"):
            flush_prose()
            block = [line]
            i += 1
            while i < n and lines[i].strip().startswith(">"):
                block.append(lines[i]); i += 1
            blocktext = "\n".join(re.sub(r"^\s*>\s?", "", b) for b in block)
            slot = {"type": "slot", "id": m.group(1), "asset_type": m.group(2),
                    "what": "", "why": "", "bad": "", "good": ""}
            for key, rx in FIELD.items():
                fm = rx.search(blocktext)
                if fm:
                    slot[key] = fm.group(1).strip().rstrip("*").strip()
            sections.append(slot)
            continue
        hm = re.match(r"^(#{1,4})\s+(.*)", line)
        if hm:
            flush_prose()
            cur_heading = hm.group(2).strip()
        else:
            buf.append(line)
        i += 1
    flush_prose()

    # Ensure every meta slot is represented even if md parsing missed it.
    seen = {s["id"] for s in sections if s["type"] == "slot"}
    for sid in slot_ids:
        if sid not in seen:
            sections.append({"type": "slot", "id": sid, "asset_type": "",
                             "what": "(slot description not found in brief — fill with your content)",
                             "why": "", "bad": "", "good": ""})
    return sections


def parse_draft(md):
    """Split a publish-ready draft into H2-anchored prose sections so each
    gets its own section-level comment toggle."""
    sections = []
    parts = re.split(r"(?m)^(##\s+.*)$", md)
    # parts: [preamble, '## H', body, '## H', body, ...]
    if parts[0].strip():
        sections.append({"type": "prose", "id": "intro", "heading": "",
                         "html": md_to_html(parts[0])})
    for j in range(1, len(parts), 2):
        heading = re.sub(r"^##\s+", "", parts[j]).strip()
        body = parts[j + 1] if j + 1 < len(parts) else ""
        sid = "sec-" + re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")
        sections.append({"type": "prose", "id": sid, "heading": heading,
                         "html": md_to_html(parts[j] + "\n" + body)})
    return sections


def inject(payload, title):
    with open(TEMPLATE, encoding="utf-8") as f:
        tpl = f.read()
    blob = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    return (tpl.replace("__TITLE__", _esc(title))
               .replace("__PAYLOAD__", blob))


def main():
    ap = argparse.ArgumentParser(description="Render interactive GEO review HTML.")
    ap.add_argument("--mode", required=True, choices=["brief", "draft", "index"])
    ap.add_argument("--md", help="brief/draft markdown path")
    ap.add_argument("--meta", help="brief/draft .meta.json path")
    ap.add_argument("--brand", help="brand_context.json (optional, for client name/brand color)")
    ap.add_argument("--client-dir", help="index mode: clients/<slug> dir to scan")
    ap.add_argument("--out", required=True, help="output .html path")
    args = ap.parse_args()

    brand = json.load(open(args.brand, encoding="utf-8")) if args.brand and os.path.exists(args.brand) else {}
    client_name = brand.get("brand_name") or brand.get("company_name") or ""
    brand_color = (brand.get("brand", {}) or {}).get("primary_color") or brand.get("brand_color") or ""

    if args.mode in ("brief", "draft"):
        meta = json.load(open(args.meta, encoding="utf-8")) if args.meta and os.path.exists(args.meta) else {}
        md = open(args.md, encoding="utf-8").read()
        if args.mode == "brief":
            slot_ids = [s["id"] for s in meta.get("slots", [])]
            sections = parse_brief(md, slot_ids)
            filled = {s["id"]: s.get("filled", False) for s in meta.get("slots", [])}
            for s in sections:
                if s["type"] == "slot":
                    s["filled"] = filled.get(s["id"], False)
        else:
            sections = parse_draft(md)
        title = meta.get("priority_id") or os.path.splitext(os.path.basename(args.md))[0]
        payload = {
            "mode": args.mode,
            "brief_id": meta.get("priority_id") or title,
            "client_name": client_name,
            "brand_color": brand_color,
            "meta": {
                "format": meta.get("format", ""),
                "status": meta.get("status", ""),
                "generated_at": meta.get("generated_at", ""),
                "word_count": meta.get("word_count", 0),
            },
            "sections": sections,
        }
    else:  # index
        cdir = args.client_dir
        items = []
        for sub, kind in (("briefs", "brief"), ("drafts", "draft")):
            d = os.path.join(cdir, sub)
            if not os.path.isdir(d):
                continue
            for fn in sorted(os.listdir(d)):
                if not fn.endswith(".meta.json"):
                    continue
                meta = json.load(open(os.path.join(d, fn), encoding="utf-8"))
                bid = meta.get("priority_id") or fn[:-len(".meta.json")]
                slots = meta.get("slots", [])
                items.append({
                    "id": bid,
                    "kind": kind,
                    "format": meta.get("format", ""),
                    "status": meta.get("status", ""),
                    "word_count": meta.get("word_count", 0),
                    "slot_count": len(slots),
                    "filled_count": sum(1 for s in slots if s.get("filled")),
                    "href": f"{sub}/{bid}.html",
                })
        payload = {"mode": "index", "client_name": client_name,
                   "brand_color": brand_color, "items": items}
        title = (client_name + " — " if client_name else "") + "GEO review index"

    html = inject(payload, title)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"wrote {args.out} ({len(html)} bytes, mode={args.mode})")


if __name__ == "__main__":
    main()
