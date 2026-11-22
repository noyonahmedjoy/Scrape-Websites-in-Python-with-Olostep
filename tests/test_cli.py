import io
import os
import unittest
from contextlib import redirect_stderr, redirect_stdout
from types import SimpleNamespace
from unittest.mock import patch

from olostep_scraper.cli import build_parser, main, validate_url


class ValidateUrlTests(unittest.TestCase):
    def test_accepts_http_and_https_urls(self):
        validate_url("https://books.toscrape.com/")
        validate_url("http://quotes.toscrape.com/js/")

    def test_rejects_urls_without_http_scheme_or_host(self):
        for url in ("books.toscrape.com", "ftp://example.com", "https://"):
            with self.subTest(url=url):
                with self.assertRaises(ValueError):
                    validate_url(url)


class ArgumentParserTests(unittest.TestCase):
    def test_markdown_is_the_default_format(self):
        args = build_parser().parse_args(["https://books.toscrape.com/"])
        self.assertIsNone(args.formats)

    def test_accepts_multiple_output_formats_and_wait(self):
        args = build_parser().parse_args(
            [
                "https://quotes.toscrape.com/js/",
                "--format",
                "markdown",
                "--format",
                "text",
                "--wait-ms",
                "2000",
            ]
        )
        self.assertEqual(args.formats, ["markdown", "text"])
        self.assertEqual(args.wait_ms, 2000)


class MainTests(unittest.TestCase):
    def test_passes_api_key_to_olostep_client(self):
        page = SimpleNamespace(markdown_content="Scraped content", credits_consumed=1)
        with (
            patch("olostep_scraper.cli.load_dotenv"),
            patch.dict(os.environ, {"OLOSTEP_API_KEY": "test-key"}, clear=True),
            patch("olostep_scraper.cli.Olostep") as olostep,
            redirect_stdout(io.StringIO()),
            redirect_stderr(io.StringIO()),
        ):
            olostep.return_value.scrapes.create.return_value = page

            result = main(["https://example.com/"])

        self.assertEqual(result, 0)
        olostep.assert_called_once_with(api_key="test-key")


if __name__ == "__main__":
    unittest.main()
