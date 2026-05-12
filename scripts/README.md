# Scraping Workspace

This directory is for local, reproducible data extraction work.

## Scrapling checkout

The Scrapling source repository is cloned locally at:

```text
scripts/scrapling-repo/
```

That checkout is intentionally ignored by git so this repository does not vendor
Scrapling's source history.

## Install locally

From the repository root:

```bash
python3 -m venv scripts/.venv
scripts/.venv/bin/python -m pip install --upgrade pip
scripts/.venv/bin/python -m pip install -r scripts/requirements.txt
scripts/.venv/bin/scrapling install
```

Use `scrapling install` only when browser-based fetchers are needed. For static
state fee pages, start with `Fetcher` before using browser automation.

Example inspection command:

```bash
scripts/.venv/bin/python scripts/extract_official_page.py \
  "https://official-state-url.example.gov/fees" \
  --selector "body"
```

## Data protocol

Only official state government sources may be used. Any extracted value must be
verified against an official fee schedule or corporation division page before
updating `states.json`.

## URL audit first

Before scraping missing sidebar fields, audit the URL roles in the generated
state JSON files. The initial files were derived from fee data, so some
`secretaryOfState.website` and `businessEntitySearch.url` values may currently
point at fee schedules instead of the agency homepage or entity search page.

Run a read-only URL audit:

```bash
scripts/.venv/bin/python scripts/audit_state_urls.py --insecure
```

The script writes a report to:

```text
entitysearch-state-data/audits/url-audit-YYYY-MM-DD.json
```

Useful options:

```bash
# Classify from URL text only, without network requests
scripts/.venv/bin/python scripts/audit_state_urls.py --no-fetch

# Limit review to one or more states
scripts/.venv/bin/python scripts/audit_state_urls.py --state AL --state AK --insecure
```

Review the generated `proposedRoles` before changing state JSON files:

- `secretaryOfState.website` should be the agency or division homepage.
- `businessEntitySearch.url` should be the live business/entity search page.
- Fee schedules, annual report pages, PDFs, and tax pages should remain in
  `sources[]` with `lastAccessed`.

Apply the curated URL role corrections:

```bash
scripts/.venv/bin/python scripts/apply_state_url_corrections.py
```

Then regenerate the final audit:

```bash
scripts/.venv/bin/python scripts/audit_state_urls.py --insecure --timeout 8 \
  --output entitysearch-state-data/audits/url-audit-final-YYYY-MM-DD.json
```
