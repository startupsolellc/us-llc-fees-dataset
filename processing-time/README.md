# processing-time

**Status: published. 51 of 51 jurisdictions, last verified 2026-08-08.**

Per-jurisdiction record of how long a state takes to process an LLC formation filing, and what
it costs to make that faster. One JSON file per jurisdiction in `states/<slug>.json`.

This namespace is additive: it adds no key to `states.json`, `entitysearch-state-data`,
`name-rules` or `dba-rules`, and nothing already published changes because of it. A consumer
that ignores this directory sees exactly the dataset it saw before.

---

## Why this namespace exists separately

The fact "how long does it take" is not one fact. It is two, and they behave nothing alike:

| | **Expedite tiers** | **Standard processing time** |
|---|---|---|
| Example | NY: 24-hour, $25 per document | CA: "online filings being reviewed as of 08/04/2026" |
| Where the state publishes it | Fee schedule, service-options page, sometimes statute | A queue-status page updated continuously |
| How often it changes | Years | Days |
| Is it a promise? | Yes — a guaranteed turnaround the state sells | No — an observation of a backlog |
| Can it carry a `lastVerified` honestly? | Yes | Only as *observed on that date*, never as *current* |

Folding both into one field would make half of every record wrong within a month and would
quietly erode the meaning of `lastVerified` across the repository. So the schema keeps them in
two objects with different contracts, and the standard-time object is explicitly framed as an
observation, never as a current value.

## Scope boundaries

- **Formation filings only.** Time-to-process for the Articles/Certificate of Organization.
  Amendments, dissolutions, and foreign qualification are out of scope for now.
- **Name reservation processing time stays where it is.** `name-rules`'s
  `nameReservationProcessingTime` is authoritative for that fact and this namespace does not
  restate it. One fact, one field.
- **This namespace is authoritative for expedited-service fees and turnarounds.** Any other
  mention of them anywhere in the dataset is prose, not a value to be read.
- **No formation-service pricing.** An expedite fee is what the state charges. What a filing
  company charges to click the expedite box is not data.
- **Registered-agent, shipping and card fees are out of scope**, the same way they are for the
  fee namespaces.

## Sourcing

Held to the same standard as the rest of the repository: the published policy in the root
`README.md` §Methodology. Every figure is read from the agency's own fee schedule, service-options
page, or the statute that sets the fee. No blogs, no formation-service pages, no commercial
aggregators — including as corroboration.

**The one conflict is resolved.** The root README's *What is excluded* list used to read
"Expedited-processing surcharges [...] are excluded." That was written about cost basis — an
expedite surcharge is not folded into a fee or total-cost field — but read as an unqualified
exclusion, this namespace would have contradicted it. The heading is now *What is excluded from
the fee figures*, and the sentence says explicitly that expedite surcharges are excluded from the
cost basis, not from the repository, and are recorded as their own value where recorded at all.

## Field dictionary

### Identity

| Field | Type | Notes |
|---|---|---|
| `stateName`, `stateAbbr`, `stateSlug` | string | Same conventions as the other namespaces |

### `expedite` — the stable half

| Field | Type | Notes |
|---|---|---|
| `offered` | bool \| null | `false` is a real finding (state offers no expedite); `null` means not yet researched |
| `appliesToLlcFormation` | bool \| null | Some schedules are written for corporations and cover LLC filings by reference — say which, in `notes` |
| `feeIsPerDocument` | bool \| null | NY charges per document; matters for a multi-document submission |
| `chargedIfRejected` | bool \| null | NY charges the expedite fee whether or not the document is accepted. Load-bearing for a filer |
| `tiers[]` | array | One entry per purchasable tier |
| `tiers[].tierName` | string | The state's own label, verbatim ("Same Day Filing Service (Class B)") |
| `tiers[].turnaround` | string | The state's own commitment, verbatim |
| `tiers[].feeUsd` | number \| null | Exact fee. `null` only when the state publishes a range |
| `tiers[].feeUsdMin` / `feeUsdMax` | number \| null | Used **only** when the published fee is a range that depends on document type. Never a guess at the midpoint |
| `tiers[].cutoff` | string \| null | Submission deadline that makes the tier achievable |
| `tiers[].channels[]` | array of `"online" \| "mail" \| "in-person" \| "fax"` | Several tiers are drop-off only; a filer needs to know before paying |
| `tiers[].note` | string \| null | Anything that qualifies the tier |

### `standardProcessing` — the volatile half

| Field | Type | Notes |
|---|---|---|
| `isPublished` | bool | `false` means the state publishes no standard time — not that it is instant |
| `basis` | `"queue-date"` \| `"stated-range"` \| `"guarantee"` \| null | **How the state expresses it.** CA publishes a queue date, not a duration. Encoding a queue date as "≈2 days" would be a derived number the source never stated |
| `queueAsOfOnline` / `queueAsOfMail` | ISO date \| null | For `basis: "queue-date"` — the filing date the office is currently working through |
| `onlineBusinessDays` / `mailBusinessDays` | `{min, max}` \| null | For `basis: "stated-range"` only |
| `statement` | string \| null | The state's wording, verbatim. The primary artifact; the parsed fields are convenience |
| `sourceUrl` | string \| null | The queue page itself |
| `observedOn` | ISO date | **Not** `lastVerified`. The date a human read this value. Consumers must render it as "as observed on X" |
| `volatile` | const `true` | A literal in the schema, so no consumer can read this object without meeting the word |

### Provenance

`sources[]` (`citation`, `title`, `url`, `lastAccessed`) and `notes` carry their usual meaning.
`lastVerified` covers the `expedite` object; it deliberately does **not** cover
`standardProcessing`, which carries its own `observedOn`.

**Every value here is bound to the words it was read from.** Each tier carries an `evidence`
object — a passage quoted from the cited page, plus that page's URL — and each quotation is
checked mechanically to occur in the page as retrieved. A quotation that does not occur is a
rejected value, not a warning. `lastVerified` is the date of that retrieval and that check.

This is a deliberately different promise from "someone looked at it", and a stronger one: a
reader cannot audit whether a person opened a page, but anyone can re-fetch these pages and
re-run the substring check. It is also not a complete one — grounding proves a passage is on the
page, not that it was taken from the right part of it, which is why quotations for queue dates
carry their section heading and row label rather than a bare date.

`needsReview` (string \| null) records a field that could not be sourced and why — see
`states/connecticut.json`, where the host that publishes the expedited-service document accepts no
connection on any route tried, and every field is left unfilled rather than guessed.

---

## Maintenance model

Two cadences, because the two halves decay at different rates.

**Tier A — `expedite`, on the existing state rotation.** When a state comes up in the normal
verification batch, its expedite schedule is re-read from the agency's fee page alongside
everything else being checked for that state. Changes here are rare and announced (a fee change
follows a statute or a regulation), so the existing rotation is the right frequency and this adds
one page per state to a visit that is already happening.

**Tier B — `standardProcessing`, never claimed as current.** A queue page that moves daily cannot
be made accurate by checking it quarterly, so the schema does not pretend otherwise: the value is
published as an observation with `observedOn`, and the honest consumer-facing rendering is
"as observed on 2026-08-06", with `sourceUrl` for the live figure. Refreshing it on the state
rotation is a bonus, not a correctness requirement.

**Proposed machine checks**, in the spirit of the existing gate — each one catches a failure a
human reviewer reliably misses:

1. `sourceUrl` and every `sources[].url` resolves (a dead fee page is the first sign of a
   reorganised schedule).
2. `expedite.offered: true` implies `tiers[]` is non-empty; `offered: false` implies `notes`
   explains it. Silent emptiness is the failure mode that made `restrictedWords` ambiguous.
3. `feeUsd` and the `feeUsdMin`/`feeUsdMax` pair are mutually exclusive — a record may not carry
   both a point value and a range for the same tier.
4. `standardProcessing.observedOn` older than N days downgrades the record to *stale* in the
   published table rather than failing the gate. A stale observation that says so is fine; one
   that presents itself as current is not.
5. `basis` and the populated fields agree: `queue-date` populates `queueAsOf*`, `stated-range`
   populates `*BusinessDays`. This is what stops a queue date from being silently rewritten as a
   duration.

Checks 1–3 and 5 are cheap and deterministic. Check 4 needs a policy decision on N.

### Deferred, on purpose — do not lose

Seven `entitysearch` records mention expedited service inside free-text `*Notes` fields
(`filingFacts.llcFeeNotes`, `filingFacts.nameReservationNotes`, `renewals.notes`). Five of them
only state that such a service exists, which cannot conflict with anything. **Two carry an actual
figure** — Illinois (`24-hour online service $250`, `paper expedited +$100`, `10 business days`)
and Arizona (`expedited $85`) — and those two will silently disagree with this namespace the day
either state changes its schedule.

Deliberately **not** acted on: the prose stays as written, and no cross-namespace check is added
for now. The exposure is two records, the figures sit in explanatory notes rather than in fields a
consumer reads as values, and nothing downstream renders them. Revisit if this namespace is ever
published or consumed alongside `entitysearch`, in which case the cheap fix is a check that flags
a dollar amount near "expedit" in those note fields when it disagrees with the state's
processing-time record.

## Records

`states/` currently holds all 51 jurisdictions. Three of them carry no purchasable value yet and say
so in `needsReview` rather than guessing: two are unreachable from the collecting network and one is
readable in statute and dark at the agency. The table below is a **selection, not the
full list**: it names the record that first forced each shape the model had to absorb, which is why
a state appears here at all. States that arrived later and exercised a shape already covered are
not listed.

| State | What it exercises |
|---|---|
| Delaware | Four tiers, two published as a **range** rather than a point fee |
| California | `basis: "queue-date"` — no duration published at all; preclearance as a prerequisite for the fastest tier |
| New Jersey | Four tiers, none of them available online; two adjacent fee blocks (LLC and LLP) that are identical in price, so the quotation must be anchored to tell them apart |
| Virginia | A tier priced as "$50 or $100" — a range the agency does not resolve on that page; paper filings excluded from expediting entirely |
| North Carolina | Expedite as a **guarantee of a decision**, not of acceptance: the fee is satisfied by a rejection too |
| Maryland | One channel only — an in-person drop box at $425 — while the state's online expedite fee lives elsewhere and is therefore absent |
| Hawaii | A flat per-document price attached to the fee schedule with **no turnaround stated at all** |
| Florida | The first researched **"no"** — the Division answers the question on its own FAQ, so the absence is evidenced rather than assumed |
| Michigan | The same turnaround priced **differently by document type**: forming an entity costs half what touching an existing one does |
| Pennsylvania | The steepest ladder in the set, where the cut-off times rather than the clock are what separate the tiers |
| Iowa | Priced in **days** rather than hours, very cheap at the bottom, and **not charged when a filing is rejected** — the inverse of North Carolina |
| Texas | Three tiers, and the reason the collection method changed: the first pass recorded the state as honest-empty because every fee page returned 403, and the same URLs opened on a different network route. A block is a property of the (host, route) pair, not of the host |
| Massachusetts | A state whose "expedite fee" prices a **channel, not a turnaround**: a surcharge on fax and electronic filings scaled to the transaction cost, with no time commitment anywhere in the schedule — recorded as an evidenced "no" rather than a tier |
| Louisiana | Two general-purpose tiers in the fee schedule's closing "Special handling" section ($50 while-you-wait, $30 within 24 hours); the page itself announces a statutory fee increase effective 2026-10-01 |
| Kentucky | An evidenced "no" resting on three pages read in full — the FAQ that answers the turnaround question, the complete fee list, and the fee statute — and the first record with a populated `standardProcessing` (`stated-range`: usually same day, up to three business days) |
| Arkansas | Same shape as Kentucky, with the inverse lever made visible: the state **discounts online filings** below paper rather than surcharging speed |
| Connecticut | Honest-empty by **network** rather than by silence: the host that publishes the expedited-service document answers no route from the collection machine, and the reachable statutes establish no fee |
| West Virginia | Four tiers across **two official documents that disagree** — the printed fee schedule lists three, the order form the same page links offers five, and one of them appears nowhere else. Both are current, so every tier is carried with the document it came from named |
| Utah | Priced and undescribed, plus the trap that gives the rule its name: a **second $75** on a different page, for a different product, with a turnaround the filing tier does not have |
| Nevada | A fee schedule printed as two columns, so the label and its price are contiguous only across a whole block; the quotation is the block, and the positional mapping is corroborated before it is trusted rather than assumed |
| New Hampshire | **Priced without a promise**: the statute sells expedited service by the batch and no official page anywhere states what it buys, so `turnaround` is null on a documented silence rather than on an unread page |
| Washington | The fullest ladder, and the only one priced by an **administrative rule** rather than an agency page — which is also where the standard processing figure lives, stated for one channel only |
| Ohio | The ladder printed on the **face of the filing form** rather than on any fee schedule, which is what makes its application to an LLC formation a matter of position rather than inference |
