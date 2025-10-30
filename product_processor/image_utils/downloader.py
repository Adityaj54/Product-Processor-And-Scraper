"""
Image Downloader Module

This module provides functionality to download images from URLs.
"""
import os
import logging
import requests
from typing import List, Dict, Any, Tuple
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

def download_image(url: str, output_dir: str, product_id: str = None, index: int = 0) -> Tuple[str, str]:
    """
    Download an image from a URL and save it to the output directory.
    
    Args:
        url (str): URL of the image to download
        output_dir (str): Directory to save the image to
        product_id (str, optional): ID of the product the image belongs to
        index (int, optional): Index of the image in the product's image list
        
    Returns:
        Tuple[str, str]: Tuple containing the original URL and the local path to the downloaded image
        
    Raises:
        requests.RequestException: If there's an error downloading the image
        IOError: If there's an error saving the image
    """
    if not url:
        logger.warning("Empty URL provided, skipping download")
        return url, ""
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Parse URL to get filename
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        # If filename is empty or doesn't have an extension, create a default one
        if not filename or '.' not in filename:
            filename = f"image_{product_id}_{index}.jpg"
        
        # Add product_id prefix if provided
        if product_id:
            filename = f"{product_id}_{filename}"
        
        output_path = os.path.join(output_dir, filename)
        
        # Download the image
        logger.info(f"Downloading image from {url} to {output_path}")
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        # Save the image
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        logger.info(f"Successfully downloaded image to {output_path}")
        return url, output_path
        
    except requests.RequestException as e:
        logger.error(f"Error downloading image from {url}: {str(e)}")
        return url, ""
    except Exception as e:
        logger.error(f"Error saving image from {url}: {str(e)}")
        return url, ""

def download_product_images(products: List[Dict[str, Any]], output_dir: str, max_workers: int = 10) -> List[Dict[str, Any]]:
    """
    Download all images for a list of products.
    
    Args:
        products (List[Dict[str, Any]]): List of product dictionaries
        output_dir (str): Directory to save the images to
        max_workers (int, optional): Maximum number of concurrent downloads
        
    Returns:
        List[Dict[str, Any]]: Updated list of product dictionaries with local image paths
    """
    if not products:
        logger.warning("No products provided for image download")
        return products
    
    logger.info(f"Downloading images for {len(products)} products to {output_dir}")
    
    # Create a list of all download tasks
    download_tasks = []
    for product in products:
        product_id = product.get('product_id', 'unknown')
        image_urls = product.get('image_urls', [])
        
        for i, url in enumerate(image_urls):
            download_tasks.append((url, output_dir, product_id, i))
    
    # Download images in parallel
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {
            executor.submit(download_image, url, output_dir, product_id, i): (product_id, i, url)
            for url, output_dir, product_id, i in download_tasks
        }
        
        for future in future_to_url:
            product_id, index, url = future_to_url[future]
            try:
                _, local_path = future.result()
                if local_path:
                    if product_id not in results:
                        results[product_id] = {}
                    results[product_id][url] = local_path
            except Exception as e:
                logger.error(f"Error processing download task for {url}: {str(e)}")
    
    # Update products with local image paths
    for product in products:
        product_id = product.get('product_id', 'unknown')
        if product_id in results:
            image_urls = product.get('image_urls', [])
            local_image_paths = []
            
            for url in image_urls:
                local_path = results[product_id].get(url, "")
                local_image_paths.append(local_path)
            
            product['local_image_paths'] = local_image_paths
    
    logger.info(f"Finished downloading images for {len(products)} products")
    return products