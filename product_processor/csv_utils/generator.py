"""
CSV Generator Module

This module provides functionality to generate CSV files from product data.
"""
import csv
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def generate_csv(products: List[Dict[str, Any]], output_file: str = "products.csv") -> str:
    """
    Generate a CSV file from the product data.
    
    Args:
        products (List[Dict[str, Any]]): List of product dictionaries
        output_file (str): Path to the output CSV file
        
    Returns:
        str: Path to the generated CSV file
        
    Raises:
        ValueError: If products list is empty
        IOError: If there's an error writing to the output file
    """
    if not products:
        logger.error("No products to write to CSV")
        raise ValueError("No products to write to CSV")
    
    try:
        # Determine maximum number of images to create columns
        max_images = 0
        for p in products:
            max_images = max(max_images, len(p.get("image_urls", [])))
        
        logger.info(f"Maximum number of images per product: {max_images}")
        
        # CSV fields
        csv_fields = [
            "brand", "name", "description", "type", "category", "weight_options",
            "THC_percent", "available_for_pickup", "available_for_delivery",
            "aggregate_rating", "review_count"
        ]
        
        # Add price columns dynamically based on common weights
        weights_keys = ["gram", "eighth_ounce", "quarter_ounce", "half_ounce", "ounce"]
        for w in weights_keys:
            csv_fields.extend([f"price_{w}", f"discounted_price_{w}"])
        
        # Add image columns
        for i in range(1, max_images + 1):
            csv_fields.append(f"image_{i}")
        
        csv_fields.extend(["tags", "product_link"])
        
        csv_rows = []
        
        for p in products:
            # Weight options
            weight_options = " - ".join([w.title() for w in p.get("available_weights", [])])
            
            # THC percent: pick first potency from inventory_potencies
            thc_percent = ""
            if p.get("inventory_potencies"):
                thc_percent = str(p["inventory_potencies"][0].get("thc_potency", "")) + "%"
            
            # Prices
            row_prices = {}
            for w in weights_keys:
                orig_key = f"price_{w}"
                disc_key = f"discounted_price_{w}"
                row_prices[orig_key] = f"${p.get(orig_key, '')}" if p.get(orig_key) else ""
                row_prices[disc_key] = f"${p.get(disc_key, '')}" if p.get(disc_key) else ""
            
            # Images
            image_urls = p.get("image_urls", [])
            image_cols = {}
            for i in range(max_images):
                col_name = f"image_{i + 1}"
                image_cols[col_name] = image_urls[i] if i < len(image_urls) else ""
            
            # Tags from brand specials
            tags = []
            if p.get("brand_special_prices"):
                for sp in p["brand_special_prices"].values():
                    if sp and sp.get("discount_label"):
                        tags.append(sp["discount_label"])
            tags_str = ", ".join(tags)
            
            # Product link
            product_link = f"/shop/menu/products/{p.get('product_id')}/{p.get('brand', '').replace(' ', '-').lower()}-{p.get('name', '').replace(' ', '-').lower()}"
            
            # Combine everything
            row = {
                "brand": p.get("brand", ""),
                "name": p.get("name", ""),
                "description": p.get("description", ""),
                "type": p.get("type", ""),
                "category": p.get("category", ""),
                "weight_options": weight_options,
                "THC_percent": thc_percent,
                "available_for_pickup": p.get("available_for_pickup", ""),
                "available_for_delivery": p.get("available_for_delivery", ""),
                "aggregate_rating": p.get("aggregate_rating", ""),
                "review_count": p.get("review_count", ""),
                **row_prices,
                **image_cols,
                "tags": tags_str,
                "product_link": product_link
            }
            
            csv_rows.append(row)
        
        # Write CSV
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=csv_fields)
            writer.writeheader()
            writer.writerows(csv_rows)
        
        logger.info(f"CSV generated with {len(csv_rows)} products: {output_file}")
        return output_file
        
    except Exception as e:
        logger.error(f"Error generating CSV: {str(e)}")
        raise