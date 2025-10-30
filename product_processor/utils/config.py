"""
Configuration Module

This module provides functionality to handle configuration settings for the product processor.
"""
import os
import argparse
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def setup_logging(log_level: str = "INFO") -> None:
    """
    Set up logging configuration.

    Args:
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def parse_args() -> Dict[str, Any]:
    """
    Parse command-line arguments.

    Returns:
        Dict[str, Any]: Dictionary of parsed arguments
    """
    parser = argparse.ArgumentParser(description="Process product data from JSON files, download images, and scrape websites.")

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Process command (default)
    process_parser = subparsers.add_parser("process", help="Process JSON files and generate CSV")

    process_parser.add_argument(
        "--input-dir",
        type=str,
        default="rawJson",
        help="Directory containing JSON files (default: rawJson)"
    )

    process_parser.add_argument(
        "--output-csv",
        type=str,
        default="products.csv",
        help="Output CSV file path (default: products.csv)"
    )

    process_parser.add_argument(
        "--images-dir",
        type=str,
        default="images",
        help="Directory to save downloaded images (default: images)"
    )

    process_parser.add_argument(
        "--download-images",
        action="store_true",
        help="Download images from URLs"
    )

    process_parser.add_argument(
        "--max-workers",
        type=int,
        default=10,
        help="Maximum number of concurrent image downloads (default: 10)"
    )

    # Scrape command
    scrape_parser = subparsers.add_parser("scrape", help="Scrape product data from websites")

    scrape_parser.add_argument(
        "--base-url",
        type=str,
        required=True,
        help="Base URL of the website to scrape"
    )

    scrape_parser.add_argument(
        "--category-url",
        type=str,
        required=True,
        help="URL of the category page to scrape"
    )

    scrape_parser.add_argument(
        "--product-link-selector",
        type=str,
        required=True,
        help="CSS selector for product links"
    )

    scrape_parser.add_argument(
        "--selectors-file",
        type=str,
        required=True,
        help="JSON file containing CSS selectors for product data"
    )

    scrape_parser.add_argument(
        "--output-dir",
        type=str,
        default="rawJson",
        help="Directory to save scraped product data (default: rawJson)"
    )

    scrape_parser.add_argument(
        "--output-file",
        type=str,
        default="products.json",
        help="Filename to save scraped product data (default: products.json)"
    )

    scrape_parser.add_argument(
        "--max-products",
        type=int,
        default=100,
        help="Maximum number of products to scrape (default: 100)"
    )

    # Common arguments for all commands
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level (default: INFO)"
    )

    args = parser.parse_args()

    # If no command is specified, default to "process"
    if not args.command:
        args.command = "process"

    # Convert args to dictionary
    config = {
        "command": args.command,
        "log_level": args.log_level
    }

    # Add command-specific arguments
    if args.command == "process":
        config.update({
            "input_dir": args.input_dir,
            "output_csv": args.output_csv,
            "images_dir": args.images_dir,
            "download_images": args.download_images,
            "max_workers": args.max_workers,
        })

        # Ensure paths are absolute
        config["input_dir"] = os.path.abspath(config["input_dir"])
        config["output_csv"] = os.path.abspath(config["output_csv"])
        config["images_dir"] = os.path.abspath(config["images_dir"])

    elif args.command == "scrape":
        config.update({
            "base_url": args.base_url,
            "category_url": args.category_url,
            "product_link_selector": args.product_link_selector,
            "selectors_file": args.selectors_file,
            "output_dir": args.output_dir,
            "output_file": args.output_file,
            "max_products": args.max_products,
        })

        # Ensure paths are absolute
        config["selectors_file"] = os.path.abspath(config["selectors_file"])
        config["output_dir"] = os.path.abspath(config["output_dir"])

    return config

def validate_config(config: Dict[str, Any]) -> None:
    """
    Validate configuration settings.

    Args:
        config (Dict[str, Any]): Configuration dictionary

    Raises:
        ValueError: If configuration is invalid
    """
    command = config.get("command", "process")

    if command == "process":
        # Check if input directory exists
        if not os.path.exists(config["input_dir"]):
            raise ValueError(f"Input directory does not exist: {config['input_dir']}")

        # Check if input directory contains JSON files
        json_files = [f for f in os.listdir(config["input_dir"]) if f.endswith(".json")]
        if not json_files:
            raise ValueError(f"No JSON files found in input directory: {config['input_dir']}")

        # Create output directory for CSV if it doesn't exist
        output_dir = os.path.dirname(config["output_csv"])
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

    elif command == "scrape":
        # Check if selectors file exists
        if not os.path.exists(config["selectors_file"]):
            raise ValueError(f"Selectors file does not exist: {config['selectors_file']}")

        # Create output directory if it doesn't exist
        if not os.path.exists(config["output_dir"]):
            os.makedirs(config["output_dir"], exist_ok=True)

    logger.info(f"Configuration validated successfully: {config}")
