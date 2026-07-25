# US LLC State Requirements Dataset

![Jurisdictions](https://img.shields.io/badge/Jurisdictions-51-blue?style=flat-square)
![Sources](https://img.shields.io/badge/Verified-Official_.gov_sources-blue?style=flat-square)
![Format](https://img.shields.io/badge/Format-JSON-orange?style=flat-square)
![Data license](https://img.shields.io/badge/Data-CC_BY_4.0-purple?style=flat-square)
![Code license](https://img.shields.io/badge/Code-MIT-purple?style=flat-square)

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

**Sourcing.** Every field is read from an official state government source. Statutes and administrative codes are preferred for rules, and the agency's own fee or how-to page is preferred for costs. Third-party blogs, formation-service pages, and aggregator sites are not accepted as sources, including as corroboration.

**Provenance per record.** Each JSON file carries a `sources` array (`citation`, `title`, `url`, `lastAccessed`) and a `lastVerified` ISO date. `lastVerified` means a human opened the cited sources on that date and confirmed the values, not that an automated check ran.

**Cost basis.** Published filing fees and real out-of-pocket costs differ in several states, because service charges and card fees are added at the point of filing. Where they differ, `nameReservationFee` holds the statutory figure and `nameReservationTotalCost` holds the real cost on the common filing path, with `nameReservationCostBasis` explaining the gap. **Use the total for any cross-state comparison.** Six of the 51 jurisdictions currently charge more than the fee their statute names.

**What is excluded.** Expedited-processing surcharges, third-party registered agent fees, county-level publication costs where they vary by county (for example New York and Nebraska), and any pricing from formation services.

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

- **Data** (all JSON files, schemas, and namespace documentation): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Use it commercially, modify it, redistribute it; credit the source. Full text in [`LICENSE`](./LICENSE).
- **Scripts** (`scripts/`): MIT. Full text in [`scripts/LICENSE`](./scripts/LICENSE).

Copyright, attribution wording, and the disclaimer are in [`NOTICE`](./NOTICE).

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
