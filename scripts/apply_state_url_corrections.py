#!/usr/bin/env python3
"""Apply curated official URL corrections to state data files.

The generated state files initially reused fee URLs for multiple roles. This
script separates official agency/division homepages, public entity search URLs,
and fee/annual-report source URLs.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = REPO_ROOT / "entitysearch-state-data" / "states"
ROOT_DATA_PATH = REPO_ROOT / "states.json"
TODAY = date.today().isoformat()


URLS: dict[str, dict[str, Any]] = {
    "AL": {
        "agency": "Alabama Secretary of State Business Entities Division",
        "website": "https://www.sos.alabama.gov/business-entities",
        "entity_search": "https://www.sos.alabama.gov/government-records/business-entity-records",
        "fee_sources": ["https://www.sos.alabama.gov/business-entities/fees"],
    },
    "AK": {
        "agency": "Alaska Division of Corporations, Business and Professional Licensing",
        "website": "https://www.commerce.alaska.gov/web/cbpl/corporations",
        "entity_search": "https://www.commerce.alaska.gov/cbp/main/search/entities",
        "fee_sources": ["https://www.commerce.alaska.gov/web/cbpl/Corporations/FormsFees.aspx"],
    },
    "AZ": {
        "agency": "Arizona Corporation Commission Corporations Division",
        "website": "https://www.azcc.gov/corporations",
        "entity_search": "https://arizonabusinesscenter.azcc.gov/businesssearch",
        "fee_sources": ["https://www.azcc.gov/corporations/fee-and-payment-info"],
    },
    "AR": {
        "agency": "Arkansas Secretary of State Business and Commercial Services",
        "website": "https://www.sos.arkansas.gov/business-commercial-services-bcs",
        "entity_search": "https://www.sos.arkansas.gov/corps/search_all.php",
        "fee_sources": [
            "https://www.sos.arkansas.gov/business-commercial-services-bcs/forms-fees",
            "https://www.sos.arkansas.gov/business-commercial-services-bcs/for-current-businesses",
        ],
    },
    "CA": {
        "agency": "California Secretary of State Business Programs Division",
        "website": "https://www.sos.ca.gov/business-programs/business-entities",
        "entity_search": "https://bizfileonline.sos.ca.gov/search/business",
        "fee_sources": [
            "https://bizfile.sos.ca.gov/forms/fees",
            "https://www.ftb.ca.gov/file/business/types/limited-liability-company/index.html",
        ],
    },
    "CO": {
        "agency": "Colorado Secretary of State Business Division",
        "website": "https://www.coloradosos.gov/pubs/business/businessHome.html",
        "entity_search": "https://www.coloradosos.gov/ucc/pages/biz/bizSearch.xhtml",
        "fee_sources": ["https://www.coloradosos.gov/pubs/info_center/fees/business.html"],
    },
    "CT": {
        "agency": "Connecticut Secretary of the State Business Services Division",
        "website": "https://business.ct.gov",
        "entity_search": "https://service.ct.gov/business/s/onlinebusinesssearch",
        "fee_sources": ["https://portal.ct.gov/sots/business-services/fees/business-entity-filing-fees"],
    },
    "DE": {
        "agency": "Delaware Division of Corporations",
        "website": "https://corp.delaware.gov",
        "entity_search": "https://icis.corp.delaware.gov/eCorp/EntitySearch/NameSearch.aspx",
        "fee_sources": [
            "https://corp.delaware.gov/fee/",
            "https://corp.delaware.gov/alt-entitytaxinstructions/",
        ],
    },
    "FL": {
        "agency": "Florida Division of Corporations",
        "website": "https://dos.fl.gov/sunbiz/",
        "entity_search": "https://search.sunbiz.org/Inquiry/CorporationSearch/ByName",
        "fee_sources": ["https://dos.fl.gov/sunbiz/forms/fees/llc-fees/"],
    },
    "GA": {
        "agency": "Georgia Secretary of State Corporations Division",
        "website": "https://sos.ga.gov/corporations-division-georgia-secretary-states-office",
        "entity_search": "https://ecorp.sos.ga.gov/BusinessSearch",
        "fee_sources": ["https://sos.ga.gov/how-to-guide/how-guide-register-domestic-entity"],
    },
    "HI": {
        "agency": "Hawaii Business Registration Division",
        "website": "https://cca.hawaii.gov/breg/",
        "entity_search": "https://hbe.ehawaii.gov/documents/search.html",
        "fee_sources": ["https://cca.hawaii.gov/breg/registration/dllc/fees/"],
    },
    "ID": {
        "agency": "Idaho Secretary of State Business Services",
        "website": "https://sosbiz.idaho.gov",
        "entity_search": "https://sosbiz.idaho.gov/search/business",
        "fee_sources": ["https://sos.idaho.gov/business-services-resources/"],
    },
    "IL": {
        "agency": "Illinois Secretary of State Business Services",
        "website": "https://www.ilsos.gov/departments/business_services/home.html",
        "entity_search": "https://apps.ilsos.gov/businessentitysearch/",
        "fee_sources": ["https://www.ilsos.gov/departments/business_services/organization/llc.html"],
    },
    "IN": {
        "agency": "Indiana Secretary of State Business Services Division",
        "website": "https://inbiz.in.gov",
        "entity_search": "https://bsd.sos.in.gov/publicbusinesssearch",
        "fee_sources": ["https://inbiz.in.gov/start-business/fee-schedule"],
    },
    "IA": {
        "agency": "Iowa Secretary of State Business Services",
        "website": "https://sos.iowa.gov/business-services",
        "entity_search": "https://sos.iowa.gov/search/business/search.aspx",
        "fee_sources": ["https://sos.iowa.gov/businesses/business-entity-forms-and-fees"],
    },
    "KS": {
        "agency": "Kansas Secretary of State Business Services",
        "website": "https://sos.ks.gov/businesses/businesses.html",
        "entity_search": "https://www.kansas.gov/bess/flow/main?execution=e1s1",
        "fee_sources": [
            "https://www.sos.ks.gov/forms/business_services/DL.pdf",
            "https://www.sos.ks.gov/forms/business_services/lc.pdf",
        ],
    },
    "KY": {
        "agency": "Kentucky Secretary of State Business Services",
        "website": "https://www.sos.ky.gov/bus/Pages/default.aspx",
        "entity_search": "https://sosbes.sos.ky.gov/BusSearchNProfile/Search.aspx",
        "fee_sources": ["https://www.sos.ky.gov/bus/business-filings/Pages/Fees.aspx"],
    },
    "LA": {
        "agency": "Louisiana Secretary of State Commercial Division",
        "website": "https://www.sos.la.gov/BusinessServices",
        "entity_search": "https://coraweb.sos.la.gov/commercialsearch/commercialsearch.aspx",
        "fee_sources": ["https://www.sos.la.gov/BusinessServices/FileBusinessDocuments/GetFormsAndFeeSchedule"],
    },
    "ME": {
        "agency": "Maine Bureau of Corporations, Elections and Commissions",
        "website": "https://www.maine.gov/sos/corporations-commissions/corporations",
        "entity_search": "https://apps3.web.maine.gov/nei-sos-icrs/ICRS?MainPage=x",
        "fee_sources": ["https://www.maine.gov/sos/corporations-commissions/i-need-a-business-form/limited-liability-company-forms"],
    },
    "MD": {
        "agency": "Maryland Department of Assessments and Taxation",
        "website": "https://dat.maryland.gov/Pages/default.aspx",
        "entity_search": "https://egov.maryland.gov/BusinessExpress/EntitySearch",
        "fee_sources": ["https://dat.maryland.gov/businesses/Pages/Fees-and-Payment-Information.aspx"],
    },
    "MA": {
        "agency": "Massachusetts Secretary of the Commonwealth Corporations Division",
        "website": "https://www.sec.state.ma.us/divisions/corporations/corporations.htm",
        "entity_search": "https://corp.sec.state.ma.us/CorpWeb/CorpSearch/CorpSearch.aspx",
        "fee_sources": ["https://www.sec.state.ma.us/divisions/corporations/fees.htm"],
    },
    "MI": {
        "agency": "Michigan Corporations Division",
        "website": "https://www.michigan.gov/lara/bureau-list/cscl/corps",
        "entity_search": "https://cofs.lara.state.mi.us/SearchApi/Search/Search",
        "fee_sources": ["https://www.michigan.gov/lara/bureau-list/cscl/corps"],
    },
    "MN": {
        "agency": "Minnesota Secretary of State Business Services",
        "website": "https://www.sos.state.mn.us/business-liens/",
        "entity_search": "https://mblsportal.sos.state.mn.us/Business/Search",
        "fee_sources": ["https://www.sos.state.mn.us/media/5969/a-guide-to-starting-a-small-business-in-minnesota.pdf"],
    },
    "MS": {
        "agency": "Mississippi Secretary of State Business Services",
        "website": "https://www.sos.ms.gov/business-services",
        "entity_search": "https://corp.sos.ms.gov/corp/portal/c/page/corpBusinessIdSearch/portal.aspx",
        "fee_sources": ["https://www.sos.ms.gov/content/documents/Business/Services%20%26%20Fees%20Document.pdf"],
    },
    "MO": {
        "agency": "Missouri Secretary of State Corporations Division",
        "website": "https://www.sos.mo.gov/business/corporations",
        "entity_search": "https://bsd.sos.mo.gov/BusinessEntity/BESearch.aspx?SearchType=0",
        "fee_sources": ["https://www.sos.mo.gov/business/corporations/forms"],
    },
    "MT": {
        "agency": "Montana Secretary of State Business Services",
        "website": "https://biz.sosmt.gov/",
        "entity_search": "https://biz.sosmt.gov/search/business",
        "fee_sources": ["https://sosmt.gov/business/fees/"],
    },
    "NE": {
        "agency": "Nebraska Secretary of State Business Services",
        "website": "https://sos.nebraska.gov/business-services",
        "entity_search": "https://www.nebraska.gov/sos/corp/corpsearch.cgi",
        "fee_sources": ["https://sos.nebraska.gov/business-services/forms-and-fees"],
    },
    "NV": {
        "agency": "Nevada Secretary of State Business Center",
        "website": "https://www.nvsos.gov/sos/businesses",
        "entity_search": "https://esos.nv.gov/EntitySearch/OnlineEntitySearch",
        "fee_sources": ["https://www.nvsos.gov/sos/businesses/commercial-recordings/forms-fees"],
    },
    "NH": {
        "agency": "New Hampshire Secretary of State Corporation Division",
        "website": "https://sos.nh.gov/corporation-division",
        "entity_search": "https://quickstart.sos.nh.gov/online/BusinessInquire",
        "fee_sources": ["https://sos.nh.gov/corporation-ucc-securities/corporation/online-business-services"],
    },
    "NJ": {
        "agency": "New Jersey Division of Revenue and Enterprise Services",
        "website": "https://www.nj.gov/treasury/revenue/",
        "entity_search": "https://www.njportal.com/DOR/BusinessNameSearch/Search/BusinessName",
        "fee_sources": ["https://www.nj.gov/treasury/revenue/fees.shtml"],
    },
    "NM": {
        "agency": "New Mexico Secretary of State Business Services",
        "website": "https://www.sos.nm.gov/business-services/",
        "entity_search": "https://portal.sos.state.nm.us/BFS/online/CorporationBusinessSearch",
        "fee_sources": ["https://www.sos.nm.gov/business-services/"],
    },
    "NY": {
        "agency": "New York Department of State Division of Corporations",
        "website": "https://dos.ny.gov/division-corporations-state-records-and-uniform-commercial-code",
        "entity_search": "https://apps.dos.ny.gov/publicInquiry/",
        "fee_sources": ["https://dos.ny.gov/forming-limited-liability-company-new-york"],
    },
    "NC": {
        "agency": "North Carolina Secretary of State Business Registration",
        "website": "https://www.sosnc.gov/divisions/business_registration",
        "entity_search": "https://www.sosnc.gov/online_services/search/by_title/_Business_Registration",
        "fee_sources": ["https://www.sosnc.gov/divisions/business_registration"],
    },
    "ND": {
        "agency": "North Dakota Secretary of State Business Services",
        "website": "https://www.sos.nd.gov/business/business-services",
        "entity_search": "https://firststop.sos.nd.gov/search/business",
        "fee_sources": ["https://www.sos.nd.gov/business/business-services/business-structures/limited-liability-company-llc"],
    },
    "OH": {
        "agency": "Ohio Secretary of State Business Services",
        "website": "https://www.ohiosos.gov/businesses/",
        "entity_search": "https://businesssearch.ohiosos.gov/",
        "fee_sources": ["https://www.ohiosos.gov/businesses/filing-forms--fee-schedule/"],
    },
    "OK": {
        "agency": "Oklahoma Secretary of State Business Services",
        "website": "https://www.sos.ok.gov/business/",
        "entity_search": "https://www.sos.ok.gov/corp/corpInquiryFind.aspx",
        "fee_sources": ["https://www.sos.ok.gov/business/fees.aspx"],
    },
    "OR": {
        "agency": "Oregon Secretary of State Corporation Division",
        "website": "https://sos.oregon.gov/business/Pages/default.aspx",
        "entity_search": "https://secure.sos.state.or.us/oard/search.action",
        "fee_sources": ["https://sos.oregon.gov/business/Pages/business-filing-fees.aspx"],
    },
    "PA": {
        "agency": "Pennsylvania Department of State Bureau of Corporations and Charitable Organizations",
        "website": "https://www.pa.gov/agencies/dos/programs/business",
        "entity_search": "https://file.dos.pa.gov/search/business",
        "fee_sources": ["https://www.pa.gov/agencies/dos/programs/business/fees-and-payments.html"],
    },
    "RI": {
        "agency": "Rhode Island Department of State Business Services",
        "website": "https://sos.ri.gov/divisions/business-services",
        "entity_search": "https://business.sos.ri.gov/CorpWeb/CorpSearch/CorpSearch.aspx",
        "fee_sources": ["https://www.sos.ri.gov/divisions/business-services/business-basics/costs-and-fees"],
    },
    "SC": {
        "agency": "South Carolina Secretary of State Business Entities",
        "website": "https://sos.sc.gov/business-entities",
        "entity_search": "https://businessfilings.sc.gov/BusinessFiling/Entity/Search",
        "fee_sources": ["https://sos.sc.gov/business-entities/filing-fees"],
    },
    "SD": {
        "agency": "South Dakota Secretary of State Business Services",
        "website": "https://sdsos.gov/business-services/",
        "entity_search": "https://sosenterprise.sd.gov/BusinessServices/Business/FilingSearch.aspx",
        "fee_sources": ["https://sdsos.gov/general-information/filing-fees.aspx"],
    },
    "TN": {
        "agency": "Tennessee Secretary of State Business Services",
        "website": "https://sos.tn.gov/businesses",
        "entity_search": "https://tnbear.tn.gov/Ecommerce/FilingSearch.aspx",
        "fee_sources": ["https://sos.tn.gov/businesses/forms-and-fees"],
    },
    "TX": {
        "agency": "Texas Secretary of State Business and Commercial Section",
        "website": "https://www.sos.state.tx.us/corp/",
        "entity_search": "https://mycpa.cpa.state.tx.us/coa/",
        "fee_sources": [
            "https://www.sos.state.tx.us/corp/forms_boc.shtml",
            "https://comptroller.texas.gov/taxes/franchise/",
        ],
    },
    "UT": {
        "agency": "Utah Division of Corporations and Commercial Code",
        "website": "https://corporations.utah.gov",
        "entity_search": "https://secure.utah.gov/bes/",
        "fee_sources": ["https://commerce.utah.gov/wp-content/uploads/2023/04/currentfees.pdf"],
    },
    "VT": {
        "agency": "Vermont Secretary of State Corporations Division",
        "website": "https://sos.vermont.gov/corporations/",
        "entity_search": "https://bizfilings.vermont.gov/online/BusinessInquire",
        "fee_sources": ["https://sos.vermont.gov/corporations/fees/"],
    },
    "VA": {
        "agency": "Virginia State Corporation Commission Clerk's Office",
        "website": "https://www.scc.virginia.gov/pages/Clerk-Information",
        "entity_search": "https://cis.scc.virginia.gov/EntitySearch/Index",
        "fee_sources": ["https://www.scc.virginia.gov/pages/Fees"],
    },
    "WA": {
        "agency": "Washington Secretary of State Corporations and Charities Division",
        "website": "https://www.sos.wa.gov/corporations-charities",
        "entity_search": "https://ccfs.sos.wa.gov/#/BusinessSearch",
        "fee_sources": [
            "https://www.sos.wa.gov/corporations-charities/business-entities/online-filing-instructions/start-domestic-wa-limited-liability-company-llc-online",
            "https://www.sos.wa.gov/corporations-charities/frequently-asked-questions-faqs/fee-scheduleexpedited-service",
        ],
    },
    "WV": {
        "agency": "West Virginia Secretary of State Business and Licensing Division",
        "website": "https://sos.wv.gov/business",
        "entity_search": "https://apps.wv.gov/SOS/BusinessEntitySearch/",
        "fee_sources": ["https://sos.wv.gov/media/282/download?inline="],
    },
    "WI": {
        "agency": "Wisconsin Department of Financial Institutions",
        "website": "https://dfi.wi.gov/Pages/BusinessServices/Corporations/",
        "entity_search": "https://apps.dfi.wi.gov/apps/CorpSearch/Search.aspx",
        "fee_sources": ["https://dfi.wi.gov/Pages/BusinessServices/Corporations/FeeSchedule.aspx"],
    },
    "WY": {
        "agency": "Wyoming Secretary of State Business Division",
        "website": "https://sos.wyo.gov/Business/Default.aspx",
        "entity_search": "https://wyobiz.wyo.gov/Business/FilingSearch.aspx",
        "fee_sources": ["https://sos.wyo.gov/Business/docs/BusinessFees.pdf"],
    },
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def source_name(index: int, url: str) -> str:
    if "tax" in url.lower() or "annual" in url.lower() or "franchise" in url.lower():
        return "Official Annual Report or Tax Source"
    if index == 0:
        return "Official Filing Fee Source"
    return "Official Supporting Source"


def update_state_file(path: Path) -> None:
    data = load_json(path)
    abbr = data["stateAbbr"]
    config = URLS[abbr]

    data.setdefault("businessEntitySearch", {})
    data.setdefault("secretaryOfState", {})

    data["businessEntitySearch"]["url"] = config["entity_search"]
    data["secretaryOfState"]["agency"] = config["agency"]
    data["secretaryOfState"]["website"] = config["website"]
    data["sources"] = [
        {
            "name": source_name(index, url),
            "url": url,
            "lastAccessed": TODAY,
        }
        for index, url in enumerate(config["fee_sources"])
    ]
    data["lastVerified"] = TODAY

    write_json(path, data)


def update_root_states() -> None:
    root = load_json(ROOT_DATA_PATH)
    for abbr, config in URLS.items():
        state = root["states"][abbr]
        fee_sources = config["fee_sources"]
        state["official_link"] = fee_sources[0]
        state["source_url"] = fee_sources[-1]
        state["last_verified"] = TODAY
    root["last_updated"] = TODAY
    write_json(ROOT_DATA_PATH, root)


def main() -> None:
    missing = sorted(set(URLS) - {load_json(path)["stateAbbr"] for path in STATE_DIR.glob("*.json")})
    if missing:
        raise SystemExit(f"Missing state files for: {', '.join(missing)}")

    for path in sorted(STATE_DIR.glob("*.json")):
        update_state_file(path)
    update_root_states()
    print(f"Applied URL corrections for {len(URLS)} states")


if __name__ == "__main__":
    main()
