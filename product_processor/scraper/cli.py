"""
Web Scraper CLI

This module provides a command-line interface for the web scraper.
"""
import os
import sys
import json
import argparse
import logging
from typing import Dict, Any

from product_processor.scraper.scraper import scrape_products_from_website
from product_processor.utils.config import setup_logging

logger = logging.getLogger(__name__)

def parse_scraper_args() -> Dict[str, Any]:
    """
    Parse command-line arguments for the scraper.
    
    Returns:
        Dict[str, Any]: Dictionary of parsed arguments
    """
    parser = argparse.ArgumentParser(description="Scrape product data from websites.")
    
    parser.add_argument(
        "--base-url",
        type=str,
        required=True,
        help="Base URL of the website to scrape"
    )
    
    parser.add_argument(
        "--category-url",
        type=str,
        required=True,
        help="URL of the category page to scrape"
    )
    
    parser.add_argument(
        "--product-link-selector",
        type=str,
        required=True,
        help="CSS selector for product links"
    )
    
    parser.add_argument(
        "--selectors-file",
        type=str,
        required=True,
        help="JSON file containing CSS selectors for product data"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default="rawJson",
        help="Directory to save scraped product data (default: rawJson)"
    )
    
    parser.add_argument(
        "--output-file",
        type=str,
        default="products.json",
        help="Filename to save scraped product data (default: products.json)"
    )
    
    parser.add_argument(
        "--max-products",
        type=int,
        default=100,
        help="Maximum number of products to scrape (default: 100)"
    )
    
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    
    args = parser.parse_args()
    
    # Convert args to dictionary
    config = {
        "base_url": args.base_url,
        "category_url": args.category_url,
        "product_link_selector": args.product_link_selector,
        "selectors_file": args.selectors_file,
        "output_dir": args.output_dir,
        "output_file": args.output_file,
        "max_products": args.max_products,
        "log_level": args.log_level
    }
    
    # Ensure paths are absolute
    config["selectors_file"] = os.path.abspath(config["selectors_file"])
    config["output_dir"] = os.path.abspath(config["output_dir"])
    
    return config

def load_selectors(selectors_file: str) -> Dict[str, str]:
    """
    Load CSS selectors from a JSON file.
    
    Args:
        selectors_file (str): Path to the JSON file containing CSS selectors
        
    Returns:
        Dict[str, str]: Dictionary mapping field names to CSS selectors
        
    Raises:
        FileNotFoundError: If the selectors file doesn't exist
        json.JSONDecodeError: If the selectors file is invalid JSON
    """
    try:
        with open(selectors_file, 'r', encoding='utf-8') as f:
            selectors = json.load(f)
        
        logger.info(f"Loaded selectors from {selectors_file}")
        return selectors
    
    except FileNotFoundError:
        logger.error(f"Selectors file not found: {selectors_file}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in selectors file: {str(e)}")
        raise

def main() -> int:
    """
    Main entry point for the scraper CLI.
    
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    try:
        # Parse command-line arguments
        config = parse_scraper_args()
        
        # Set up logging
        setup_logging(config["log_level"])
        
        # Load selectors
        selectors = load_selectors(config["selectors_file"])
        
        # Create output directory if it doesn't exist
        os.makedirs(config["output_dir"], exist_ok=True)
        
        # Scrape products
        logger.info(f"Scraping products from {config['base_url']}")
        products = scrape_products_from_website(
            config["base_url"],
            config["category_url"],
            config["product_link_selector"],
            selectors,
            config["max_products"]
        )
        
        # Save products to JSON file
        output_path = os.path.join(config["output_dir"], config["output_file"])
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=2)
        
        logger.info(f"Saved {len(products)} products to {output_path}")
        return 0
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())