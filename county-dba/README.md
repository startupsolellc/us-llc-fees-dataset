# county-dba

**Status: draft / proposal. Not published, not part of the dataset yet.**

Per-jurisdiction record of the **county dimension of DBA costs**: a verified fee range and up
to three example counties per jurisdiction, plus a note on publication cost where publication
is required. One JSON file per jurisdiction in `states/<slug>.json`.

This namespace is additive: it adds no key to `states.json`, `entitysearch-state-data`,
`name-rules`, `dba-rules`, `processing-time` or `tax-rules`, and nothing already published
changes because of it. A consumer that ignores this directory sees exactly the dataset it saw
before.

## Scope: county-dimension jurisdictions only

This namespace does **not** collect 51 jurisdictions. It covers the jurisdictions where DBA
costs have a county dimension — where the filing level is county or split, or where
publication is required — as already recorded in `dba-rules` (`filingLevel` and
`publicationRequired`). Measured from the current data that is **16 jurisdictions**; the
remaining 35 are out of scope by design and need no record. The README's coverage statement
will name the set, not a 51/51 claim.

## Why this namespace exists separately

`dba-rules` already records the state-level facts, including the important sentence "each
county sets its own fee". What a filer actually needs next is numbers: a range and verified
examples from official county pages. This namespace adds that layer without touching the
state-level contract, and it deliberately caps the work — three examples per jurisdiction,
no county-by-county census.

## Scope boundaries

- **Costs only.** The county filing fee and, where required, the publication cost. The
  publication *requirement* stays authoritative in `dba-rules`
  (`publicationRequired` / `publicationRule`); this namespace never restates it as a value.
- **Verified examples, capped at three.** `examples` never lists more than three counties per
  jurisdiction, and every example is read from that county's own official page.
- **A range is sourced, never derived.** `feeRangeUsd` is the range the official pages actually
  show, or the range spanned by the verified examples — never an average, never a guess.
- **This namespace is authoritative for county DBA fee figures and publication costs.** The
  county examples in `dba-rules` `feeBasis` are narrative; where they disagree with a record
  here, this namespace wins.
- **No "unknown" estimation.** A county whose fee is not published is simply absent from
  `examples`; three-state null discipline applies.

## Sourcing

Held to the standard in the root `README.md` §Methodology. The publisher is the county filing
office — a Clerk of Superior Court, a county clerk, a Register of Deeds — or the official legal
organ that sets the publication rate. No blogs, no formation-service pages, no commercial
aggregators, including as corroboration.

Every admissible value is bound to a verbatim passage quoted from the cited page (`evidence`).
`null` means not yet researched and is always preferred to a plausible guess.

## Field dictionary

### Identity

| Field | Type | Notes |
|---|---|---|
| `stateName`, `stateAbbr`, `stateSlug` | string | Same conventions as the other namespaces; DC uses `district-of-columbia` |

### `countyDba`

| Field | Type | Notes |
|---|---|---|
| `applies` | boolean \| null | Whether this jurisdiction has a county dimension. `false` is only used inside the scoped set, for a jurisdiction whose county costs turned out not to vary |
| `feeRangeUsd` | object \| null | `{min, max}` — the range the official pages show or the verified examples span |
| `publicationCostNote` | string \| null | One short sentence on publication cost where publication is required |
| `examples` | array, max 3 | `{county, feeUsd, publicationFeeUsd, note}` — verified county examples |
| `note` | string \| null | Anything the fields cannot carry |
| `evidence` | evidence[] | One verbatim passage per value |

### Record plumbing

`notes`, `needsReview`, `sources[]` (`citation`, `title`, `url`, `type`, `lastAccessed`) and
`lastVerified` carry their usual meaning from the other draft namespaces.

## The pilot

The namespace opens with five jurisdictions chosen to stress the schema, not to cover ground.
Hypothesis candidates: **California** (county-set fees under a statutory cap), **Georgia**
(county clerk fees plus a publication fee), **New York** (per-county fees), **Nebraska**
(state filing with publication) and **Minnesota** (state filing with publication). Every
expectation here is a hypothesis until the record's own sources confirm it; the schema is
expected to change during the pilot.

This is not legal advice, and nothing here is a filing instruction. County fees move
frequently; read `lastVerified` before trusting any of them.
