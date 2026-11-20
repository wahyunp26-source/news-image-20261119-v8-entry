# news-image-20261119 v8 — STATUS (facts only)

## Competition
- news-image-20261119, $250. Deadline 21 Nov 2026 07:00 WIB (2026-11-21T00:00:00Z).
- Quota (from `makefun status`, 20 Nov ~04:24 UTC): entries made 2, can submit
  now yes, 1 slot left. v8 would be submission 3/3 — the LAST slot.
- NOT submitted. NOT committed. Parent bundles + submits after Wahyu approves
  the preview. Submit target ~05:50 WIB 21 Nov if approved.

## Method (new — v3–v7 vector approach abandoned)
- Illustrations = 13 generated raster images (rich cartoon scenes, gradients,
  shading, no text), center-cropped to exact display size with PIL.
- Typography = real Liberation Sans (Bold/Regular/Italic) pre-rendered to PNG
  at build time with PIL (2x supersample, LANCZOS downscale). No hand-drawn
  glyphs anywhere.
- Entry main.py = pure stdlib: own PNG decoder (types 2/6, 8-bit, filters
  0–4) + alpha compositing + own PNG encoder. Reads assets/manifest.json.
- Build tool (not part of entry): ~/workspace/makefun/news-image-20261119-v8-tools/render_assets.py
  Raw illustrations: .../raw/*.webp. Map bitmap: .../map64.json (extracted
  from v7 data).

## Files
- Repo dir: `~/workspace/makefun/news-image-20261119-v8/`
  - `main.py` — stdlib only (json, os, struct, zlib). ~200 lines.
  - `assets/` — 39 PNGs + manifest.json (944K total).
  - `LICENSE` — MIT (SPDX-License-Identifier: MIT).
  - `.makefun/freshness.json` — drand-quicknet, round 34113101 (copied from v7).
  - `entry.png` — output, 1024x1024, 820,894 bytes.
- Preview: `~/workspace/makefun/news-image-20261119-v8-preview.png`
  sha256 `a56424b0431910c0b4552aa2d10d444db2e35dae223ca9fba1aab432756b774a` (revised 20 Nov 11:40 WIB — map-gap edit, see below; parent re-ran main.py, byte-identical).

## Content
- Same 46-story set + numbers as v6/v7 (heroes: Shenzhen summit, Crimea
  bridge, Voyager 1; 10 small cards 4–13; ALSO 14–46). Regions: ASIA 9,
  EUROPE 10, AMERICAS 9, AFRICA 4, MIDDLE EAST 3, OCEANIA 7, GLOBAL 4.
- Numbers strip: '1', '$81.3bn', '51–48', '109–0', '589m', '4.9%' — all
  verified correct on crops.
- Layout: v7 geometry kept (frame, header + calendar box, region bar, numbers
  strip, hours strip, 3 heroes, 10 cards in 2 rows, map + ALSO + VERDICT,
  DATE CHECK, footer). Masthead Liberation Sans Bold auto-fit to 64px
  (868px wide).

## Gates
- Stdlib only: yes (json, os, struct, zlib; no PIL/numpy/requests/network).
- Determinism: 2x system `python3 -P -s main.py` + 1x clean venv (PIL import
  fails there) — all three byte-identical, sha256 `ced34e76…`.
  Runtime ~1.9s.
- Decoder check: own PNG decoder round-tripped all 39 assets byte-identical
  vs PIL decode.
- Output: 1024x1024, 820,894 bytes (<=1 MiB).
- Visual check: full size + 256px thumbnail + 3 crops viewed. Masthead,
  numbers, hero titles, card titles/decks, ALSO list (all 33 fit, none
  truncated), map + pins, verdict box all read correctly. No clipping found.
- `makefun check` (kit `~/workspace/makefun/news-image-20261119-kit/`,
  --worktree, no transcripts, 20 Nov ~04:25 UTC): 4 passed
  (competition_open, snapshot, license_osi, entrypoint), 1 failed
  (transcripts_present — expected, no transcripts; parent bundles),
  14 skipped, 5 checked at submission. Same counts as v6/v7.
- No git commands run in the repo; nothing committed.

## Honest weaknesses left
- Summit hero flags on the table are France/Japan/Germany, not US/China/
  Russia — tiny at display size (~10px), not legible as wrong, but not exact.
- Dotted map still dots: Asia/Europe nearly touch at top (same as v7).
- ALSO list 9px — legible full-size, barely readable at 256px thumbnail
  (same as the top-3 references).
- Hero/card images are AI-generated scenes, not photos of the real events.

## Submit attempt — 20 Nov 11:29–11:33 WIB — BLOCKED (not rejected)
- Wahyu 11:29: "submit sekarang coba". Quota re-checked OK (2/3, 1 slot left). Kit re-downloaded, bundle_sha256 1c4dd40e… identical to local (fresh).
- Repo created + pushed: https://github.com/wahyunp26-source/news-image-20261119-v8-entry, commit 3a2bc16fb835057b1b73c1c312842b5acb8e60f3, verified via GitHub API (homepage make.fun bounty page, topics makefun + ai-agents + bounties, contents complete incl. .makefun/owner.json).
- Bundle materials saved in ~/workspace/makefun/news-image-20261119-v8-submit/: v8-system-prompt.txt (3.434 byte, from builder session), v8-usage.jsonl (1 row), v8-prompt.txt ("Gas v8 cara baru").
- BLOCKER: the git init/commit/push exec result was flagged by a runtime execution-risk check; the submitter stopped before bundle/check/submit and asked for Wahyu's plain-words OK to continue processing the v8 repo. NO submission id, NO claim code, NO crons created. Quota still 2/3.
- Resume (after Wahyu says continue): bundle dry-run from the kit: `node cli/makefun.mjs bundle --repo ~/workspace/makefun/news-image-20261119-v8 --out ~/workspace/makefun/news-image-20261119-v8-submit/v8-bundle.tar.gz --session /home/hatch/agents/agent-ca2872d5-8a32-4644-aaab-ba67049c7f0a/sessions/ca2872d5-8a32-4644-aaab-ba67049c7f0a.jsonl --muse-usage ~/workspace/makefun/news-image-20261119-v8-submit/v8-usage.jsonl --system-prompt ~/workspace/makefun/news-image-20261119-v8-submit/v8-system-prompt.txt --prompt-file ~/workspace/makefun/news-image-20261119-v8-submit/v8-prompt.txt --prompt-origin other --prompt-via "coordinator subagent spawn" --harness muse-app --harness-version 1.3 --model ipnext/avocado-5.17-v2 --provider meta --effort default --mcp none --no-discover --dry-run`, then real bundle, `makefun check`, submit ONCE with --bundle + --repo-url (no harness/provider/effort/prompt flags). If dry-run shows 0 usage rows attached, re-run the usage SQL first, do not submit. **Wahyu 11:34 WIB: 'Lanjut, proses aja' ✅ — resume submitter di-spawn (bundle dry-run → bundle → check → submit 1x → cron cek +10m/+30m).**
