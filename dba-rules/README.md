# DBA Rules Namespace (`dba-rules/states/*.json`)

**Additive namespace** — DBA / assumed name / fictitious name / trade name filing
rules per state, hand-researched from official state statutes, Secretary of State
guidance, and (where filing is county-level) official county filing-office pages.
This directory is independent of `entitysearch-state-data/` and `name-rules/` and
never modifies them; consumers of the existing namespaces are unaffected.

Coverage starts with 5 pilot states (GA, TX, CA, FL, OH) and grows over time.
A missing `{state-slug}.json` simply means that state has not been researched yet.

## Schema

| Field | Type | Meaning |
|-------|------|---------|
| `stateName` / `stateAbbr` / `stateSlug` | `string` | Same identifiers as `entitysearch-state-data/states/*.json` |
| `dbaTerm` | `string` | What the state's own statute calls the filing (e.g. `"assumed name"`, `"trade name"`, `"fictitious business name"`) |
| `filingLevel` | `"state" \| "county" \| "split"` | Which level of government takes the filing; `"split"` = depends on owner type |
| `llcFilesWith` | `string` | The office an LLC or corporation files with |
| `soleProprietorFilesWith` | `string` | The office a sole proprietor or partnership files with |
| `llcFee` | `number \| null` | Fixed statewide cost in USD on the LLC filing path; `null` when each county sets its own fee (see `feeBasis`) |
| `feeBasis` | `string` | What the fee covers, why it is null, or verified county examples. Never compare `llcFee` across states without reading this |
| `duration` | `string` | How long the registration lasts (e.g. `"5 years"`, `"No expiration"`) |
| `renewalRule` | `string \| null` | Renewal window and terms |
| `publicationRequired` | `boolean` | Whether a newspaper publication step exists |
| `publicationRule` | `string \| null` | The publication requirement with statute cite |
| `protectionLevel` | `"none" \| "county-presumption" \| "exclusive-registration"` | The strongest name protection the state's DBA-type filing can carry |
| `protectionNote` | `string` | What the filing legally does or does not do to name rights, statute-backed |
| `searchUrl` | `string \| null` | Official lookup for existing registrations; `null` when no statewide index exists |
| `searchNote` | `string` | How existing registrations are actually searched |
| `filingUrl` | `string \| null` | Official how-to or filing page |
| `statuteCitation` / `statuteUrl` | `string` | Governing statute and an accessible copy of it |
| `notes` | `string \| null` | Nuances: deadlines, penalties, terminology traps |
| `sources` | `{citation, title, url, lastAccessed}[]` | Sources used for verification (`citation` = authority or statute number, `title` = document title) |
| `lastVerified` | `string` | ISO date of last manual verification |

## Sourcing rules

Same integrity protocol as the root dataset (see repository `AGENTS.md`): every
fact verified against official government sources (statutes, administrative codes,
Secretary of State and county filing-office pages); no third-party blogs; every
file carries its `sources` and `lastVerified`. Where a state's code has no free
official host (Georgia's O.C.G.A.), the statute link points at an accessible
verbatim copy and the facts are cross-verified against official state and county
pages listed alongside it.

Copy style: no em dashes in any string field (they render on consumer sites);
en dash only between numbers.

## Usage

```
https://raw.githubusercontent.com/startupsolellc/us-llc-fees-dataset/main/dba-rules/states/{state-slug}.json
```
