# DBA Rules Namespace (`dba-rules/states/*.json`)

**Additive namespace** — DBA / assumed name / fictitious name / trade name filing
rules per state, hand-researched from official state statutes, Secretary of State
guidance, and (where filing is county-level) official county filing-office pages.
This directory is independent of `entitysearch-state-data/` and `name-rules/` and
never modifies them; consumers of the existing namespaces are unaffected.

**Coverage is complete: 51 of 51 jurisdictions**, meaning all 50 states plus the
District of Columbia (`washington-d-c.json`, `stateAbbr: "DC"`). The namespace
began with 5 pilot states (GA, TX, CA, FL, OH) and reached full coverage on
2026-07-23.

**Schema extended 2026-07-18:** `filingLevel` gained a fourth value, `"none"`, for
states with **no DBA / assumed-name registration** for LLCs, corporations, and sole
proprietors. South Carolina (no statewide filing; trading names are a local
business-license matter, with a narrow LP / foreign-entity assumed-name exception
at the SoS) and Kansas (no registry at any level; the SoS forms list says no
application registers an assumed, fictitious, trade, or DBA name) are recorded
this way. For `"none"` states the fee, duration, publication, and filing fields
describe the absence and the nearest real instrument, and `llcFee` stays `null`.

## Schema

| Field | Type | Meaning |
|-------|------|---------|
| `stateName` / `stateAbbr` / `stateSlug` | `string` | Same identifiers as `entitysearch-state-data/states/*.json` |
| `dbaTerm` | `string` | What the state's own statute calls the filing (e.g. `"assumed name"`, `"trade name"`, `"fictitious business name"`) |
| `filingLevel` | `"state" \| "county" \| "split" \| "none"` | Which level of government takes the filing; `"split"` = depends on owner type; `"none"` = no such filing exists in the state |
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

Same integrity protocol as the root dataset: see **Methodology** in the
[repository README](../README.md#methodology) for what counts as an official
source, which non-`.gov` hosts are official, and the exact conditions of the
exception below. Every fact is verified against official government sources
(statutes, administrative codes, Secretary of State and county filing-office
pages); every file carries its `sources` and `lastVerified`.

A handful of states license their code to a commercial publisher and put no free
citable copy online (Georgia's O.C.G.A. is the clearest case). Only there may
`statuteUrl` point at a verbatim mirror, and only when the record also carries an
official source that independently supports the same fact and its `notes` field
says the state publishes no free official copy. Everywhere an official copy of the
statute is reachable, a mirror is a defect.

Copy style: no em dashes in any string field (they render on consumer sites);
en dash only between numbers.

## Usage

```
https://raw.githubusercontent.com/startupsolellc/us-llc-fees-dataset/main/dba-rules/states/{state-slug}.json
```
