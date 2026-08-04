# US LLC State Requirements Dataset

![Jurisdictions](https://img.shields.io/badge/Jurisdictions-51-blue?style=flat-square)
![Sources](https://img.shields.io/badge/Verified-Official_.gov_sources-blue?style=flat-square)
![Format](https://img.shields.io/badge/Format-JSON-orange?style=flat-square)
![License](https://img.shields.io/badge/License-CC_BY_4.0-purple?style=flat-square)

An open, machine-readable dataset of **US limited liability company formation costs, naming rules, and assumed-name (DBA) filing rules**, covering all 50 states and the District of Columbia.

Every field is hand-verified against official state government sources: statutes, administrative codes, Secretary of State pages, and state fee schedules. Every record carries the sources it was built from and the date it was last checked.

## Why it exists

State-level LLC requirements are public information, but they are not published in any comparable form. Each state uses its own vocabulary, its own fee structure, and its own page layout, and several states publish a statutory fee that is not the amount you actually pay. Comparing 51 jurisdictions means reading 51 different websites.

Aggregations that do exist are mostly lead magnets for formation services, and they go stale quietly. This dataset exists so the comparison can be done from a single machine-readable source with its provenance attached.

## Coverage

| Namespace | Records | What it covers |
|---|---|---|
| `states.json` | 50 states | Formation fee, annual report fee and due date, official links |
| `entitysearch-state-data/states/` | 51 | Agency contact details, addresses, hours, business entity search portals, renewal links, filing facts |
| `name-rules/states/` | 51 | LLC name designators, distinguishability standard, restricted words, name reservation cost, hold period and processing time, naming statutes |
| `dba-rules/states/` | 51 | DBA terminology, filing level (state or county), fees, duration and renewal, publication requirements, protection level, statutes |

"51" means the 50 states plus the District of Columbia (`washington-d-c.json`, `stateAbbr: "DC"`). `states.json` predates the DC addition and covers 50 states only.

Each namespace is additive and independent. Adding one never modifies another, so downstream consumers of one namespace are unaffected by work on the others.

## Methodology

This matters more than the data itself, because a number without provenance is not usable for research.

**Sourcing.** Every field is read from an official source, meaning the government body that publishes the fact: a Secretary of State, a Division of Corporations, a Department of Financial Institutions, a state legislature or law revisor, or the county office that actually takes the filing. Statutes and administrative codes are preferred for rules; the agency's own fee or how-to page is preferred for costs.

Third-party blogs, formation-service pages, and commercial legal aggregators (Justia, FindLaw, and similar statute mirrors) are not accepted as sources, including as corroboration.

**"Official" is a question about the publisher, not the domain suffix.** Most official sources sit on `.gov`, but not all of them do, and a `.gov`-only test would wrongly reject sources this dataset legitimately depends on. These hosts are official and are used deliberately:

| Host | Publisher |
|---|---|
| `sos-corp-search.ark.org` | Arkansas Secretary of State, entity search |
| `www.njportal.com` | New Jersey's official business filing portal |
| `search.sunbiz.org` | Florida Division of Corporations |
| `api.realfile.rtsclients.com` | New Mexico Secretary of State's document host |
| `www.gwinnettcourts.com`, `dksuperiorclerk.com` | Georgia Clerks of Superior Court, the offices that take a Georgia trade-name filing |

**A state's own `state.XX.us` domain counts the same as its `.gov`.** Several states publish from that legacy government namespace instead: `www.sec.state.ma.us`, `www.sos.state.tx.us`, `www.leg.state.nv.us`, `www.sos.state.mn.us`, `mibusinessregistry.lara.state.mi.us`, `secure.sos.state.or.us`, `www.leg.state.fl.us`. It is delegated to the state governments themselves, so a source there is as official as the same state's `.gov`, and 45 URLs in this dataset rely on it. This is deliberately narrower than accepting `.us` as a whole: `.us` is open to general registration, so a host on plain `.us` is official only when it is named as a publisher, the way the Pennsylvania General Assembly's `www.palegis.us` is.

**The one exception, and its conditions.** A few jurisdictions license their statutory code to a commercial publisher and put no free, citable copy of the code text online. There, and only there, a record may cite a verbatim mirror of the statute. The exception holds only when both of these are true:

1. the record carries at least one official source that independently supports the same fact, and
2. the record's own `notes` field states that the jurisdiction publishes no free official copy of its code.

A mirror is never the only source for a fact, and never a substitute for an official page that exists. Where an official copy of the statute is reachable, a mirror is a defect rather than a choice.

**Provenance per record.** Each JSON file carries a `sources` array (`citation`, `title`, `url`, `lastAccessed`) and a `lastVerified` ISO date. `lastVerified` means a human opened the cited sources on that date and confirmed the values, not that an automated check ran.

**Cost basis.** Published filing fees and real out-of-pocket costs differ in several states, because service charges and card fees are added at the point of filing. Where they differ, `nameReservationFee` holds the statutory figure and `nameReservationTotalCost` holds the real cost on the common filing path, with `nameReservationCostBasis` explaining the gap. **Use the total for any cross-state comparison.** Six of the 51 jurisdictions currently charge more than the fee their statute names.

The entity-search namespace carries a single reservation figure, `filingFacts.nameReservation`. It is defined to hold the **real out-of-pocket cost**, mirroring `name-rules`'s `nameReservationTotalCost`, which is the authoritative field. A consumer reading either namespace should therefore quote a price a filer can actually pay.

**One fact, one field.** Where the same fact appears in more than one namespace, one field is defined as authoritative and the others must agree with it, not paraphrase it. A number that a visitor could be asked to pay is held to this strictly: a value that disagrees across namespaces is a bug in this repository, regardless of which copy happens to be right.

**What is excluded.** Expedited-processing surcharges, third-party registered agent fees, county-level publication costs where they vary by county (for example New York and Nebraska), and any pricing from formation services.

### Where the data does not yet meet this standard

The rules above are the standard the dataset is held to, and as of **2026-08-04** parts of it do not meet them. An audit of the whole repository found the following, and a phased remediation is under way. Publishing the gap is preferable to letting a reader assume it is not there.

| Gap | Extent | Status |
|---|---|---|
| `namingStatuteUrl`, `statuteUrl` and some `sources[].url` values point at commercial statute mirrors rather than the state's own publisher | 111 URLs across 23 jurisdictions, in `name-rules` and `dba-rules` only (down from 145 across 29) | being migrated jurisdiction by jurisdiction, each replacement opened and checked against the cited section |
| `restrictedWords` is an empty array where the state's list has not yet been read | 24 of 51 | an empty array here means *not yet researched*, not *the state restricts nothing* |
| Some cited URLs have gone dead since they were last opened | 17 confirmed | being re-sourced; a dead link is never replaced by a guess |

`states.json` and `entitysearch-state-data` carry no mirror citations. Nothing in this table affects a fee amount in `states.json`.

### Known limitations

- Fees and rules change without notice, and a record is only as current as its `lastVerified` date. Check the cited source before relying on a figure.
- `restrictedWords` lists words that are prohibited *or* that require approval from a named regulator. Which of the two applies is described in `notes`, not encoded structurally.
- Some states publish no processing time; `nameReservationProcessingTime` is `null` there rather than estimated.
- County-level DBA regimes are represented at the state level with a `filingLevel` value and a note. The dataset does not enumerate individual counties.
- This is a dataset, not legal advice. Only the relevant state agency can decide an actual filing.

## Usage

Files are served directly from GitHub as raw JSON.

```
https://raw.githubusercontent.com/startupsolellc/us-llc-fees-dataset/main/states.json
https://raw.githubusercontent.com/startupsolellc/us-llc-fees-dataset/main/name-rules/states/{state-slug}.json
https://raw.githubusercontent.com/startupsolellc/us-llc-fees-dataset/main/dba-rules/states/{state-slug}.json
https://raw.githubusercontent.com/startupsolellc/us-llc-fees-dataset/main/entitysearch-state-data/states/{state-slug}.json
```

```javascript
const BASE = "https://raw.githubusercontent.com/startupsolellc/us-llc-fees-dataset/main";

const rules = await fetch(`${BASE}/name-rules/states/georgia.json`).then((r) => r.json());

console.log(rules.nameReservationTotalCost); // 35
console.log(rules.nameReservationDuration);  // "30 days"
console.log(rules.sources[0].url);           // official source it was verified against
```

```python
import json, urllib.request

BASE = "https://raw.githubusercontent.com/startupsolellc/us-llc-fees-dataset/main"

with urllib.request.urlopen(f"{BASE}/name-rules/states/georgia.json") as r:
    rules = json.load(r)

print(rules["nameReservationTotalCost"], rules["nameReservationDuration"])
```

Per-namespace schema documentation lives in `name-rules/README.md`, `dba-rules/README.md`, and `entitysearch-state-data/README.md`. A JSON Schema for the entity-search namespace is at `entitysearch-state-data/schema/state.schema.json`:

```bash
npx ajv-cli validate --strict=false \
  -s entitysearch-state-data/schema/state.schema.json \
  -d 'entitysearch-state-data/states/*.json'
```

## How to cite

The data is licensed **CC BY 4.0**, so attribution is a condition of the licence. Any reasonable citation format is fine.

```
US LLC State Requirements Dataset. StartupSole LLC, 2026.
https://github.com/startupsolellc/us-llc-fees-dataset
```

BibTeX:

```bibtex
@misc{usllcdataset2026,
  title  = {US LLC State Requirements Dataset},
  author = {Dikyurt, Muhammet},
  year   = {2026},
  howpublished = {\url{https://github.com/startupsolellc/us-llc-fees-dataset}}
}
```

GitHub reads `CITATION.cff` in this repository, so the "Cite this repository" button produces the same reference.

When citing a specific figure, cite the record's own `lastVerified` date alongside it. Fees change, and a citation without a date will go stale.

## Licence

Everything published here is data and documentation, licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Use it commercially, modify it, redistribute it; credit the source. Full text in [`LICENSE`](./LICENSE); copyright, attribution wording, and the disclaimer in [`NOTICE`](./NOTICE).

The maintainer's research and verification scripts are not part of this repository. Everything needed to consume the data is here; nothing is withheld that a consumer would need.

> **Note on a previous version of this file.** Earlier revisions declared MIT for everything and asked users to place a backlink to a maintainer website "as a condition of use". That condition was not part of MIT, is not enforceable as written, and requiring a link in exchange for use is a link scheme under search engine guidelines. It has been removed. Attribution is now handled by CC BY 4.0, which asks for credit rather than a specific hyperlink.

## Projects using this dataset

These are built on the namespaces above and are maintained by the same author. They are listed here as downstream consumers and as a disclosure, not as a recommendation.

| Project | What it does | Namespaces used |
|---|---|---|
| [entitysearch.us](https://entitysearch.us) | Business entity search guides for all 50 states, with official portal walkthroughs | `states.json`, `entitysearch-state-data` |
| [businessnamesearch.us](https://businessnamesearch.us) | Pre-formation business name availability checker and naming-rule reference | `name-rules`, `dba-rules`, `entitysearch-state-data` |
| [formation.legal](https://formation.legal) | Guides for non-US founders forming a US LLC | `states.json` |
| [llcrehberi.tr](https://llcrehberi.tr) | Turkish-language US LLC cost calculator and 50-state comparison, with fees converted at the central bank rate on the build date | `states.json` |

Two of these pages are worth naming because they are the widest public views of the data: the [51-jurisdiction name reservation comparison](https://businessnamesearch.us/name-reservation/) and the [nationwide Secretary of State search directory](https://entitysearch.us/resources/secretary-of-state-business-search/).

## Maintainer and disclosure

Maintained by **StartupSole LLC** (Muhammet Dikyurt).

The sites listed above are commercial, and some of them carry affiliate links to formation services. **The dataset itself carries no affiliate links, no tracking, and no commercial content, and using it is not conditioned on linking anywhere.** This disclosure is here so that anyone evaluating the data as a source can weigh it rather than have to discover it.

The dataset is maintained on its own terms: a data error is treated as a bug no matter which project reports it, and corrections from outside contributors are held to the same sourcing standard as the maintainer's own.

## Contributing

Corrections are welcome, and a correction with an official source attached will be merged quickly.

1. Check the state's own Secretary of State, Division of Corporations, or statute page.
2. Update the relevant JSON file, including its `sources` entry and `lastVerified` date.
3. Open a pull request citing the official URL that verifies the change.

Pull requests that change a value without an official source will be asked for one. Third-party blogs and formation-service pages are not accepted as sources.

Found an error but do not want to open a PR? Open an issue with the state, the field, and the official link.
