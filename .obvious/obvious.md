# Obvious Agent Guidance

> Autobuild setup worker version: 1.2.0
> Installed for `autopermit/HVACapp` on 2026-06-18.

## Codebase Map

Tiny-repo case: codebase map is inlined here; no separate `.obvious/codebase-map.md` is generated.

| Directory | Purpose |
|---|---|
| `.` | Static single-page HVACapp marketing and early-access signup site. Primary source is the root HTML document with embedded CSS and JavaScript plus image assets. |

## Repo Guidance

- This repository is a static single-page site with no package manager, lockfile, build system, application server, or dependency install step.
- Keep changes focused: application behavior and presentation currently live in one root HTML document with embedded styles and scripts.
- Serve the repository over HTTP for validation; do not rely on opening the HTML file directly because asset paths and browser behavior should match hosted usage.
- Do not invent npm, Bun, lint, typecheck, or test commands unless the repository later adds those tools.
- Scratch installer artifacts belong under `.obvious-install/` and must never be staged in PRs.

## Local Verification

<!-- local-verification-summary:v1 -->
no commands discovered
<!-- /local-verification-summary -->

### Verified local-dev commands

1. `python3 -m http.server 8765 --directory /home/user/work/HVACapp` — verified static HTTP server startup.
2. `curl -s --max-time 5 -o /dev/null -w "HTTP %{http_code}" http://localhost:8765/` — verified page responds with `HTTP 200`.
3. `curl -s --max-time 5 http://localhost:8765/ | grep -i "<title>"` — verified HVACapp titles are present in served HTML.
4. `curl -s --max-time 5 -o /dev/null -w "HTTP %{http_code}" http://localhost:8765/b5-favicon.png` — verified favicon asset responds with `HTTP 200`.
5. `curl -s --max-time 5 -o /dev/null -w "HTTP %{http_code}" http://localhost:8765/hvacapp_preview.png` — verified preview image asset responds with `HTTP 200`.

### Scoped Workflow

No scoped lint, typecheck, or test workflow exists because the repository has no discovered tooling.

## Sandbox Snapshot

- **Snapshot ID:** `2nm8r7afht4wpd6pqg7x:default`
- **Captured at:** `2026-06-18T19:38:51.998Z`
- **Captured after:** local dev was verified healthy and before any `.obvious/` files were written.

## Bibliography

- **Status:** bibliography_scanned
- **Nodes upserted:** 2
- **Slugs touched:** `hvacapp-early-access-signup`, `hvacapp-landing-site`
- **Failures:** none

## Security Scan

> **Note:** security_scan_not_triggered — the trigger_security_onboarding tool was unavailable in this worker toolset. Trigger manually using the trigger_security_onboarding tool with commit SHA `817ce3edc441ea74f6a478ed7f240a81de8821b2`.

