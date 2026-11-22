# Scrape Websites in Python with Olostep

A beginner-friendly command-line project for scraping public web pages with the [Olostep Python SDK](https://docs.olostep.com/sdks/python). Choose Markdown, HTML, or plain text, wait for JavaScript-rendered pages, and save a result to a file.

The examples use the practice sites [Books to Scrape](https://books.toscrape.com/) and [Quotes to Scrape](https://quotes.toscrape.com/). Scrape responsibly: review a website's terms and `robots.txt`, collect only public information, and keep your request rate low.

## What You Will Build

By following this tutorial, you will:

1. Install the Olostep SDK and configure an API key outside the source code.
2. Scrape a page to Markdown.
3. Choose between Markdown, HTML, and text output.
4. Wait for content rendered by JavaScript.
5. Save the result to a local file and handle common request errors.

## Prerequisites

- Python 3.11 or newer.
- An Olostep API key from the [Olostep dashboard](https://www.olostep.com/dashboard/).
- A terminal and an internet connection.

Olostep requests may use credits. Check your account and the current pricing before running scrapes.

## How to Set Up the Project

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/scrape-websites-with-olostep.git
cd scrape-websites-with-olostep
```

Replace `YOUR_USERNAME` with your GitHub username and adjust the repository name if needed.

### 2. Create and activate a virtual environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install the dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

The project installs `olostep` for scraping and `python-dotenv` for loading your local environment configuration.

### 4. Configure your API key

Copy the example environment file:

On macOS or Linux:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Open `.env` and replace the example value with your key:

```dotenv
OLOSTEP_API_KEY=your_real_api_key
```

The original `.env` file is ignored by Git. Keep your real key private and never commit it. The application reads this setting from the environment; the API key is not stored in the Python source.

## How to Scrape a Page to Markdown

Run the Books to Scrape example:

```bash
python -m olostep_scraper https://books.toscrape.com/
```

Markdown is the default output. It preserves useful headings, lists, and tables without requiring you to work with all the page's HTML tags.

You can also install and use the command-line entry point:

```bash
olostep-scraper https://books.toscrape.com/
```

## How to Choose an Output Format

Choose one format with `--format`:

```bash
python -m olostep_scraper https://books.toscrape.com/ --format html
python -m olostep_scraper https://books.toscrape.com/ --format text
```

| Format | Use it when |
| --- | --- |
| `markdown` | You want readable page content or content for search and language-model workflows. |
| `html` | You plan to parse markup yourself. |
| `text` | You only need the words without page formatting. |

You can request multiple formats in one scrape:

```bash
python -m olostep_scraper https://books.toscrape.com/ --format html --format markdown --format text
```

The CLI prints each requested result and reports the credits used.

## How to Scrape Pages That Load With JavaScript

The Quotes to Scrape JavaScript example renders quotes in the browser. Ask Olostep to wait two seconds before reading the page:

```bash
python -m olostep_scraper https://quotes.toscrape.com/js/ --wait-ms 2000
```

Use `--wait-ms` when a page needs extra time to render. The value is a number of milliseconds and defaults to `0`.

## How to Save Scraped Content

Use `--output` to write a single selected format to a file:

```bash
python -m olostep_scraper https://books.toscrape.com/ --format markdown --output books.md
```

The command reports the output file path after saving. `--output` accepts one format at a time.

## How Errors Are Handled

The CLI checks that the URL is a complete HTTP or HTTPS address and that `--wait-ms` is not negative. It also checks for `OLOSTEP_API_KEY` before making a request. Olostep SDK errors are reported with their error type and message, and the command exits with a non-zero status.

For example, this command has an invalid URL:

```bash
python -m olostep_scraper not-a-url
```

Fix the URL and try again. A malformed URL is rejected before the scrape request is sent.

## Repository Structure

```text
.
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── README.md
├── src/
│   └── olostep_scraper/
│       ├── __init__.py
│       ├── __main__.py
│       └── cli.py
└── tests/
    └── test_cli.py
```

## Testing

Run the unit tests from the project root:

```bash
python -m unittest discover -s tests -v
```

The tests cover URL validation and command-line argument parsing; they do not make paid Olostep requests.

## Troubleshooting

### `OLOSTEP_API_KEY is not set`

Make sure `.env` exists in the directory where you run the command and contains a valid `OLOSTEP_API_KEY` value. You can also set the variable in your terminal environment.

### `No module named olostep_scraper`

Activate the virtual environment and install the project with `python -m pip install -e .`, or run the project from its root using `python -m olostep_scraper`.

### The scraped page is missing content

Try a longer `--wait-ms` value for pages that render content with JavaScript. Some pages may also require interaction beyond a wait, and not every website permits automated access.

## Next Steps

- Check the [Olostep Python SDK documentation](https://docs.olostep.com/sdks/python) for batches, crawling, and advanced scrape options.
- Add a file-based output workflow for processing content downstream.
- Review website policies and keep scrape volume responsible.
