#!/usr/bin/env python3
"""
build.py — Tiny template engine for the MedMe website mockup.

Reads source templates from ./src/, expands partial includes
from ./partials/, and writes finished HTML to the project root
(overwriting mockup-*-homepage.html, etc.).

USAGE
-----
    python3 build.py            # build everything in src/
    python3 build.py --check    # build to stdout (no write), exit 1 if anything changed

TEMPLATE SYNTAX
---------------
    {{> partials/nav-us }}      Inline the contents of partials/nav-us.html
    {{ page.title }}            Substitute a variable from frontmatter
    {{# ignored comment }}      Removed entirely

Frontmatter (optional, at top of template):

    ---
    region: us
    page.title: MedMe — United States
    ---

NOTES
-----
* Partials may include other partials. Cycles raise an error.
* This file uses only the Python stdlib — no `pip install` needed.
* Output is byte-identical to whatever the partial files contain, so
  a partial-only edit produces a clean diff in the rendered HTML.
"""

from __future__ import annotations
import hashlib
import re
import sys
from pathlib import Path

INCLUDE_RE   = re.compile(r"\{\{>\s*([^\s}]+)\s*\}\}")
VAR_RE       = re.compile(r"\{\{\s*([a-zA-Z_][\w.]*)\s*\}\}")
COMMENT_RE   = re.compile(r"\{\{#[^}]*\}\}")
# Auto-rewrite stale ?v=N query strings on asset references so cache
# busting no longer drifts across pages. The build picks a fresh key
# (an 8-char content hash of the referenced file) and stamps every
# matching <link>/<script> reference in the rendered output.
ASSET_VER_RE = re.compile(r'(/assets/([^"\?]+))\?v=[^"\s>]+')
MAX_INCLUDE_DEPTH = 50


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Pull a YAML-ish frontmatter block off the top, if present."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    body  = text[end + 5:]
    raw   = text[4:end]
    data: dict = {}
    for line in raw.strip().splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            data[key.strip()] = val.strip()
    return data, body


def resolve_var(name: str, ctx: dict) -> str:
    """Look up a dotted path against ctx. Missing keys return ''."""
    if name in ctx:           # exact match wins (supports keys with dots)
        return str(ctx[name])
    parts = name.split(".")
    val: object = ctx
    for p in parts:
        if isinstance(val, dict):
            val = val.get(p, "")
        else:
            return ""
    return str(val)


def expand_includes(text: str, partials_dir: Path) -> str:
    """Iteratively replace {{> partials/x }} with the contents of x.html."""
    for _ in range(MAX_INCLUDE_DEPTH):
        if not INCLUDE_RE.search(text):
            return text

        def _sub(m: re.Match) -> str:
            name = m.group(1).strip()
            # Tolerate both `partials/nav-us` and just `nav-us`
            short = name.removeprefix("partials/")
            path = partials_dir / f"{short}.html"
            if not path.exists():
                raise FileNotFoundError(f"Partial not found: {path}")
            # Strip any trailing newlines so editor-added \n doesn't
            # propagate as an extra blank line in the rendered HTML
            return path.read_text(encoding="utf-8").rstrip("\n")

        text = INCLUDE_RE.sub(_sub, text)
    raise RuntimeError(
        "Include depth exceeded — check for a circular partial reference"
    )


def asset_hash(path: Path) -> str:
    """Return a short content hash for an asset file. Used to replace
    the manual `?v=N` cache-busting query strings with a key that
    changes whenever the underlying file changes."""
    h = hashlib.sha256(path.read_bytes()).hexdigest()
    return h[:8]


def rewrite_asset_versions(body: str, assets_dir: Path, cache: dict[str, str]) -> str:
    """Replace every `/assets/foo.css?v=N` (or ?v=anything) reference
    with a content-hash version. Missing files are left untouched so a
    typo doesn't silently strip the version."""
    def _sub(m: re.Match) -> str:
        full_path = m.group(1)          # e.g. /assets/brand.css
        rel       = m.group(2)          # e.g. brand.css
        local     = assets_dir / rel
        if not local.exists():
            return m.group(0)           # leave reference untouched
        if rel not in cache:
            cache[rel] = asset_hash(local)
        return f"{full_path}?v={cache[rel]}"
    return ASSET_VER_RE.sub(_sub, body)


def build_one(template: Path, partials_dir: Path, assets_dir: Path, hash_cache: dict[str, str]) -> str:
    raw = template.read_text(encoding="utf-8")
    vars_, body = parse_frontmatter(raw)
    body = COMMENT_RE.sub("", body)
    body = expand_includes(body, partials_dir)
    body = VAR_RE.sub(lambda m: resolve_var(m.group(1).strip(), vars_), body)
    body = rewrite_asset_versions(body, assets_dir, hash_cache)
    return body


def main(argv: list[str]) -> int:
    root         = Path(__file__).parent.resolve()
    src_dir      = root / "src"
    partials_dir = root / "partials"
    assets_dir   = root / "assets"
    check_only   = "--check" in argv
    hash_cache: dict[str, str] = {}     # asset rel-path -> 8-char content hash

    if not src_dir.exists():
        print(f"error: src/ not found at {src_dir}", file=sys.stderr)
        return 1
    if not partials_dir.exists():
        print(f"error: partials/ not found at {partials_dir}", file=sys.stderr)
        return 1

    templates = sorted(src_dir.rglob("*.html"))   # recursive — supports nested directories
    if not templates:
        print("error: no *.html templates in src/", file=sys.stderr)
        return 1

    print(f"Building {len(templates)} template(s)…")
    any_changed = False
    for tpl in templates:
        rel = tpl.relative_to(src_dir)
        # Output non-index pages as <name>/index.html so clean URLs work
        # under a static server (e.g. python -m http.server). Examples:
        #   src/us/about.html         -> us/about/index.html        (URL: /us/about)
        #   src/us/index.html         -> us/index.html              (URL: /us)
        #   src/us/platform/ehr.html  -> us/platform/ehr/index.html (URL: /us/platform/ehr)
        if rel.name == "index.html":
            output_path = root / rel
        else:
            output_path = root / rel.parent / rel.stem / "index.html"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            new = build_one(tpl, partials_dir, assets_dir, hash_cache)
        except Exception as e:
            print(f"  ✗ {tpl.name}: {e}", file=sys.stderr)
            return 1

        if check_only:
            old = output_path.read_text(encoding="utf-8") if output_path.exists() else ""
            if old != new:
                any_changed = True
                print(f"  Δ  {rel} (would change)")
            else:
                print(f"  =  {rel}")
        else:
            output_path.write_text(new, encoding="utf-8")
            print(f"  ✓  {rel}")

    if check_only and any_changed:
        return 1
    print("done.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
