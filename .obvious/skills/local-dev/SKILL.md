---
name: local-dev
description: Bring up and verify the HVACapp static single-page site locally.
version: 1.0.0
triggers:
  - local dev
  - serve site
  - static site
  - HVACapp
created: 2026-06-18
---

## Purpose

Use this skill to run and verify local development for `autopermit/HVACapp`. The repository is a tiny static single-page site with no package manager, dependency install, build system, lint command, typecheck command, or test command discovered during setup.

## Prerequisites

- Python 3.13.13 — verified with `python3 --version`.
- `curl` — verified at `/usr/bin/curl`.
- Optional screenshot tooling for evidence capture: `shot-scraper` 1.9.1 with Playwright Chromium. During setup this required installing browser shared libraries with `sudo apt-get install -y libnspr4 libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libpangocairo-1.0-0 libasound2`.

## Install Commands

No repository dependency install is required. The site is served directly from checked-in static files.

For screenshot evidence only, setup used:

```bash
pip3 install shot-scraper
shot-scraper install
```

## Environment Setup

No environment variables, secrets, databases, queues, or external local services were discovered or required.

## Start Commands

Run from the repository root:

```bash
python3 -m http.server 8765 --directory /home/user/work/HVACapp
```

Verified URL: `http://localhost:8765/`

When running in a long-lived sandbox session, keep the server in tmux:

```bash
tmux new-session -d -s hvac-serve "python3 -m http.server 8765 --directory /home/user/work/HVACapp"
```

## Primary Flow

1. Start the static HTTP server on port 8765.
2. Visit `http://localhost:8765/` in a browser.
3. Confirm the HVACapp landing page renders.
4. Scroll through the landing page to verify main content remains visible.
5. Scroll to the signup area and confirm the page reaches the early-access section.
6. Verify static image assets respond over HTTP:
   - `http://localhost:8765/b5-favicon.png`
   - `http://localhost:8765/hvacapp_preview.png`

Evidence captured during install:

- `.obvious-install/screenshots/landing/01-landing.png` — landing page loaded — artifact/file: `fl_PJCXvN4m`
- `.obvious-install/screenshots/landing/03-scrolled.png` — scrolled page state — artifact/file: `fl_0OgZ8U4v`
- `.obvious-install/screenshots/landing/04-signup.png` — signup area state — artifact/file: `fl_6QOnZ3g1`

## Verification Commands

No lint, typecheck, or test commands were discovered.

Use these smoke checks instead:

```bash
curl -s --max-time 5 -o /dev/null -w "HTTP %{http_code}" http://localhost:8765/
curl -s --max-time 5 http://localhost:8765/ | grep -i "<title>"
curl -s --max-time 5 -o /dev/null -w "HTTP %{http_code}" http://localhost:8765/b5-favicon.png
curl -s --max-time 5 -o /dev/null -w "HTTP %{http_code}" http://localhost:8765/hvacapp_preview.png
```

Expected result: each HTTP check returns `HTTP 200`, and the title check prints the HVACapp title tags.

## Sandbox Snapshot

Snapshot ID: `2nm8r7afht4wpd6pqg7x:default`

Captured at: `2026-06-18T19:38:51.998Z`

## Known Blockers

- No application-level lint/typecheck/test tooling exists yet. Use HTTP smoke checks and browser screenshots for local validation until the repo adds tooling.
- Do not stage `.obvious-install/`; it contains local installer evidence only.

