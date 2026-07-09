# Name Rules Namespace (`name-rules/states/*.json`)

**Additive namespace** — LLC naming rules per state, hand-researched from official
state statutes and Secretary of State guidance. This directory is independent of
`entitysearch-state-data/` and never modifies it; consumers of the existing
namespaces are unaffected.

Coverage starts with 5 pilot states (GA, TX, CA, FL, OH) and grows over time.
A missing `{state-slug}.json` simply means that state has not been researched yet.

## Schema

| Field | Type | Meaning |
|-------|------|---------|
| `stateName` / `stateAbbr` / `stateSlug` | `string` | Same identifiers as `entitysearch-state-data/states/*.json` |
| `entitySuffixRule` | `string` | Required designators/suffix for an LLC name, with statute cite |
| `distinguishabilityNote` | `string \| null` | The state's distinguishability standard, summarized |
| `restrictedWords` | `string[]` | Words prohibited or requiring regulator approval (see `notes` for which) |
| `nameReservationFee` | `number \| null` | Base reservation fee in USD (`null` = no reservation offered) |
| `nameReservationDuration` | `string \| null` | e.g. `"120 days"`, `"120 days (non-renewable)"` |
| `nameReservationUrl` | `string \| null` | Official page describing how to reserve |
| `namingStatuteUrl` | `string \| null` | Official statute / administrative-rule link |
| `notes` | `string \| null` | Nuances: approval authorities, renewal rules, service charges |
| `sources` | `{name, url, lastAccessed}[]` | Official sources used for verification |
| `lastVerified` | `string` | ISO date of last manual verification |

## Sourcing rules

Same integrity protocol as the root dataset (see repository `AGENTS.md`): every
fact verified against official state government sources (statutes, administrative
codes, Secretary of State pages); no third-party blogs; every file carries its
`sources` and `lastVerified`.

## Usage

```
https://raw.githubusercontent.com/startupsolellc/us-llc-fees-dataset/main/name-rules/states/{state-slug}.json
```
