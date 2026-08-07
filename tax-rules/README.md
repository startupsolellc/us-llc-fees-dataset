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
| `collectedWithAnnualReport` | boolean \| null | `true` where this tax **is** the payment root `states.json` already carries in `annual_report_fee` — the anti-double-counting flag. Read it as "already counted there", not as "collected alongside a report": Delaware LLCs file no annual report at all and the flag is still `true` |
| `dueDate` | string \| null | The state's own statement, verbatim; not normalised |
| `evidence` | evidence[] \| null | One passage per value, each naming what it grounds in `supports`. The figure, the due date and the first-year waiver are routinely three passages on two pages |

### `stateIncomeTax`

| Field | Type | Notes |
|---|---|---|
| `passThroughApplies` | boolean \| null | Whether members owe state personal income tax on pass-through income |
| `topRatePercent` | number \| null | Top marginal rate, orientation only |
| `hasPTETElection` | boolean \| null | Whether a pass-through entity tax election exists |
| `evidence` | evidence[] \| null | One passage per value. The rate, the pass-through posture and the election are almost never on the same page |

### Record plumbing

| Field | Type | Notes |
|---|---|---|
| `notes` | string | Anything the fields cannot carry without lying |
| `needsReview` | string \| null | What is missing and what would settle it |
| `sources` | array | `citation`, `title`, `url`, `type` (`statute` · `agency-page` · `fee-schedule` · `official-pdf` · null), `lastAccessed` |
| `lastVerified` | date | The date the cited pages were retrieved and every quoted passage mechanically confirmed to occur in them |

An `evidence` object is a contiguous verbatim passage, the URL it occurs on, and an optional
`supports` naming the value it grounds. Quotes are never assembled across ellipses, never taken
from search snippets, and never tidied. **Evidence is a list, not a single object**, because one
passage per record could only ground one of a record's values: the figure, the due date and the
first-year waiver come from three places, and a record carrying several passages is only honest
if each one says what it is evidence for.

## The pilot

The namespace opens with five jurisdictions chosen to stress the schema, not to cover ground:
**California** (flat minimum collected by a tax board, plus a revenue-scaled companion fee),
**Texas** (margin-based, with a no-tax-due threshold), **Delaware** (a flat annual tax that is
the annual obligation itself), **Tennessee** (a two-component franchise-and-excise regime), and
**Wyoming** (an annual-report license fee scaled on in-state assets, which tests where the
boundary falls). Every structural expectation named here was a hypothesis until the record's own
sources confirmed it, and the schema was expected to change during the pilot; that is what a
pilot is for.

The five are collected. Two things the sources settled, both visible in the records: Wyoming's
license fee **is** a franchise-type levy under the substance test rather than a filing fee, and
Tennessee's franchise-and-excise regime splits — the net-worth franchise tax is recorded, the
income-based excise is not, and each record's `notes` says why. The schema changed once, and not
where the paper expected: `evidence` is a list, because a single record's figure, due date and
first-year waiver are different passages on different pages.

This is not legal or tax advice, and nothing here is a filing instruction. Tax figures move
with legislative sessions; read `lastVerified` before trusting any of them.
