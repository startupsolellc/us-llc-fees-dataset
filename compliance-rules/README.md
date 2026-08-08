# compliance-rules

**Status: draft / proposal. Not published, not part of the dataset yet.**

Per-jurisdiction record of what happens when an LLC misses an annual obligation: the late fee
(flat, percentage or interest), the grace period, and the cost of reinstatement after
administrative dissolution, plus one short note on the process. One JSON file per jurisdiction
in `states/<slug>.json`.

This namespace is additive: it adds no key to `states.json`, `entitysearch-state-data`,
`name-rules`, `dba-rules`, `processing-time` or `tax-rules`, and nothing already published
changes because of it. A consumer that ignores this directory sees exactly the dataset it saw
before.

## Why this namespace exists separately

Penalty structures are the most heterogeneous and least-copied facts in this domain: a state
charges a flat fee, another a monthly percentage, a third adds interest, and several publish
only the reinstatement path. They are scattered across fee schedules, penalty pages and
statutes. This namespace reduces that chaos to one small set of fields per state — deliberately
no penalty matrices, no interest tables, no per-year schedules — because the card a user needs
asks three questions: how much for being late, how long do I have, and what does fixing it cost.

## Scope boundaries

- **Annual obligations of an existing LLC only.** Late fees, grace and reinstatement around
  annual reports and the standing annual obligations of a registered LLC. Formation-filing
  penalties are out of scope.
- **No penalty matrices.** One late-fee shape per record: flat amount, or percentage/interest
  rate, or a published none. Where a state has several shapes, `lateFeeBasis` says so and the
  dominant figure goes in the field, with the rest in `notes`.
- **No interest tables or compounding schedules.** A single monthly rate is data; a table is
  maintenance nobody will keep honest.
- **No court, judgment or criminal fees.**
- **Tax-authority interest stays out unless it is the published late-fee shape for the annual
  obligation.** Where the annual obligation is a tax (Delaware's annual tax, for example), the
  late fee on it belongs here; general income-tax interest does not.
- **This namespace is authoritative for the late fee, grace period and reinstatement fee.**
  Any other mention of those values anywhere else in the dataset is prose, not a value to be
  read.

## Sourcing

Held to the standard in the root `README.md` §Methodology. The publisher is the Secretary of
State, the tax authority, or the statute that sets the penalty. No blogs, no formation-service
pages, no commercial aggregators, including as corroboration.

Every admissible value is bound to a verbatim passage quoted from the cited page (`evidence`).
`null` means not yet researched and is always preferred to a plausible guess. A published "no
late fee" is a researched `none`, not an absent field.

## Field dictionary

### Identity

| Field | Type | Notes |
|---|---|---|
| `stateName`, `stateAbbr`, `stateSlug` | string | Same conventions as the other namespaces; DC uses `district-of-columbia` |

### `compliance`

| Field | Type | Notes |
|---|---|---|
| `lateFeeUsd` | number \| null | Flat late fee in USD; null when the state uses a rate or publishes none |
| `lateFeeRatePercentPerMonth` | number \| null | Monthly percentage or interest rate; the only rate field, by design |
| `lateFeeBasis` | enum \| null | `flat` · `percentage` · `interest` · `mixed` · `none` · `unpublished` — what the state actually publishes |
| `gracePeriodDays` | integer \| null | Published grace before the late fee applies; null when none is published |
| `reinstatementFeeUsd` | number \| null | The fee to reinstate after administrative dissolution, including any per-year component folded in; `reinstatementNote` says how |
| `reinstatementNote` | string \| null | One short sentence: what reinstatement requires (delinquent reports, per-year fees, time window) |
| `evidence` | evidence[] | One verbatim passage per value |

### Record plumbing

`notes`, `needsReview`, `sources[]` (`citation`, `title`, `url`, `type`, `lastAccessed`) and
`lastVerified` carry their usual meaning from the other draft namespaces.

## The pilot

The namespace opens with five jurisdictions chosen to stress the schema, not to cover ground.
Hypothesis candidates: **Delaware** (flat fee plus a monthly rate), **New York** (flat), **Texas**
(rate-shaped), **South Dakota** (published reinstatement schedule) and **Washington** (per-year
fee plus a flat penalty). Every expectation here is a hypothesis until the record's own sources
confirm it; the schema is expected to change during the pilot.

This is not legal advice, and nothing here is a filing instruction. Penalties move with
legislative sessions; read `lastVerified` before trusting any of them.
