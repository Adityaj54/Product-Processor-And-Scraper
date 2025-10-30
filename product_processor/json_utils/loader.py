"""
JSON Loader Module

This module provides functionality to load and process JSON files containing product data.
"""
import os
import json
import logging
from typing import List, Dict, Any, Union

logger = logging.getLogger(__name__)

def load_json_files(folder_path: str) -> List[Dict[str, Any]]:
    """
    Load all JSON files from the specified folder and return a list of product dictionaries.
    
    Args:
        folder_path (str): Path to the folder containing JSON files
        
    Returns:
        List[Dict[str, Any]]: List of product dictionaries
        
    Raises:
        FileNotFoundError: If the folder_path doesn't exist
        json.JSONDecodeError: If a JSON file is invalid
    """
    all_products = []
    
    try:
        # Check if folder exists
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder not found: {folder_path}")
            
        # Load all JSON files
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
                logger.info(f"Loading JSON file: {file_path}")
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        
                        if isinstance(data, list):
                            logger.debug(f"Found {len(data)} products in {filename}")
                            all_products.extend(data)
                        elif isinstance(data, dict):
                            logger.debug(f"Found 1 product in {filename}")
                            all_products.append(data)
                        else:
                            logger.warning(f"Unexpected data type in {filename}: {type(data)}")
                            
                except json.JSONDecodeError as e:
                    logger.error(f"Error parsing JSON file {filename}: {str(e)}")
                    raise
                except Exception as e:
                    logger.error(f"Error processing file {filename}: {str(e)}")
                    raise
                    
        logger.info(f"Successfully loaded {len(all_products)} products from {folder_path}")
        return all_products
        
    except Exception as e:
        logger.error(f"Error loading JSON files: {str(e)}")
        raise