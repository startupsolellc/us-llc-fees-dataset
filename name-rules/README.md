# Name Rules Namespace (`name-rules/states/*.json`)

**Additive namespace** — LLC naming rules per state, hand-researched from official
state statutes and Secretary of State guidance. This directory is independent of
`entitysearch-state-data/` and never modifies it; consumers of the existing
namespaces are unaffected.

**Coverage is complete: 51 of 51 jurisdictions**, meaning all 50 states plus the
District of Columbia (`washington-d-c.json`, `stateAbbr: "DC"`). The namespace
began with 5 pilot states (GA, TX, CA, FL, OH) and reached full coverage on
2026-07-23.

## Schema

| Field | Type | Meaning |
|-------|------|---------|
| `stateName` / `stateAbbr` / `stateSlug` | `string` | Same identifiers as `entitysearch-state-data/states/*.json` |
| `entitySuffixRule` | `string` | Required designators/suffix for an LLC name |
| `entitySuffixCitation` | `string \| null` | Statute backing `entitySuffixRule` |
| `distinguishabilityNote` | `string \| null` | The state's distinguishability standard, summarized |
| `distinguishabilityCitation` | `string \| null` | Statute backing `distinguishabilityNote` |
| `restrictedWords` | `string[]` | Words prohibited or requiring regulator approval (see `notes` for which) |
| `nameReservationFee` | `number \| null` | Statutory reservation filing fee in USD (`null` = no reservation offered). **Not comparable across states**: use `nameReservationTotalCost` |
| `nameReservationTotalCost` | `number \| null` | Real out-of-pocket cost on the common filing path, incl. service charges and card fees |
| `nameReservationCostBasis` | `string \| null` | What the total includes and why it differs from the filing fee |
| `nameReservationDuration` | `string \| null` | e.g. `"120 days"`, `"120 days (non-renewable)"` |
| `nameReservationProcessingTime` | `string \| null` | Published turnaround, where the state publishes one |
| `nameReservationUrl` | `string \| null` | Official page describing how to reserve |
| `namingStatuteUrl` | `string \| null` | Official statute / administrative-rule link. **Points at the source behind `distinguishabilityCitation`** — the provision that decides whether a name is available — and falls back to `entitySuffixCitation`'s source only where the state has no separate distinguishability provision. In most states one section carries both. |
| `notes` | `string \| null` | Nuances: approval authorities, renewal rules, service charges |
| `sources` | `{citation, title, url, lastAccessed}[]` | Official sources used for verification (`citation` = authority or statute number, `title` = document title) |
| `lastVerified` | `string` | ISO date of last manual verification |

## Sourcing rules

Same integrity protocol as the root dataset: see **Methodology** in the
[repository README](../README.md#methodology) for what counts as an official
source, which non-`.gov` hosts are official, and the narrow exception for
jurisdictions that publish no free copy of their own code. Every fact is verified
against official sources; commercial statute mirrors are not accepted; every file
carries its `sources` and `lastVerified`.

`nameReservationTotalCost` is the authoritative reservation cost for this dataset.
`entitysearch-state-data`'s `filingFacts.nameReservation` mirrors it and must agree
with it.

## Usage

```
https://raw.githubusercontent.com/startupsolellc/us-llc-fees-dataset/main/name-rules/states/{state-slug}.json
```
