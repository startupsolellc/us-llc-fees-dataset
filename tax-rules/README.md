# tax-rules

**Status: draft / proposal. Not published, not part of the dataset yet.**

Per-jurisdiction record of the recurring state-level taxes an LLC owes for existing: franchise
and privilege taxes under whatever name the state gives them, and the posture of the state's
personal income tax toward a default (pass-through) LLC. One JSON file per jurisdiction in
`states/<slug>.json`.

This namespace is additive: it adds no key to `states.json`, `entitysearch-state-data`,
`name-rules`, `dba-rules` or `processing-time`, and nothing already published changes because of
it. A consumer that ignores this directory sees exactly the dataset it saw before.

---

## Why this namespace exists separately

The root dataset answers "what does the state charge to file". This namespace answers a
different question: **what does the state charge the LLC for existing**, year after year, once
the filing fees are paid. That fact is scattered, mislabeled, and routinely conflated with the
annual report fee — by states and by the sites that copy each other's tables.

**The label is not the substance.** The same economic fact is called a franchise tax (TX), an
annual tax (DE), a business privilege tax (AL), an annual report license tax (WY), or a
commercial activity tax (OH). A record here is keyed to the substance — a recurring state-level
levy on the LLC's existence or privilege of doing business, as distinct from tax on income
passed through to members — and carries the state's own label verbatim in `taxName`, so a
consumer can render what the state actually calls it.

## Scope boundaries

- **Default (pass-through) LLC taxation only.** An LLC that has elected corporate treatment is
  out of scope; the record describes the default entity.
- **No rate brackets.** `stateIncomeTax` carries the top marginal rate and whether a
  pass-through entity tax election exists, as orientation, not as tax advice. Bracket tables
  are deliberately excluded: their maintenance cost is out of all proportion to their value
  here.
- **No local taxes.** City and county levies (e.g. municipal business taxes) are out of scope.
- **No federal tax.** Nothing here describes the IRS.
- **The annual report fee stays where it is.** Root `states.json` `annual_report_fee` remains
  authoritative for what is paid with or as the annual report. Where a state's franchise-type
  tax *is* that payment, the record says so (`collectedWithAnnualReport: true`) rather than
  restating the figure as a second authoritative value — a total-cost consumer must not count
  it twice. One fact, one field.
- **This namespace is authoritative for franchise-tax structure** (whether it applies, its
  basis, its minimum, who collects it, when it is due). Any other mention of franchise or
  privilege taxes elsewhere in the dataset is prose, not a value to be read.

## Sourcing

Held to the standard in the root `README.md` §Methodology, with one clarification it already
implies: for this namespace the official publisher is usually the state's **tax authority** —
a Franchise Tax Board, a Comptroller, a Department of Revenue — not the Secretary of State.
A Secretary of State page describing another agency's tax is a pointer, not a source. No blogs,
no formation-service pages, no commercial aggregators — including as corroboration.

Every admissible value is bound to a verbatim passage quoted from the cited page (`evidence`),
and `applies: false` is admissible only with evidence from a page that would have said so if a
tax existed. `null` means not yet researched, and is always preferred to a plausible guess.

## Field dictionary

### Identity

| Field | Type | Notes |
|---|---|---|
| `stateName`, `stateAbbr`, `stateSlug` | string | Same conventions as the other namespaces |

### `franchiseTax`

| Field | Type | Notes |
|---|---|---|
| `applies` | boolean \| null | `false` is a researched finding and requires `appliesEvidence`; `null` means not yet researched |
| `appliesEvidence` | evidence \| null | Required when `applies` is `false`: a passage showing the state's own statement of what recurring entity taxes exist |
| `taxName` | string \| null | The state's own label, verbatim |
| `basis` | enum \| null | `flat` · `net-worth` · `revenue` · `hybrid` |
| `minimumAnnualUsd` | number \| null | The floor an existing LLC pays in an ordinary year; `null` where no minimum is published |
| `firstYearExemption` | boolean \| null | Statutory first-year waivers; expiry dates and conditions go to `notes` |
| `filedWith` | string \| null | The collecting agency's name, verbatim — most franchise taxes are not the Secretary of State's business |
| `collectedWithAnnualReport` | boolean \| null | `true` where this tax is the annual-report payment root `states.json` already carries — the anti-double-counting flag |
| `dueDate` | string \| null | The state's own statement, verbatim; not normalised |
| `evidence` | evidence \| null | The passage establishing the tax and its figure |

### `stateIncomeTax`

| Field | Type | Notes |
|---|---|---|
| `passThroughApplies` | boolean \| null | Whether members owe state personal income tax on pass-through income |
| `topRatePercent` | number \| null | Top marginal rate, orientation only |
| `hasPTETElection` | boolean \| null | Whether a pass-through entity tax election exists |
| `evidence` | evidence \| null | |

### Record plumbing

| Field | Type | Notes |
|---|---|---|
| `notes` | string | Anything the fields cannot carry without lying |
| `needsReview` | string \| null | What is missing and what would settle it |
| `sources` | array | `citation`, `title`, `url`, `type` (`statute` · `agency-page` · `fee-schedule` · `official-pdf` · null), `lastAccessed` |
| `lastVerified` | date | The date the cited pages were retrieved and every quoted passage mechanically confirmed to occur in them |

An `evidence` object is a contiguous verbatim passage plus the URL it occurs on. Quotes are
never assembled across ellipses, never taken from search snippets, and never tidied.

## The pilot

The namespace opens with five jurisdictions chosen to stress the schema, not to cover ground:
**California** (flat minimum collected by a tax board, plus a revenue-scaled companion fee),
**Texas** (margin-based, with a no-tax-due threshold), **Delaware** (a flat annual tax that is
the annual obligation itself), **Tennessee** (a two-component franchise-and-excise regime), and
**Wyoming** (expected `applies: false` for a franchise tax proper, next to an annual-report
license tax that tests the boundary). Every structural expectation named here is a hypothesis
until the record's own sources confirm it. The schema is expected to change during the pilot;
that is what a pilot is for.

This is not legal or tax advice, and nothing here is a filing instruction. Tax figures move
with legislative sessions; read `lastVerified` before trusting any of them.
