import os
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup, Tag
import re
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate
import json

class SectionAuthorAgent:
    """
    AskVision Section Author Agent
    
    This agent can:
    1. Parse and structure any webpage's HTML
    2. Build semantic sections (reviews, pricing, headers)
    3. Answer natural language questions about the page content
    4. Provide intelligent, conversational responses
    """
    
    def __init__(self):
        """Initialize the agent with NVIDIA AI endpoints"""
        self.llm = ChatNVIDIA(
            model="nemotron-3-8b-chat-4k",
            temperature=0.1,
            max_tokens=2048
        )
        
        # Initialize section extractors
        self.section_extractors = {
            'reviews': self._extract_reviews,
            'pricing': self._extract_pricing,
            'product_info': self._extract_product_info,
            'navigation': self._extract_navigation,
            'content': self._extract_main_content
        }
    
    def parse_and_structure(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Parse HTML and extract structured sections
        
        Args:
            soup: BeautifulSoup object of the webpage
            
        Returns:
            Dictionary with structured content sections
        """
        structured_content = {
            'url': '',
            'title': '',
            'sections': {},
            'metadata': {}
        }
        
        # Extract basic page info
        structured_content['title'] = soup.find('title').get_text().strip() if soup.find('title') else ''
        
        # Extract different sections
        for section_name, extractor in self.section_extractors.items():
            try:
                section_content = extractor(soup)
                if section_content:
                    structured_content['sections'][section_name] = section_content
            except Exception as e:
                print(f"Error extracting {section_name}: {e}")
        
        # Add metadata
        structured_content['metadata'] = {
            'total_sections': len(structured_content['sections']),
            'has_reviews': 'reviews' in structured_content['sections'],
            'has_pricing': 'pricing' in structured_content['sections'],
            'has_product_info': 'product_info' in structured_content['sections']
        }
        
        return structured_content
    
    def answer_question(self, question: str, structured_content: Dict[str, Any]) -> str:
        """
        Answer a question about the structured content
        
        Args:
            question: User's question
            structured_content: Structured content from parse_and_structure
            
        Returns:
            Intelligent answer to the question
        """
        # Create a context string from the structured content
        context = self._create_context_string(structured_content)
        
        # Create the prompt
        prompt = f"""
You are AskVision, an AI assistant that helps visually impaired users understand web content. 
You have access to structured information from a webpage. Answer the user's question in a clear, 
helpful, and conversational way. Focus on being accessible and providing actionable information.

Webpage Context:
{context}

User Question: {question}

Please provide a clear, helpful answer that would be useful for someone using a screen reader:
"""
        
        # Get response from LLM
        messages = [
            SystemMessage(content="You are AskVision, an accessibility-focused AI assistant that helps visually impaired users understand web content."),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def process_and_answer(self, url: str, soup: BeautifulSoup, question: str) -> str:
        """
        Process a webpage and answer a question in one step
        
        Args:
            url: The webpage URL
            soup: BeautifulSoup object of the webpage
            question: User's question
            
        Returns:
            Answer to the question
        """
        # Parse and structure the content
        structured_content = self.parse_and_structure(soup)
        structured_content['url'] = url
        
        # Answer the question
        return self.answer_question(question, structured_content)
    
    def _create_context_string(self, structured_content: Dict[str, Any]) -> str:
        """Create a context string from structured content"""
        context_parts = []
        
        # Add title
        if structured_content.get('title'):
            context_parts.append(f"Page Title: {structured_content['title']}")
        
        # Add sections
        for section_name, section_content in structured_content.get('sections', {}).items():
            if isinstance(section_content, dict):
                # Handle structured section content
                section_text = self._format_section_content(section_content)
            else:
                # Handle simple text content
                section_text = str(section_content)[:500] + "..." if len(str(section_content)) > 500 else str(section_content)
            
            context_parts.append(f"{section_name.title()}: {section_text}")
        
        return "\n\n".join(context_parts)
    
    def _format_section_content(self, section_content: Dict[str, Any]) -> str:
        """Format section content for context"""
        if isinstance(section_content, dict):
            formatted_parts = []
            for key, value in section_content.items():
                if isinstance(value, list):
                    formatted_parts.append(f"{key}: {len(value)} items")
                    for i, item in enumerate(value[:3]):  # Limit to first 3 items
                        formatted_parts.append(f"  {i+1}. {str(item)[:100]}")
                else:
                    formatted_parts.append(f"{key}: {str(value)[:200]}")
            return "\n".join(formatted_parts)
        return str(section_content)
    
    def _extract_reviews(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract review information from the page"""
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
    
    def _extract_pricing(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract pricing information from the page"""
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
    
    def _extract_product_info(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract product information from the page"""
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
    
    def _extract_navigation(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract navigation elements"""
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
    
    def _extract_main_content(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract main content areas"""
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