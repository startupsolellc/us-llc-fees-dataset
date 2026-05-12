# 🇺🇸 US LLC Fees Dataset (2026) - 50 States Formation & Annual Costs JSON

![Updated for 2026](https://img.shields.io/badge/Updated_For-2026-brightgreen?style=flat-square)
![Data Integrity](https://img.shields.io/badge/Verified-Official_.gov_Sources-blue?style=flat-square)
![Format](https://img.shields.io/badge/Format-JSON-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)

A comprehensive, open-source dataset providing highly accurate, machine-readable information on **United States LLC formation fees, recurring annual reporting costs, and state compliance requirements** across all 50 states.

All data is manually verified against official Secretary of State and Department of Revenue `.gov` portals to ensure 100% accuracy.

---

## 🤝 Sponsored By Formation.Legal

This dataset is created, sponsored, and actively maintained by **[Formation.Legal - The Non-US Founder's Guide to US LLCs](https://formation.legal)**.

Are you a non-US resident looking to start a business in the USA? Formation.Legal provides completely free, unbiased guides on how to:
*   Form a US LLC from anywhere in the world.
*   Get an EIN without an ITIN or SSN.
*   Open US business bank accounts (Mercury, Relay, Stripe, Wise).
*   Choose the best state (Wyoming vs. Delaware vs. New Mexico) for your startup.

---

## 🚀 Why This Dataset Exists

Finding accurate, up-to-date LLC fees is surprisingly difficult. Most business blogs hide their fee schedules behind paywalls, use them as lead magnets for expensive registered agent services, or display severely outdated information.

We created this dataset to provide developers, financial researchers, and global entrepreneurs with a **single source of truth** for state fees, verified directly from the source.

---

## 💻 How to Use (JSON API)

You can use this dataset directly in your applications (React, Node.js, Python, Astro, Next.js, etc.) as a free, raw JSON API.

### JavaScript / TypeScript Example

```javascript
// Fetch the live, always-updated 2026 dataset directly from GitHub
const DATASET_URL = "https://raw.githubusercontent.com/startupsolellc/us-llc-fees-dataset/main/states.json";

fetch(DATASET_URL)
  .then(response => response.json())
  .then(data => {
    const wyoming = data.states.WY;
    console.log(`Wyoming Formation Fee: $${wyoming.formation_fee}`);
    console.log(`Wyoming Annual Fee: $${wyoming.annual_report_fee}`);
    console.log(`Official Source: ${wyoming.source_url}`);
  })
  .catch(error => console.error("Error fetching LLC data:", error));
```

---

## 🔗 Attribution & How to Cite (Required)

This dataset is open-sourced under the MIT License, meaning you can use it freely in your commercial SaaS applications, pricing calculators, blogs, or internal tools. 

**However, as a condition of use and to support the open-source maintenance of this data, we kindly require a backlink/attribution.**

If you use this data on a website, blog, or public application, please copy and paste one of the following HTML snippets to give credit:

**Standard Attribution (HTML):**
```html
<p>State fee data provided by <a href="https://formation.legal" target="_blank" rel="noopener">Formation.Legal - US LLC Guide</a>.</p>
```

**Markdown / Blog Attribution:**
```markdown
*Data sourced from the open-source LLC fee dataset maintained by [Formation.Legal](https://formation.legal).*
```

---

## 🗂 Data Schema (`states.json`)

The dataset is structured as a dictionary with 2-letter state abbreviations as keys (e.g., `DE`, `WY`, `NM`).

| Field | Type | Description |
| :--- | :--- | :--- |
| `name` | String | Full name of the state (e.g., "Delaware"). |
| `formation_fee` | Number | The state's one-time base filing fee for Articles of Organization. |
| `annual_report_fee` | Number | The recurring annual report fee, franchise tax, or minimum license fee. |
| `annual_report_due_date` | String | Description of when the recurring fee is due (e.g., "Anniversary month", "April 15"). |
| `official_link` | String | Link to the Secretary of State's portal. |
| `source_url` | String | The exact `.gov` URL where the fee was verified. |
| `last_verified` | String | The YYYY-MM-DD date the fee was last checked against the `.gov` source. |

*(Note: Fees represent state-mandated costs for standard, online domestic LLC filings. Optional expedited fees, third-party registered agent fees, and variable county-level publication fees (like in NY or NE) are excluded from the base numbers.)*

---

## 📦 Extended Dataset: EntitySearch State Data

For sidebar components and enhanced state reference pages, we provide a separate extended dataset in the `entitysearch-state-data/` directory.

### What's Included

| Feature | Description |
|---------|-------------|
| **50 States Complete** | All US states with structured contact info, addresses, and hours |
| **Business Entity Search** | Direct URLs to official state business entity search portals |
| **Filing Facts** | LLC formation fees, annual report requirements, name reservation info |
| **Renewal Links** | Online and paper renewal URLs for each state |
| **Schema Validated** | JSON schema validation available (`entitysearch-state-data/schema/state.schema.json`) |

### Directory Structure

```
entitysearch-state-data/
├── README.md              # Detailed documentation
├── schema/
│   └── state.schema.json  # JSON validation schema
├── states/                # Individual state JSON files
│   ├── alabama.json
│   ├── alaska.json
│   └── ...                # All 50 states
└── assets/
    ├── seals/             # State seal images (WebP)
    └── provider-logos/    # Formation partner logos
```

### Quick Example

```javascript
// Fetch extended state data for sidebar
const stateData = require('./entitysearch-state-data/states/wyoming.json');

console.log(stateData.stateName);              // "Wyoming"
console.log(stateData.businessEntitySearch.url); // Official search portal URL
console.log(stateData.filingFacts.llcFee);      // Formation fee
console.log(stateData.secretaryOfState.website); // SOS website
```

### Validation

Validate all state JSON files against the schema:

```bash
npx ajv-cli validate --strict=false \
  -s entitysearch-state-data/schema/state.schema.json \
  -d 'entitysearch-state-data/states/*.json'
```

---

## 🌐 Built With This Dataset

### EntitySearch.us
**[EntitySearch.us](https://entitysearch.us)** — A comprehensive guide to business entity search for all 50 US states. Each state page features step-by-step screenshots, official portal links, and LLC formation facts powered by this dataset.

```
https://entitysearch.us/texas/
https://entitysearch.us/wyoming/
https://entitysearch.us/delaware/
```

---

## 🛠 Contributing & Data Integrity

**Data integrity is our #1 priority.** We strictly enforce that all PRs must cite official `.gov` sources. 

Did a state change its fee structure? Help us keep the data accurate!
1. Check the state's official Secretary of State / Division of Corporations website.
2. Fork the repository and update `states.json`.
3. Submit a Pull Request including the `.gov` link verifying the change.
