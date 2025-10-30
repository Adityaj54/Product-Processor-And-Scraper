"""
Product Processor

This is the main entry point for the product processor application.
It processes product data from JSON files, downloads images, and generates a CSV file.
It can also scrape product data from websites.
"""
import sys
import logging
from typing import Dict, Any, List

from product_processor.json_utils.loader import load_json_files
from product_processor.csv_utils.generator import generate_csv
from product_processor.image_utils.downloader import download_product_images
from product_processor.utils.config import setup_logging, parse_args, validate_config
from product_processor.scraper.cli import main as scraper_main

logger = logging.getLogger(__name__)

def process_products(config: Dict[str, Any]) -> None:
    """
    Process products according to the provided configuration.

    Args:
        config (Dict[str, Any]): Configuration dictionary
    """
    try:
        # Load JSON files
        logger.info(f"Loading JSON files from {config['input_dir']}")
        products = load_json_files(config["input_dir"])
        logger.info(f"Loaded {len(products)} products")

        # Download images if requested
        if config["download_images"]:
            logger.info(f"Downloading images to {config['images_dir']}")
            products = download_product_images(
                products, 
                config["images_dir"], 
                config["max_workers"]
            )
            logger.info("Image download complete")

            # Update image URLs in CSV to include local paths
            for product in products:
                if "local_image_paths" in product:
                    # Create a mapping of URLs to local paths
                    image_mapping = {}
                    for i, url in enumerate(product.get("image_urls", [])):
                        if i < len(product["local_image_paths"]) and product["local_image_paths"][i]:
                            image_mapping[url] = product["local_image_paths"][i]

                    # Replace image_urls with local paths where available
                    for i, url in enumerate(product.get("image_urls", [])):
                        if url in image_mapping:
                            product["image_urls"][i] = image_mapping[url]

        # Generate CSV
        logger.info(f"Generating CSV file: {config['output_csv']}")
        generate_csv(products, config["output_csv"])
        logger.info(f"CSV file generated successfully: {config['output_csv']}")

    except Exception as e:
        logger.error(f"Error processing products: {str(e)}")
        raise

def main() -> int:
    """
    Main entry point for the application.

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    try:
        # Parse command-line arguments
        config = parse_args()

        # Set up logging
        setup_logging(config["log_level"])

        # Get the command to execute
        command = config.get("command", "process")

        if command == "process":
            # Validate configuration
            validate_config(config)

            # Process products
            process_products(config)

            logger.info("Product processing completed successfully")
            return 0

        elif command == "scrape":
            # Call the scraper main function
            return scraper_main()

        else:
            logger.error(f"Unknown command: {command}")
            return 1

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
