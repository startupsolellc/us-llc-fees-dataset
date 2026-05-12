# Handoff: Entity Search State Data Enrichment

Date: 2026-05-12
Workspace: `/Users/muhammetdikyurt/Projects/repos/us-llc-fees-dataset`

## Goal

Continue enriching `entitysearch-state-data/states/*.json` in alphabetical 3-state batches. The dataset is for US LLC fees and state business entity search metadata. Accuracy matters: use only official state/government sources, preferably `.gov` or the state's official filing portal linked from a `.gov` page.

Follow `AGENTS.md` strictly:

- Verify every fee and requirement via official state government sources.
- `source_url`, `official_link`, and per-state `sources[]` must point to official fee schedules, corporation divisions, statutes, or official filing portals.
- Do not use third-party blogs, legal service providers, or commercial summaries.
- Update the specific state's `lastVerified` and root `states.json` `last_verified` / `last_updated` when touching data.

## Current Progress

All 50 state JSON files exist.

Enrichment is complete through:

- `AL` through `OK`, including the last completed batch `ND / OH / OK`.

The most recent completed audit:

- `entitysearch-state-data/audits/url-audit-batch-nd-oh-ok-2026-05-12.json`

Remaining states, in order:

1. `OR` Oregon
2. `PA` Pennsylvania
3. `RI` Rhode Island
4. `SC` South Carolina
5. `SD` South Dakota
6. `TN` Tennessee
7. `TX` Texas
8. `UT` Utah
9. `VT` Vermont
10. `VA` Virginia
11. `WA` Washington
12. `WV` West Virginia
13. `WI` Wisconsin
14. `WY` Wyoming

Next batch to run:

- `OR / PA / RI`

## Files To Edit Per Batch

For each state, update:

- `entitysearch-state-data/states/<state-slug>.json`
- `states.json` only if root fee, due date, source URL, official link, or verification date needs correction
- Create one batch audit file in `entitysearch-state-data/audits/`

Audit filename pattern:

```text
entitysearch-state-data/audits/url-audit-batch-nd-oh-ok-2026-05-12.json
```

## Fields To Fill

For each state JSON, fill or verify:

- `businessEntitySearch.url`
- `secretaryOfState.agency`
- `secretaryOfState.website`
- `secretaryOfState.phone`
- `secretaryOfState.email` when a real email address is officially published; otherwise keep `null`
- `hours.timezone`
- `hours.regular`
- `physicalAddresses[]`
- `mailingAddress`
- `renewals.onlineRenewalUrl`
- `renewals.paperRenewalUrl` if official and useful; otherwise `null`
- `renewals.notes`
- `filingFacts.llcFee`
- `filingFacts.llcFeeNotes`
- `filingFacts.annualReport`
- `filingFacts.annualReportDue`
- `filingFacts.nameReservation`
- `filingFacts.nameReservationNotes`
- `sources[]` with official URLs and `lastAccessed: "2026-05-12"`
- `lastVerified: "2026-05-12"`

Root `states.json` should stay aligned with official data:

- `formation_fee`
- `annual_report_fee`
- `annual_report_due_date`
- `official_link`
- `source_url`
- `last_verified`
- root `last_updated`

Use `0` in root `states.json` when the state has no LLC annual report fee. In the detailed state JSON, existing pattern is sometimes `annualReport: null` with `annualReportDue: "N/A"` for no report requirement; follow the pattern already used for similar states unless schema/user expectations require otherwise.

## Research Method

For each batch:

1. Read current state JSONs and root entries.
2. Search/browse official sources for each state.
3. Use `curl` against official pages where possible to capture exact fee/contact lines.
4. Patch JSON files with `apply_patch`.
5. Run JSON/schema validation.
6. Run URL audit for the batch.
7. Summarize changed files, validation result, and audit caveats.

Use official sources such as:

- Secretary of State / Department of State corporation division pages
- Official fee schedule pages/PDFs
- Official annual report / online filing portals linked from state pages
- Official state statutes only when fee schedules are incomplete or bot-protected

Do not rely on:

- LegalZoom, Northwest, ZenBusiness, Harbor Compliance, Forbes, blogs, SEO pages
- Search result snippets without confirming the linked official source

## Useful Commands

Read current state files:

```bash
sed -n '1,220p' entitysearch-state-data/states/north-dakota.json
sed -n '1,220p' entitysearch-state-data/states/ohio.json
sed -n '1,220p' entitysearch-state-data/states/oklahoma.json
sed -n '330,390p' states.json
```

Quick enrichment-gap scan:

```bash
jq -r '[.stateAbbr, .stateName, (.secretaryOfState.phone // ""), (.secretaryOfState.email // ""), ((.physicalAddresses // []) | length), (.renewals.onlineRenewalUrl // ""), (.filingFacts.nameReservation // "")] | @tsv' entitysearch-state-data/states/*.json
```

Validate JSON syntax:

```bash
jq empty entitysearch-state-data/states/north-dakota.json entitysearch-state-data/states/ohio.json entitysearch-state-data/states/oklahoma.json states.json
```

Validate schema:

```bash
npx ajv-cli validate --strict=false -s entitysearch-state-data/schema/state.schema.json -d 'entitysearch-state-data/states/*.json'
```

Run batch URL audit:

```bash
scripts/.venv/bin/python scripts/audit_state_urls.py --state ND --state OH --state OK --insecure --timeout 8 --output entitysearch-state-data/audits/url-audit-batch-nd-oh-ok-2026-05-12.json
```

Summarize audit statuses:

```bash
jq -r '.states | to_entries[] as $s | $s.value.urls[] | [$s.key, (.fetched.status // "ERR"), .url, (.fetched.error // "")] | @tsv' entitysearch-state-data/audits/url-audit-batch-nd-oh-ok-2026-05-12.json
```

## Known Audit Caveats

Some official portals return `403`, bot pages, connection resets, or timeouts to automated audit requests while still being official and valid. This happened in recent batches:

- Nevada Legislature NRS pages: Cloudflare `403`
- NH QuickStart: `403`
- NJ portal pages: connection reset
- NM enterprise/BFS portal: `403` / connection reset
- NM Legislature PDF: timeout in audit
- NC business search endpoint: `403`

When this happens:

- Keep the official URL if it is linked from an official state page.
- Add supporting official source pages that return `200` whenever possible.
- Mention the audit caveat in the final user summary.

## Recent Completed Batch Notes

`ND / OH / OK` changes:

- `north-dakota.json`: phone/email, address, hours, FirstStop annual report note, LLC fee notes, name reservation note, supporting official sources.
- `ohio.json`: business services phone/email, Client Service Center and mailing address, hours, no annual report note, name reservation `$39`, supporting official sources.
- `oklahoma.json`: business filing department phone/address/hours, annual certificate online/paper links, annual certificate `$25`, name reservation `$10`, supporting official sources.
- `states.json`: no fee corrections needed for this batch; root values matched official sources.
- Audit caveat: Ohio official portals returned `403` to automated audit requests while remaining official state URLs.

`NM / NY / NC` changes:

- `new-mexico.json`: phone/email, address, hours, no annual report note, online business portal note, name reservation `$20`.
- `new-york.json`: phone/email, address, hours, e-Biennial portal, biennial `$9`, name reservation `$20`.
- `north-carolina.json`: phone/email, address, hours, annual report portal, online annual report `$203`, paper `$200`, name reservation `$10`.
- `states.json`: NC annual report fee updated from `202` to `203` because official NC due-date page says online `$203` and paper `$200`.

## Worktree Notes

The worktree is already dirty and includes many uncommitted generated/enrichment files. Do not revert unrelated changes. Only patch the files needed for the current batch.

Expected relevant untracked/modified paths include:

- `entitysearch-state-data/states/*.json`
- `entitysearch-state-data/audits/*.json`
- `states.json`
- `scripts/`
- `.gitignore`

## Final Response Pattern

Answer the user in Turkish. Keep it concise:

- State the batch completed.
- List updated state JSON files.
- Mention any root `states.json` corrections.
- Confirm AJV validation passed.
- Link the audit file.
- Mention audit caveats for official portals that returned `403`, bot pages, or timeouts.

Do not over-explain unless a fee changed from the previous root value.
