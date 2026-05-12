# EntitySearch State Data

Structured state-level dataset for sidebar components. This data is designed for use in sidebar components on external websites.

## Status

As of `2026-05-12`, detailed enrichment batch operations have been completed for all 50 states.

- **Coverage:** `AL` through `WY`
- **Last completed batch:** `WI / WY`
- Each state file contains contact info, addresses, hours, renewal links, LLC filing facts, name reservation details, and official sources — or consciously left as `null` if not available from official sources.
- Root [`../states.json`](../states.json) records have been aligned with official fee/source corrections.
- Batch audit outputs are generated locally under `entitysearch-state-data/audits/`. This folder is under `.gitignore`.

## Structure

```
entitysearch-state-data/
├── README.md
├── schema/
│   └── state.schema.json      # JSON validation schema
├── states/                    # Individual state JSON files
│   └── alabama.json           # Example state file
└── assets/
    ├── seals/                 # State seal images (.webp)
    └── provider-logos/       # Bizee, Northwest, IncAuthority logos
```

## Schema Fields

| Field | Type | Description |
|------|------|-------------|
| `stateName` | string | Full state name |
| `stateAbbr` | string | 2-letter state abbreviation (e.g., AL) |
| `stateSlug` | string | URL-friendly slug (e.g., alabama) |
| `stateSeal` | string\|null | State seal URL (WebP preferred) |
| `businessEntitySearch` | object | Search CTA and URL |
| `secretaryOfState` | object | Agency information |
| `hours` | object | Operating hours |
| `physicalAddresses` | array | Physical addresses |
| `mailingAddress` | object | Mailing address |
| `renewals` | object | Renewal links |
| `corporateDocuments` | object | Template links |
| `filingFacts` | object | LLC fee, annual report, name reservation |
| `sources` | array | Official sources |
| `lastVerified` | string | ISO date (YYYY-MM-DD) |

## Optional Enrichment Fields

The following fields are **not mandatory core data** for the entity search experience, and missing values are not considered data quality issues:

| Field | Status | Note |
|-------|--------|------|
| `stateSeal` | Optional | In an app that consumes seal/logo assets, e.g., Astro `src/assets/images/statesseals`, can be managed there. |
| `secretaryOfState.officialName` | Optional | Current official name/since info is time-sensitive political/personnel data; can be left empty without a separate maintenance process. |
| `corporateDocuments` | Optional | Operating agreement, bylaws, and partnership agreement template pages can be produced as separate internal content. If no official state template exists, stays `null`. |

**Core data target:** Official search URL, agency website, contact info (phone/email if available), address, hours, filing/renewal facts, and source tracking — practical information for the entity search user.

## Data Rules

- **Official sources only** (.gov domains)
- **Fee and requirement verification:** Every fee, due date, and filing requirement is verified against the official state government portal, official fee schedule, official statute, or official filing portal
- **Source requirement:** `sources[]`, root `official_link`, and root `source_url` fields must point to official sources
- **No third-party sources:** Legal service providers, blogs, SEO pages, news sites, or commercial summary sources are not used
- **Unknown values:** Left as `null` or empty
- **Date format:** ISO 8601 (`YYYY-MM-DD`)
- **Image format:** WebP preferred
- **URL validation:** Valid URI format required

## Usage

```javascript
const stateData = require('./states/alabama.json');

// Sidebar usage example
console.log(stateData.stateName); // "Alabama"
console.log(stateData.secretaryOfState.website); // "https://www.sos.alabama.gov"
```

## Validation

To validate JSON files against `state.schema.json`:

```bash
npx ajv-cli validate --strict=false -s entitysearch-state-data/schema/state.schema.json -d 'entitysearch-state-data/states/*.json'
```

JSON parse check:

```bash
jq empty states.json entitysearch-state-data/states/*.json
```

## Future Update Workflow

Since all states have been enriched, future work should focus on periodic verification, official fee change tracking, and link health checks rather than generating new batches. Maintenance work should still follow the same batch logic.

### Batch Selection

- Divide states to update into small batches of 2-3 states.
- For each batch, first read the existing state JSON files and root `states.json` records.
- Clearly state batch scope in the final response and handoff notes if needed.

Example:

```bash
sed -n '1,220p' entitysearch-state-data/states/wisconsin.json
sed -n '1,220p' entitysearch-state-data/states/wyoming.json
sed -n '490,540p' states.json
```

### Official Source Research

For each state, **only use these source types**:

- Secretary of State or Department of State corporation/business division pages
- Department of Financial Institutions, Department of Revenue, or official filing agency pages
- Official fee schedule HTML/PDF pages
- Official annual report, renewal, or business filing portals
- Official state statute pages

**Do not use:**

- LegalZoom, Northwest, ZenBusiness, Harbor Compliance, Forbes, etc. commercial pages
- Blogs, SEO landing pages, news sites
- Search result snippets only

> If the audit returns `403`, timeout, or connection reset due to official portal bot protection, the URL should not be automatically dropped. If it's an official state page, it can be kept; if possible, add an additional official `200`-returning source that supports the same information.

### Fields to Update

For each state file, check these fields:

- `businessEntitySearch.url`
- `secretaryOfState.agency`
- `secretaryOfState.website`
- `secretaryOfState.phone`
- `secretaryOfState.email`
- `hours.timezone`
- `hours.regular`
- `physicalAddresses[]`
- `mailingAddress`
- `renewals.onlineRenewalUrl`
- `renewals.paperRenewalUrl`
- `renewals.notes`
- `filingFacts.llcFee`
- `filingFacts.llcFeeNotes`
- `filingFacts.annualReport`
- `filingFacts.annualReportDue`
- `filingFacts.nameReservation`
- `filingFacts.nameReservationNotes`
- `sources[]`
- `lastVerified`

In root `states.json`, only update if official data changed or source link was corrected:

- `formation_fee`
- `annual_report_fee`
- `annual_report_due_date`
- `official_link`
- `source_url`
- `last_verified`
- root `last_updated`

### Timestamp and Source Format

- `lastVerified` in touched state file must be current ISO date.
- `lastAccessed` in touched source records must be current ISO date.
- Relevant state `last_verified` in root `states.json` must be updated.
- If official data change was made across the dataset, root `last_updated` must be updated.

### Annual Report and Fee Rules

- If there's no annual report fee in root `states.json`, use `annual_report_fee: 0`.
- Follow existing pattern in detail state JSON: if a state has no annual report, `annualReport: null` and `annualReportDue: "N/A"` can be used.
- If online and paper fees differ, the most practical/current online fee can be used as the main value; paper fee should be clearly noted in notes.
- If there's a minimum/maximum or asset-based fee, write the minimum fee as the main value; explain variable structure in `filingFacts.*Notes` and `renewals.notes`.

### Batch Audit

Generate URL audit at the end of each batch:

```bash
scripts/.venv/bin/python scripts/audit_state_urls.py --state WI --state WY --insecure --timeout 8 --output entitysearch-state-data/audits/url-audit-batch-wi-wy-2026-05-12.json
```

To extract audit summary:

```bash
jq -r '.states | to_entries[] as $s | $s.value.urls[] | [$s.key, (.fetched.status // "ERR"), .url, (.fetched.error // "")] | @tsv' entitysearch-state-data/audits/url-audit-batch-wi-wy-2026-05-12.json
```

The audit folder is kept out of git. Audit file can be linked in the final report but not included in commits.

### Batch End Checklist

1. Run JSON parse check:

```bash
jq empty states.json entitysearch-state-data/states/*.json
```

2. Run schema validation:

```bash
npx ajv-cli validate --strict=false -s entitysearch-state-data/schema/state.schema.json -d 'entitysearch-state-data/states/*.json'
```

3. Run batch audit and note caveats.
4. If `handoff.md` exists, write current batch, audit file, caveats, and next step.
5. Check with `git diff` that only expected files changed.
6. Write commit message to describe batch scope.

Example commit messages:

```text
Enrich Wisconsin and Wyoming data
Refresh California and Colorado official fee sources
Audit annual report URLs for southeast batch
```

### Agent Notes

- Keep changes small and limited to batch scope.
- Do not revert other user or agent changes.
- Preserve existing field order and file style in JSON edits.
- If changing fee or due date, specifically note in final response.
- If official URL audit errors, try to distinguish whether it's automation-related or a genuinely broken link.
- If a broken official link is replaced with an updated official page, both state JSON `sources[]` and root `states.json` sources must be updated.

---

## Built With This Dataset

### [EntitySearch.us](https://entitysearch.us)

Comprehensive step-by-step guides for business entity search across all 50 US states. Each state page features screenshots, official portal links, and LLC formation facts powered by this dataset.

```
https://entitysearch.us/texas/
https://entitysearch.us/wyoming/
https://entitysearch.us/delaware/
```

---

*This dataset is part of the `us-llc-fees-dataset` repository.*