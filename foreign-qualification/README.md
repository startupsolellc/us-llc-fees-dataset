# foreign-qualification

**Status: draft / proposal. Not published, not part of the dataset yet.**

Per-jurisdiction record of what it costs and what it takes to register an existing LLC from
another state: the registration fee, the official form, the agency that takes the filing, and
the ongoing obligations that follow. One JSON file per jurisdiction in `states/<slug>.json`.

This namespace is additive: it adds no key to `states.json`, `entitysearch-state-data`,
`name-rules`, `dba-rules`, `processing-time` or `tax-rules`, and nothing already published
changes because of it. A consumer that ignores this directory sees exactly the dataset it saw
before.

## Why this namespace exists separately

Foreign qualification is the same filing event as formation but with its own fee, its own form
and its own follow-on obligations, and it is the one place an existing LLC's owner meets a new
state's bureaucracy without forming a new entity. The root dataset answers "what does this state
charge to form"; this namespace answers "what does this state charge to let an LLC from
elsewhere do business here".

## Scope boundaries

- **The registration filing only.** The fee and form to register a foreign LLC. Amendments,
  withdrawals and dissolutions are out of scope.
- **No "doing business" advice.** Whether a particular activity requires registration is a legal
  question for the filer; the record carries the state's published fee and form, not an opinion
  on when they are triggered.
- **Registered-agent eligibility rules stay where they are.** `agent-rules` is authoritative for
  who may be an agent. This namespace records only the standing requirement to have one, inside
  `ongoingObligationsNote`, as prose.
- **County-level costs are out of scope.** Where a foreign registration also triggers local
  costs, they belong to the county layer, not here.
- **This namespace is authoritative for the foreign registration fee and the official form.**
  Any other mention of a foreign qualification fee anywhere else in the dataset is prose, not a
  value to be read.

## Sourcing

Held to the standard in the root `README.md` §Methodology. The publisher is the Secretary of
State or the agency that takes the filing; the fee usually sits on that agency's own fee
schedule. No blogs, no formation-service pages, no commercial aggregators, including as
corroboration.

Every admissible value is bound to a verbatim passage quoted from the cited page (`evidence`).
`registrationFeeUsd` holds the real out-of-pocket cost on the common filing path, and `feeBasis`
explains the gap when it differs from the statutory figure. `null` means not yet researched and
is always preferred to a plausible guess.

## Field dictionary

### Identity

| Field | Type | Notes |
|---|---|---|
| `stateName`, `stateAbbr`, `stateSlug` | string | Same conventions as the other namespaces; DC uses `district-of-columbia` |

### `foreignQualification`

| Field | Type | Notes |
|---|---|---|
| `registrationFeeUsd` | number \| null | Real out-of-pocket cost on the common filing path (online or paper); `feeBasis` names the path |
| `feeBasis` | string | What the figure covers and why it differs from a statutory fee, if it does |
| `formName` | string | The official form's name or number, verbatim |
| `formUrl` | string \| null | The official form page or fee schedule the form was read from |
| `filedWith` | string \| null | The agency that takes the filing, verbatim |
| `ongoingObligationsNote` | string \| null | One short sentence: what the LLC must do after registering (annual report, agent maintenance, recurring fees) |
| `evidence` | evidence[] | One verbatim passage per value |

### Record plumbing

`notes`, `needsReview`, `sources[]` (`citation`, `title`, `url`, `type`, `lastAccessed`) and
`lastVerified` carry their usual meaning from the other draft namespaces.

## The pilot

The namespace opens with five jurisdictions chosen to stress the schema, not to cover ground.
Hypothesis candidates: **California** (online-only application), **New York** (paper, higher
fee), **Texas**, **Delaware** and **Georgia**. Every expectation here is a hypothesis until the
record's own sources confirm it; the schema is expected to change during the pilot.

This is not legal advice, and nothing here is a filing instruction. Fees move with legislative
sessions; read `lastVerified` before trusting any of them.
