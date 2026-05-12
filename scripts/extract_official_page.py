#!/usr/bin/env python3
"""Fetch an official source page and print selector matches for inspection."""

from __future__ import annotations

import argparse

from scrapling.fetchers import Fetcher


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inspect official state source pages with Scrapling."
    )
    parser.add_argument("url", help="Official state government URL to fetch")
    parser.add_argument(
        "--selector",
        default="body",
        help="CSS selector to extract. Defaults to the whole body.",
    )
    args = parser.parse_args()

    page = Fetcher.get(args.url, stealthy_headers=True)
    matches = page.css(args.selector)

    for index, match in enumerate(matches, start=1):
        text = " ".join(match.css("::text").getall()).strip()
        print(f"--- match {index} ---")
        print(text)


if __name__ == "__main__":
    main()
