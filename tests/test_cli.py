import unittest

from olostep_scraper.cli import build_parser, validate_url


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


if __name__ == "__main__":
    unittest.main()
