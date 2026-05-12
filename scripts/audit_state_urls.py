#!/usr/bin/env python3
"""Audit state data URLs and classify their intended roles.

This script is intentionally read-only for state JSON files. It produces a
review artifact that separates agency homepages, entity search URLs, fee
sources, annual report sources, and ambiguous URLs before data scraping starts.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from scrapling.fetchers import Fetcher


REPO_ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = REPO_ROOT / "entitysearch-state-data" / "states"
ROOT_DATA_PATH = REPO_ROOT / "states.json"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "entitysearch-state-data" / "audits"

ROLE_KEYWORDS = {
    "fee_schedule": (
        "fee",
        "fees",
        "fee schedule",
        "filing fees",
        "forms fees",
        "payment information",
    ),
    "annual_report": (
        "annual report",
        "annual reports",
        "franchise tax",
        "biennial report",
        "periodic report",
    ),
    "entity_search": (
        "business search",
        "entity search",
        "business entity search",
        "corporation search",
        "corporations search",
        "business records",
        "business lookup",
        "search business",
        "records search",
    ),
    "contact": (
        "contact",
        "contact us",
        "office location",
        "mailing address",
        "phone",
        "hours",
    ),
}

HOMEPAGE_HINTS = (
    "business services",
    "corporations division",
    "business entities",
    "business registration",
    "division of corporations",
    "secretary of state",
)

PATH_HOMEPAGE_SUFFIXES = (
    "",
    "/",
    "/business",
    "/business/",
    "/business-services",
    "/business-services/",
    "/corporations",
    "/corporations/",
    "/corps/",
    "/default.aspx",
)


@dataclass
class FetchResult:
    url: str
    final_url: str | None
    status: int | None
    content_type: str | None
    title: str | None
    h1: str | None
    text_sample: str | None
    error: str | None = None


@dataclass
class ClassifiedUrl:
    url: str
    source_fields: list[str]
    fetched: FetchResult | None
    roles: list[str]
    confidence: str
    official_domain: bool
    notes: list[str]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_url(url: str | None) -> str | None:
    if not url:
        return None
    value = url.strip()
    return value or None


def is_official_domain(url: str) -> bool:
    host = urlparse(url).hostname or ""
    host = host.lower()
    if host.endswith(".gov"):
        return True
    if ".gov." in host:
        return True
    if ".state." in host:
        return True
    if host.endswith(".us") and ("sos" in host or "state" in host):
        return True
    return False


def collect_urls(state_doc: dict[str, Any], root_state: dict[str, Any] | None) -> dict[str, list[str]]:
    urls: dict[str, list[str]] = {}

    def add(field: str, url: str | None) -> None:
        value = normalize_url(url)
        if not value:
            return
        urls.setdefault(value, []).append(field)

    add("state.secretaryOfState.website", state_doc.get("secretaryOfState", {}).get("website"))
    add("state.businessEntitySearch.url", state_doc.get("businessEntitySearch", {}).get("url"))
    for index, source in enumerate(state_doc.get("sources", [])):
        add(f"state.sources[{index}].url", source.get("url"))

    if root_state:
        add("statesJson.official_link", root_state.get("official_link"))
        add("statesJson.source_url", root_state.get("source_url"))

    return urls


def fetch_url(url: str, *, insecure: bool, timeout: int) -> FetchResult:
    try:
        page = Fetcher.get(
            url,
            stealthy_headers=True,
            verify=not insecure,
            timeout=timeout,
        )
    except Exception as exc:  # noqa: BLE001 - report exact fetch failures for review.
        return FetchResult(
            url=url,
            final_url=None,
            status=None,
            content_type=None,
            title=None,
            h1=None,
            text_sample=None,
            error=f"{type(exc).__name__}: {exc}",
        )

    title = first_text(page.css("title::text").getall())
    h1 = first_text(page.css("h1::text").getall())
    body_text = clean_text(" ".join(page.css("body ::text").getall()))
    final_url = getattr(page, "url", None)
    if not final_url and getattr(page, "request", None):
        final_url = getattr(page.request, "url", None)

    return FetchResult(
        url=url,
        final_url=final_url,
        status=getattr(page, "status", None),
        content_type=header_value(getattr(page, "headers", None), "content-type"),
        title=title,
        h1=h1,
        text_sample=body_text[:500] if body_text else None,
    )


def header_value(headers: Any, key: str) -> str | None:
    if not headers:
        return None
    try:
        value = headers.get(key) or headers.get(key.title())
    except AttributeError:
        return None
    if value is None:
        return None
    return str(value)


def first_text(values: list[str]) -> str | None:
    for value in values:
        cleaned = clean_text(value)
        if cleaned:
            return cleaned
    return None


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def classify_url(url: str, fetched: FetchResult | None, source_fields: list[str]) -> tuple[list[str], str, list[str]]:
    notes: list[str] = []
    roles: set[str] = set()
    parsed = urlparse(url)
    path_query = f"{parsed.path} {parsed.query}".lower()
    content_type = (fetched.content_type if fetched else "") or ""
    text_parts = [
        path_query,
        fetched.title if fetched else "",
        fetched.h1 if fetched else "",
        fetched.text_sample if fetched else "",
    ]
    haystack = clean_text(" ".join(part or "" for part in text_parts)).lower()

    if parsed.path.lower().endswith(".pdf") or "application/pdf" in content_type.lower():
        roles.add("pdf")

    for role, keywords in ROLE_KEYWORDS.items():
        if any(keyword in haystack for keyword in keywords):
            roles.add(role)

    if is_homepage_like(parsed.path, haystack):
        roles.add("agency_homepage")

    if "state.secretaryOfState.website" in source_fields and "agency_homepage" not in roles:
        notes.append("secretaryOfState.website does not look like an agency homepage")
    if "state.businessEntitySearch.url" in source_fields and "entity_search" not in roles:
        notes.append("businessEntitySearch.url does not look like an entity search page")
    if "fee_schedule" in roles and "state.secretaryOfState.website" in source_fields:
        notes.append("fee source appears to be stored as secretaryOfState.website")
    if fetched and fetched.status and fetched.status >= 400:
        notes.append(f"HTTP status {fetched.status}; content may be an error page")
    if fetched and fetched.error:
        notes.append("fetch failed")

    confidence = "low"
    if fetched and fetched.error:
        confidence = "none"
    elif len(roles) == 1:
        confidence = "medium"
    elif len(roles) > 1:
        confidence = "low"
    if "agency_homepage" in roles and len(roles) == 1:
        confidence = "high"
    if "fee_schedule" in roles and ("pdf" in roles or "fee" in path_query):
        confidence = "high"
    if "entity_search" in roles and ("search" in path_query or "records" in path_query):
        confidence = "high"

    return sorted(roles) or ["unknown"], confidence, notes


def is_homepage_like(path: str, haystack: str) -> bool:
    normalized_path = path.lower().rstrip("/")
    if path.lower() in PATH_HOMEPAGE_SUFFIXES or normalized_path in PATH_HOMEPAGE_SUFFIXES:
        return True
    if any(hint in haystack for hint in HOMEPAGE_HINTS):
        has_specific_role = any(
            keyword in haystack
            for keywords in ROLE_KEYWORDS.values()
            for keyword in keywords
        )
        return not has_specific_role
    return False


def proposed_roles(classified: list[ClassifiedUrl]) -> dict[str, Any]:
    role_map: dict[str, list[dict[str, str]]] = {
        "agency_homepage": [],
        "entity_search": [],
        "fee_schedule": [],
        "annual_report": [],
        "contact": [],
        "pdf": [],
        "unknown": [],
    }
    for item in classified:
        for role in item.roles:
            role_map.setdefault(role, []).append(
                {
                    "url": item.url,
                    "confidence": item.confidence,
                    "sourceFields": ", ".join(item.source_fields),
                }
            )
    return role_map


def audit(args: argparse.Namespace) -> dict[str, Any]:
    root_data = load_json(ROOT_DATA_PATH) if ROOT_DATA_PATH.exists() else {}
    root_states = root_data.get("states", {})
    requested_states = {abbr.upper() for abbr in args.state}
    result: dict[str, Any] = {
        "generatedAt": date.today().isoformat(),
        "protocol": "official-government-sources-only",
        "readOnly": True,
        "states": {},
    }

    for path in sorted(STATE_DIR.glob("*.json")):
        state_doc = load_json(path)
        abbr = state_doc.get("stateAbbr")
        if requested_states and abbr not in requested_states:
            continue
        root_state = root_states.get(abbr)
        urls = collect_urls(state_doc, root_state)
        classified_items: list[ClassifiedUrl] = []

        for url, fields in sorted(urls.items()):
            fetched = None if args.no_fetch else fetch_url(url, insecure=args.insecure, timeout=args.timeout)
            roles, confidence, notes = classify_url(url, fetched, fields)
            classified_items.append(
                ClassifiedUrl(
                    url=url,
                    source_fields=fields,
                    fetched=fetched,
                    roles=roles,
                    confidence=confidence,
                    official_domain=is_official_domain(url),
                    notes=notes,
                )
            )

        state_notes = []
        for item in classified_items:
            state_notes.extend(item.notes)
            if not item.official_domain:
                state_notes.append(f"URL is not obviously official: {item.url}")

        result["states"][abbr] = {
            "stateName": state_doc.get("stateName"),
            "stateSlug": state_doc.get("stateSlug"),
            "urlCount": len(classified_items),
            "proposedRoles": proposed_roles(classified_items),
            "urls": [asdict(item) for item in classified_items],
            "notes": sorted(set(state_notes)),
        }

    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit state JSON URLs before scraping contact, search, and fee data."
    )
    parser.add_argument(
        "--state",
        action="append",
        default=[],
        help="Limit audit to a state abbreviation. Can be repeated.",
    )
    parser.add_argument(
        "--no-fetch",
        action="store_true",
        help="Classify from URL text only without making network requests.",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable TLS certificate verification for official sites with local CA issues.",
    )
    parser.add_argument("--timeout", type=int, default=30, help="Request timeout in seconds.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_DIR / f"url-audit-{date.today().isoformat()}.json",
        help="Audit JSON output path.",
    )
    args = parser.parse_args()

    report = audit(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {args.output}")
    print(f"Audited {len(report['states'])} states")


if __name__ == "__main__":
    main()
