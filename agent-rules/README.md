# agent-rules

**Status: draft / proposal. Not published, not part of the dataset yet.**

Per-jurisdiction record of who may serve as an LLC's registered agent: whether the LLC itself
may be its own agent, whether a commercial mail receiving agency (CMRA) address is acceptable,
and what address rule applies. One JSON file per jurisdiction in `states/<slug>.json`.

This namespace is additive: it adds no key to `states.json`, `entitysearch-state-data`,
`name-rules`, `dba-rules`, `processing-time` or `tax-rules`, and nothing already published
changes because of it. A consumer that ignores this directory sees exactly the dataset it saw
before.

## Why this namespace exists separately

Registered-agent rules are statute-level facts that formation sites copy loosely and
contradict each other on: the same state is described as "you can be your own agent" by one
service and "an entity cannot serve as its own agent" by another. The distinction that matters
to a filer is narrow — the LLC itself, a member, another entity, a CMRA — and it is exactly the
distinction this namespace records, one small set of fields per state.

## Scope boundaries

- **Eligibility rules only.** Who or what may be the agent, and what address the agent's office
  must have. Commercial registered-agent pricing and services are out of scope.
- **No filing mechanics.** Acceptance of service, service on the Secretary of State as fallback,
  and court process rules are out of scope.
- **Contact data stays where it is.** `entitysearch-state-data` remains authoritative for the
  agencies' own contact details, addresses and hours.
- **This namespace is authoritative for registered-agent eligibility.** Any other mention of who
  may be an agent anywhere else in the dataset is prose, not a value to be read.

## Sourcing

Held to the standard in the root `README.md` §Methodology. The source is the registered-agent
provision of the state's LLC act or the agency's own registration guidance; the statute is
preferred. No blogs, no formation-service pages, no commercial aggregators, including as
corroboration.

Every admissible value is bound to a verbatim passage quoted from the cited page (`evidence`).
`false` is a researched finding and requires a passage from the provision that would have said
so. `null` means not yet researched and is always preferred to a plausible guess.

## Field dictionary

### Identity

| Field | Type | Notes |
|---|---|---|
| `stateName`, `stateAbbr`, `stateSlug` | string | Same conventions as the other namespaces; DC uses `district-of-columbia` |

### `registeredAgent`

| Field | Type | Notes |
|---|---|---|
| `llcCanBeOwnAgent` | boolean \| null | Whether the LLC itself may serve as its own registered agent. `false` needs evidence from the provision that would have said so |
| `cmraAllowed` | boolean \| null | Whether a commercial mail receiving agency (CMRA) may serve as the registered office or address |
| `addressRule` | string \| null | The address requirement in the state's own words: physical street address, P.O. box policy, business-office requirement |
| `evidence` | evidence[] | One verbatim passage per value |

### Record plumbing

`notes`, `needsReview`, `sources[]` (`citation`, `title`, `url`, `type`, `lastAccessed`) and
`lastVerified` carry their usual meaning from the other draft namespaces.

## The pilot

The namespace opens with five jurisdictions chosen to stress the schema, not to cover ground.
Hypothesis candidates: **Texas** (reported explicit prohibition on the entity serving as its own
agent), **Delaware** (reported entity-permissive provision), **California**, **New York** and
**Georgia**. Every expectation here is a hypothesis until the record's own sources confirm it;
the schema is expected to change during the pilot.

This is not legal advice, and nothing here is a filing instruction. Statutes move with
legislative sessions; read `lastVerified` before trusting any of them.
