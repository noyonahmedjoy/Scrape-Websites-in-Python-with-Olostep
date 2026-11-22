import argparse
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv
from olostep import Olostep, Olostep_BaseError


FORMATS = ("markdown", "html", "text")
CONTENT_ATTRIBUTES = {
    "markdown": "markdown_content",
    "html": "html_content",
    "text": "text_content",
}


def build_parser():
    parser = argparse.ArgumentParser(
        prog="olostep-scraper",
        description="Scrape a web page with Olostep and print or save its content.",
    )
    parser.add_argument("url", help="The complete URL of the page to scrape.")
    parser.add_argument(
        "--format",
        dest="formats",
        action="append",
        choices=FORMATS,
        default=None,
        help="Output format; repeat to request multiple formats. Defaults to markdown.",
    )
    parser.add_argument(
        "--wait-ms",
        type=int,
        default=0,
        help="Milliseconds to wait before reading JavaScript-rendered content.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Save the selected content to this file instead of printing it.",
    )
    return parser


def validate_url(url):
    parsed_url = urlparse(url)
    if parsed_url.scheme not in ("http", "https") or not parsed_url.netloc:
        raise ValueError("Provide a complete HTTP or HTTPS URL.")


def main(argv=None):
    args = build_parser().parse_args(argv)

    try:
        validate_url(args.url)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2

    if args.wait_ms < 0:
        print("Error: --wait-ms must be zero or greater.", file=sys.stderr)
        return 2

    if args.output and len(args.formats) > 1:
        print("Error: --output can only be used with one output format.", file=sys.stderr)
        return 2

    load_dotenv()
    if not os.getenv("OLOSTEP_API_KEY"):
        print(
            "Error: OLOSTEP_API_KEY is not set. Add it to your .env file or environment.",
            file=sys.stderr,
        )
        return 2

    formats = list(dict.fromkeys(args.formats or ["markdown"]))
    try:
        client = Olostep()
        page = client.scrapes.create(
            url_to_scrape=args.url,
            formats=formats,
            wait_before_scraping=args.wait_ms,
        )
    except Olostep_BaseError as error:
        print(f"Olostep request failed ({type(error).__name__}): {error}", file=sys.stderr)
        return 1

    if args.output:
        content = getattr(page, CONTENT_ATTRIBUTES[formats[0]], None)
        if content is None:
            print(f"Error: Olostep returned no {formats[0]} content.", file=sys.stderr)
            return 1
        try:
            args.output.write_text(content, encoding="utf-8")
        except OSError as error:
            print(f"Error: Could not write {args.output}: {error}", file=sys.stderr)
            return 1
        print(f"Saved {formats[0]} content to {args.output}")
        return 0

    for output_format in formats:
        content = getattr(page, CONTENT_ATTRIBUTES[output_format], None)
        if content is None:
            print(f"Error: Olostep returned no {output_format} content.", file=sys.stderr)
            return 1
        if len(formats) > 1:
            print(f"--- {output_format.upper()} ---")
        print(content)
    print(f"Credits used: {page.credits_consumed}", file=sys.stderr)
    return 0
