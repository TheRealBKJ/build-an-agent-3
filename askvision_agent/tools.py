"""Tools for AskVision webpage analysis."""

import json
import logging
from typing import Any, Dict, List
from bs4 import BeautifulSoup

from langchain_core.tools import tool

_LOGGER = logging.getLogger(__name__)


@tool
async def extract_reviews(html_content: str) -> Dict[str, Any]:
    """Extract review information from a webpage."""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        reviews = {
            'review_count': 0,
            'average_rating': 0,
            'review_items': [],
            'sentiment_summary': ''
        }
        
        # Look for common review selectors
        review_selectors = [
            '[data-testid*="review"]',
            '.review',
            '.reviews',
            '[class*="review"]',
            '[id*="review"]'
        ]
        
        for selector in review_selectors:
            review_elements = soup.select(selector)
            if review_elements:
                reviews['review_count'] = len(review_elements)
                
                # Extract review text
                for element in review_elements[:5]:  # Limit to first 5 reviews
                    review_text = element.get_text().strip()
                    if review_text and len(review_text) > 10:
                        reviews['review_items'].append({
                            'text': review_text[:200],
                            'length': len(review_text)
                        })
                break
        
        return reviews
    except Exception as e:
        _LOGGER.error(f"Error extracting reviews: {e}")
        return {"error": str(e)}


@tool
async def extract_pricing(html_content: str) -> Dict[str, Any]:
    """Extract pricing information from a webpage."""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        pricing = {
            'price': '',
            'currency': '',
            'original_price': '',
            'discount': '',
            'shipping': ''
        }
        
        # Look for price elements
        price_selectors = [
            '[data-testid*="price"]',
            '.price',
            '[class*="price"]',
            '[id*="price"]'
        ]
        
        for selector in price_selectors:
            price_elements = soup.select(selector)
            if price_elements:
                price_text = price_elements[0].get_text().strip()
                pricing['price'] = price_text
                break
        
        return pricing
    except Exception as e:
        _LOGGER.error(f"Error extracting pricing: {e}")
        return {"error": str(e)}


@tool
async def extract_product_info(html_content: str) -> Dict[str, Any]:
    """Extract product information from a webpage."""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        product_info = {
            'name': '',
            'description': '',
            'features': [],
            'specifications': {}
        }
        
        # Extract product name
        name_selectors = ['h1', '[data-testid*="title"]', '.product-title']
        for selector in name_selectors:
            name_element = soup.select_one(selector)
            if name_element:
                product_info['name'] = name_element.get_text().strip()
                break
        
        # Extract description
        desc_selectors = ['[data-testid*="description"]', '.description', '.product-description']
        for selector in desc_selectors:
            desc_element = soup.select_one(selector)
            if desc_element:
                product_info['description'] = desc_element.get_text().strip()[:500]
                break
        
        return product_info
    except Exception as e:
        _LOGGER.error(f"Error extracting product info: {e}")
        return {"error": str(e)}


@tool
async def extract_navigation(html_content: str) -> Dict[str, Any]:
    """Extract navigation elements from a webpage."""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        navigation = {
            'menu_items': [],
            'breadcrumbs': []
        }
        
        # Extract menu items
        nav_selectors = ['nav', '[role="navigation"]', '.navigation']
        for selector in nav_selectors:
            nav_elements = soup.select(selector)
            for nav in nav_elements:
                links = nav.find_all('a')
                for link in links:
                    text = link.get_text().strip()
                    if text:
                        navigation['menu_items'].append(text)
        
        return navigation
    except Exception as e:
        _LOGGER.error(f"Error extracting navigation: {e}")
        return {"error": str(e)}


@tool
async def extract_main_content(html_content: str) -> Dict[str, Any]:
    """Extract main content areas from a webpage."""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        content = {
            'headings': [],
            'paragraphs': [],
            'lists': []
        }
        
        # Extract headings
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            text = heading.get_text().strip()
            if text:
                content['headings'].append({
                    'level': heading.name,
                    'text': text
                })
        
        # Extract paragraphs
        for p in soup.find_all('p')[:10]:  # Limit to first 10 paragraphs
            text = p.get_text().strip()
            if text and len(text) > 20:
                content['paragraphs'].append(text[:200])
        
        return content
    except Exception as e:
        _LOGGER.error(f"Error extracting main content: {e}")
        return {"error": str(e)} 