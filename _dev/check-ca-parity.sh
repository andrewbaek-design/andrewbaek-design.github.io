#!/usr/bin/env bash
# check-ca-parity.sh — Report structural drift between src/us/ and src/ca/.
#
# What this checks:
#  - Files that exist in src/us/ but not in src/ca/ (and vice versa)
#  - Page-count drift between the two regions
#  - Last-modified gap: which side has been touched more recently
#
# Exit code: 1 if any drift is detected, 0 if structurally in sync.
#
# Usage:
#   ./_dev/check-ca-parity.sh           # report only
#   ./_dev/check-ca-parity.sh --strict  # exit 1 on any drift (for CI)

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
US_DIR="$ROOT/src/us"
CA_DIR="$ROOT/src/ca"

STRICT=0
if [[ "${1:-}" == "--strict" ]]; then
  STRICT=1
fi

red()    { printf "\033[31m%s\033[0m\n" "$*"; }
green()  { printf "\033[32m%s\033[0m\n" "$*"; }
yellow() { printf "\033[33m%s\033[0m\n" "$*"; }
bold()   { printf "\033[1m%s\033[0m\n" "$*"; }

# ---- 1. File-presence diff ---------------------------------------------
bold "== Page presence =="

# Get all .html files relative to each region root, sorted.
us_files=$(cd "$US_DIR" && find . -name "*.html" -type f | sed 's|^\./||' | sort)
ca_files=$(cd "$CA_DIR" && find . -name "*.html" -type f | sed 's|^\./||' | sort)

# Files only in US.
only_us=$(comm -23 <(echo "$us_files") <(echo "$ca_files"))
only_ca=$(comm -13 <(echo "$us_files") <(echo "$ca_files"))

drift=0
if [[ -n "$only_us" ]]; then
  yellow "US-only pages (no CA equivalent):"
  while read -r f; do echo "  src/us/$f"; done <<< "$only_us"
  drift=1
fi

if [[ -n "$only_ca" ]]; then
  yellow "CA-only pages (no US equivalent):"
  while read -r f; do echo "  src/ca/$f"; done <<< "$only_ca"
  drift=1
fi

if [[ "$drift" -eq 0 ]]; then
  green "Page sets match (US: $(echo "$us_files" | wc -l | xargs) pages, CA: $(echo "$ca_files" | wc -l | xargs) pages)."
fi

# ---- 2. Recency gap ----------------------------------------------------
echo
bold "== Last-modified gap =="

us_latest=$(find "$US_DIR" -name "*.html" -type f -exec stat -f "%m %N" {} + 2>/dev/null | sort -rn | head -1 || echo "")
ca_latest=$(find "$CA_DIR" -name "*.html" -type f -exec stat -f "%m %N" {} + 2>/dev/null | sort -rn | head -1 || echo "")

if [[ -n "$us_latest" && -n "$ca_latest" ]]; then
  us_ts=$(echo "$us_latest" | cut -d' ' -f1)
  ca_ts=$(echo "$ca_latest" | cut -d' ' -f1)
  us_path=$(echo "$us_latest" | cut -d' ' -f2-)
  ca_path=$(echo "$ca_latest" | cut -d' ' -f2-)
  echo "US most-recent edit: $(date -r "$us_ts" "+%Y-%m-%d %H:%M") -> ${us_path#$ROOT/}"
  echo "CA most-recent edit: $(date -r "$ca_ts" "+%Y-%m-%d %H:%M") -> ${ca_path#$ROOT/}"

  gap=$(( us_ts - ca_ts ))
  if [[ "$gap" -lt 0 ]]; then gap=$(( -gap )); fi
  days=$(( gap / 86400 ))
  if [[ "$days" -gt 14 ]]; then
    yellow "Gap is $days days. CA may be falling behind US (or vice versa)."
    drift=1
  else
    green "Gap is $days days. Within tolerance."
  fi
fi

# ---- 3. Inline-CSS size comparison ------------------------------------
echo
bold "== Inline-CSS size comparison =="

# Match pages that exist in both, compare inline <style> line counts.
common=$(comm -12 <(echo "$us_files") <(echo "$ca_files"))
big_drift=0
while read -r rel; do
  [[ -z "$rel" ]] && continue
  us_file="$US_DIR/$rel"
  ca_file="$CA_DIR/$rel"
  us_lines=$(awk '/<style>/,/<\/style>/' "$us_file" 2>/dev/null | wc -l | xargs)
  ca_lines=$(awk '/<style>/,/<\/style>/' "$ca_file" 2>/dev/null | wc -l | xargs)
  if [[ "$us_lines" -gt 0 || "$ca_lines" -gt 0 ]]; then
    diff_lines=$(( us_lines - ca_lines ))
    if [[ "$diff_lines" -lt 0 ]]; then diff_lines=$(( -diff_lines )); fi
    # Flag if the diff exceeds 50 lines OR is >2x larger
    if [[ "$diff_lines" -gt 50 ]]; then
      printf "  %-35s  US=%4s lines, CA=%4s lines  (gap: %s lines)\n" "$rel" "$us_lines" "$ca_lines" "$diff_lines"
      big_drift=1
    fi
  fi
done <<< "$common"

if [[ "$big_drift" -eq 0 ]]; then
  green "No significant inline-CSS-size drift between matching pages."
else
  yellow "Pages above show significant inline-CSS drift. CA may need a port."
  drift=1
fi

# ---- Exit code --------------------------------------------------------
echo
if [[ "$drift" -eq 1 ]]; then
  if [[ "$STRICT" -eq 1 ]]; then
    red "Drift detected. Exiting with code 1 (strict mode)."
    exit 1
  else
    yellow "Drift detected. Run with --strict for CI."
    exit 0
  fi
else
  green "US and CA are in structural sync."
  exit 0
fi
