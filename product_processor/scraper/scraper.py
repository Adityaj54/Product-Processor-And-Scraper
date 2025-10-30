"""
Web Scraper Module

This module provides functionality to scrape product data from websites.
"""
import logging
import requests
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class ProductScraper:
    """
    A class for scraping product data from websites.
    """
    
    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None):
        """
        Initialize the ProductScraper.
        
        Args:
            base_url (str): The base URL of the website to scrape
            headers (Dict[str, str], optional): HTTP headers to use for requests
        """
        self.base_url = base_url
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        logger.info(f"Initialized ProductScraper for {base_url}")
    
    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Get a page and parse it with BeautifulSoup.
        
        Args:
            url (str): The URL to fetch
            
        Returns:
            Optional[BeautifulSoup]: Parsed HTML or None if request failed
        """
        try:
            full_url = urljoin(self.base_url, url)
            logger.info(f"Fetching page: {full_url}")
            
            response = requests.get(full_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            logger.debug(f"Successfully parsed page: {full_url}")
            return soup
            
        except requests.RequestException as e:
            logger.error(f"Error fetching page {url}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error parsing page {url}: {str(e)}")
            return None
    
    def extract_product_links(self, soup: BeautifulSoup, product_link_selector: str) -> List[str]:
        """
        Extract product links from a page.
        
        Args:
            soup (BeautifulSoup): Parsed HTML
            product_link_selector (str): CSS selector for product links
            
        Returns:
            List[str]: List of product URLs
        """
        try:
            links = []
            for link in soup.select(product_link_selector):
                href = link.get('href')
                if href:
                    full_url = urljoin(self.base_url, href)
                    links.append(full_url)
            
            logger.info(f"Extracted {len(links)} product links")
            return links
            
        except Exception as e:
            logger.error(f"Error extracting product links: {str(e)}")
            return []
    
    def extract_product_data(self, soup: BeautifulSoup, selectors: Dict[str, str]) -> Dict[str, Any]:
        """
        Extract product data from a product page.
        
        Args:
            soup (BeautifulSoup): Parsed HTML
            selectors (Dict[str, str]): Dictionary mapping field names to CSS selectors
            
        Returns:
            Dict[str, Any]: Extracted product data
        """
        try:
            product = {}
            
            for field, selector in selectors.items():
                elements = soup.select(selector)
                if elements:
                    if field == 'image_urls':
                        # Extract multiple image URLs
                        product[field] = [img.get('src') for img in elements if img.get('src')]
                    else:
                        # Extract text for other fields
                        product[field] = elements[0].get_text().strip()
            
            logger.debug(f"Extracted product data: {product}")
            return product
            
        except Exception as e:
            logger.error(f"Error extracting product data: {str(e)}")
            return {}
    
    def scrape_products(self, category_url: str, product_link_selector: str, 
                       product_selectors: Dict[str, str], max_products: int = 100) -> List[Dict[str, Any]]:
        """
        Scrape products from a category page.
        
        Args:
            category_url (str): URL of the category page
            product_link_selector (str): CSS selector for product links
            product_selectors (Dict[str, str]): Dictionary mapping field names to CSS selectors
            max_products (int, optional): Maximum number of products to scrape
            
        Returns:
            List[Dict[str, Any]]: List of product dictionaries
        """
        products = []
        
        # Get the category page
        category_soup = self.get_page(category_url)
        if not category_soup:
            logger.error(f"Failed to fetch category page: {category_url}")
            return products
        
        # Extract product links
        product_links = self.extract_product_links(category_soup, product_link_selector)
        logger.info(f"Found {len(product_links)} product links")
        
        # Limit the number of products to scrape
        product_links = product_links[:max_products]
        
        # Scrape each product page
        for i, link in enumerate(product_links):
            logger.info(f"Scraping product {i+1}/{len(product_links)}: {link}")
            
            product_soup = self.get_page(link)
            if not product_soup:
                logger.warning(f"Failed to fetch product page: {link}")
                continue
            
            product_data = self.extract_product_data(product_soup, product_selectors)
            if product_data:
                product_data['product_url'] = link
                products.append(product_data)
        
        logger.info(f"Successfully scraped {len(products)} products")
        return products

def scrape_products_from_website(base_url: str, category_url: str, 
                               product_link_selector: str, 
                               product_selectors: Dict[str, str],
                               max_products: int = 100) -> List[Dict[str, Any]]:
    """
    Scrape products from a website.
    
    Args:
        base_url (str): Base URL of the website
        category_url (str): URL of the category page
        product_link_selector (str): CSS selector for product links
        product_selectors (Dict[str, str]): Dictionary mapping field names to CSS selectors
        max_products (int, optional): Maximum number of products to scrape
        
    Returns:
        List[Dict[str, Any]]: List of product dictionaries
    """
    scraper = ProductScraper(base_url)
    return scraper.scrape_products(category_url, product_link_selector, product_selectors, max_products)