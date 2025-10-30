# Product Processor

A Python application for processing product data from JSON files, downloading product images, and generating CSV files.

## Features

- Load product data from JSON files
- Generate CSV files with product information
- Download product images from URLs
- Web scraping of product data from websites
- Command-line interface with configurable options
- Parallel image downloading for improved performance
- Comprehensive error handling and logging

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/product-processor.git
   cd product-processor
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install the package (development mode):
   ```
   pip install -e .
   ```

## Usage

The application supports two main commands: `process` and `scrape`.

### Process Command

#### Basic Usage

Process JSON files and generate a CSV file:

```
python -m product_processor process --input-dir /path/to/json/files --output-csv /path/to/output.csv
```

#### Download Images

Process JSON files, download images, and generate a CSV file:

```
python -m product_processor process --input-dir /path/to/json/files --output-csv /path/to/output.csv --images-dir /path/to/images --download-images
```

#### Process Command Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--input-dir` | Directory containing JSON files | `rawJson` |
| `--output-csv` | Output CSV file path | `products.csv` |
| `--images-dir` | Directory to save downloaded images | `images` |
| `--download-images` | Download images from URLs | `False` |
| `--max-workers` | Maximum number of concurrent image downloads | `10` |
| `--log-level` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) | `INFO` |

### Scrape Command

#### Basic Usage

Scrape product data from a website:

```
python -m product_processor scrape --base-url https://example.com --category-url /products --product-link-selector "div.product a" --selectors-file selectors.json
```

#### Scrape Command Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--base-url` | Base URL of the website to scrape | (Required) |
| `--category-url` | URL of the category page to scrape | (Required) |
| `--product-link-selector` | CSS selector for product links | (Required) |
| `--selectors-file` | JSON file containing CSS selectors for product data | (Required) |
| `--output-dir` | Directory to save scraped product data | `rawJson` |
| `--output-file` | Filename to save scraped product data | `products.json` |
| `--max-products` | Maximum number of products to scrape | `100` |
| `--log-level` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) | `INFO` |

#### Selectors File Format

The selectors file should be a JSON file containing CSS selectors for product data:

```json
{
  "name": "h1.product-name",
  "brand": "div.product-brand",
  "price": "span.product-price",
  "description": "div.product-description",
  "image_urls": "div.product-images img"
}
```

## Project Structure

```
product_processor/
├── product_processor/
│   ├── __init__.py
│   ├── main.py
│   ├── csv_utils/
│   │   ├── __init__.py
│   │   └── generator.py
│   ├── image_utils/
│   │   ├── __init__.py
│   │   └── downloader.py
│   ├── json_utils/
│   │   ├── __init__.py
│   │   └── loader.py
│   ├── scraper/
│   │   ├── __init__.py
│   │   ├── scraper.py
│   │   └── cli.py
│   └── utils/
│       ├── __init__.py
│       └── config.py
├── product_processor.py
├── README.md
└── requirements.txt
```

## Examples

### Command-line Examples

#### Process JSON Files

```
python -m product_processor process --input-dir data/json --output-csv data/products.csv
```

#### Download Images

```
python -m product_processor process --input-dir data/json --output-csv data/products.csv --images-dir data/images --download-images
```

#### Scrape Products

First, create a selectors.json file:

```json
{
  "name": "h1.product-name",
  "brand": "div.product-brand",
  "price": "span.product-price",
  "description": "div.product-description",
  "image_urls": "div.product-images img"
}
```

Then run the scraper:

```
python -m product_processor scrape --base-url https://example.com --category-url /products --product-link-selector "div.product a" --selectors-file selectors.json --output-dir data/json
```

#### Debug Mode

```
python -m product_processor process --input-dir data/json --output-csv data/products.csv --log-level DEBUG
```

#### Complete Workflow

Scrape products, then process them and download images:

```
# First, scrape products from a website
python -m product_processor scrape --base-url https://example.com --category-url /products --product-link-selector "div.product a" --selectors-file selectors.json --output-dir data/json

# Then, process the scraped products and download images
python -m product_processor process --input-dir data/json --output-csv data/products.csv --images-dir data/images --download-images
```

### Programmatic Examples

The package includes several example scripts in the `examples` directory:

- `scrape_example.py`: Demonstrates how to use the scraper module programmatically
- `process_example.py`: Demonstrates how to use the process module programmatically
- `complete_workflow.py`: Demonstrates a complete workflow using both the scraper and process functionality
- `selectors.json`: A sample selectors file for scraping product data

To run the examples:

```
cd product_processor
python examples/scrape_example.py
python examples/process_example.py
python examples/complete_workflow.py --base-url https://example.com --category-url /products
```

The complete workflow example supports various command-line arguments:

```
python examples/complete_workflow.py --help
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
