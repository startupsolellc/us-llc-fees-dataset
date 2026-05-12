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

- `AL` through `WV`, including the last completed batch `VA / WA / WV`.

The most recent completed audit:

- `entitysearch-state-data/audits/url-audit-batch-va-wa-wv-2026-05-12.json`

Remaining states, in order:

1. `WI` Wisconsin
2. `WY` Wyoming

Next batch to run:

- `WI / WY`

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
- TX SOS business services homepage: `403`
- Vermont SOS pages and business filing portal: `403`
- Vermont Legislature statute pages: timeout in automated audit, but accessible in browser/web lookup
- Virginia SCC/CIS official pages: automated curl closed connections, but pages were verified through browser/web lookup
- West Virginia business entity search endpoint: timeout in automated audit; SOS source pages returned `200`

When this happens:

- Keep the official URL if it is linked from an official state page.
- Add supporting official source pages that return `200` whenever possible.
- Mention the audit caveat in the final user summary.

## Recent Completed Batch Notes

`VA / WA / WV` changes:

- `virginia.json`: SCC Clerk phone/email/address/hours, CIS renewal URL, annual registration fee note, LLC formation `$100`, annual registration `$50`, name reservation `$10`, official SCC forms/fees/contact/annual registration sources.
- `washington.json`: Corporations & Charities phone/email/address/hours, CCFS renewal URL, current WAC/SOS fee schedule values, LLC formation corrected to `$180`, annual report corrected to `$70`, name reservation `$30`, official SOS and WAC sources.
- `west-virginia.json`: Business & Licensing phone/email, Charleston/Clarksburg/Martinsburg addresses/hours, Business4WV renewal URL, LLC formation `$100`, annual report `$25`, name reservation `$15`, official SOS source pages.
- `states.json`: WA formation fee changed from `200` to `180`, WA annual report fee changed from `60` to `70`, WA source URLs updated to current SOS/WAC fee sources. WV official/source URLs changed from the stale PDF URL to the current `register-new-wv-business` official page.
- Audit caveats: VA SCC/CIS URLs closed automated curl connections. WV business entity search timed out. WA and WV official source pages returned `200`.

`TX / UT / VT` changes:

- `texas.json`: Business & Public Filings contact/address/hours, Comptroller franchise tax renewal/file-and-pay URLs, LLC formation fee `$300`, annual report/tax due date `May 15`, name reservation `$40`, official SOS and Comptroller sources.
- `utah.json`: Division phone/email/address/hours, annual report/renewal URL, LLC formation fee `$59`, annual report/renewal `$18`, due date `Anniversary date`, name reservation `$22`, FY2026 fee schedule and renewal/search sources.
- `vermont.json`: Business Services phone/email/address/hours, annual report note, LLC formation fee `$155`, annual report `$45`, due date corrected to `Within 3 months after fiscal year end`, name reservation `$25`, SOS and Vermont Legislature statute sources.
- `states.json`: TX `official_link` updated to direct Form 205 instructions; VT annual report due date and `source_url` updated to the Vermont LLC fee statute. No root fee amount changes.
- Audit caveats: TX SOS homepage returned `403`, while direct TX SOS instruction/contact pages and Comptroller pages returned `200`. Vermont SOS and filing portal URLs returned `403`; Vermont Legislature statute URLs timed out in automated audit but were verified through browser/web lookup.

`SC / SD / TN` changes:

- `south-carolina.json`: Business Filings phone/address/hours, no Secretary of State annual report note for LLCs, name reservation `$25`, supporting official SOS/businessfilings sources.
- `south-dakota.json`: phone/address/hours, annual report online URL, online annual report `$55`, name reservation `$25`, due date corrected to `1st day of anniversary month`.
- `tennessee.json`: phone/address/hours, annual report online URL, LLC annual report fee note clarifying `$300` minimum to `$3,000` maximum, name reservation `$20`.
- `states.json`: SD annual report due date corrected from `Last day of anniversary month` to `1st day of anniversary month`. No root fee amount changes.
- Audit caveats: SC `sos.sc.gov` returned `403`; SC `businessfilings.sc.gov` and TN BEAR search timed out in automated audit. SD sources and TN main source pages returned `200`.

`OR / PA / RI` changes:

- `oregon.json`: phone/email, address, hours, Oregon Business Registry renewal URL, LLC annual renewal note, name reservation `$100`, direct fee schedule/name reservation sources.
- `pennsylvania.json`: phone/email, address, hours, Business Filing Services annual report URL, 2025 annual report requirement note, name reservation `$70`, annual reports source.
- `rhode-island.json`: phone/email, address, hours, online/paper annual report links, fee notes clarifying base fee plus enhanced access fee, name reservation `$52.50`, direct fee schedule and form sources.
- `states.json`: OR and RI `official_link` / `source_url` updated to direct official fee schedule PDFs. No root fee amount changes.
- Audit caveats: Oregon official `sos.oregon.gov` URLs timed out in the automated audit; PA Business Filing Services search returned `403`. PA source pages and RI sources returned `200`.

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
