"""
Exchange Rate Service for API communication
"""

import os
import httpx
import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ExchangeRateService:
    """Service for communicating with the Exchange Rate API"""
    
    def __init__(self, api_key: str, base_url: str = None, timeout: int = None):
        """
        Initialize the Exchange Rate Service
        
        Args:
            api_key: API key for authentication
            base_url: Base URL for the API (defaults to environment variable)
            timeout: Request timeout in seconds (defaults to environment variable)
        """
        self.api_key = api_key
        self.base_url = (base_url or os.getenv('EXCHANGE_RATE_API_BASE_URL', 'https://v6.exchangerate-api.com/v6')).rstrip('/')
        self.timeout = timeout or int(os.getenv('EXCHANGE_RATE_API_TIMEOUT', '30'))
        self.client = httpx.AsyncClient(timeout=self.timeout)
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
        
    async def get_latest_rates(self, base_currency: str) -> Dict[str, Any]:
        """
        Get latest exchange rates for a base currency
        
        Args:
            base_currency: Base currency code (e.g., 'USD', 'EUR')
            
        Returns:
            Dict with exchange rates data
        """
        try:
            url = f"{self.base_url}/{self.api_key}/latest/{base_currency.upper()}"
            
            logger.info(f"🌐 Fetching latest rates for {base_currency}")
            response = await self.client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Successfully fetched rates for {base_currency}")
                return {
                    "status": "success",
                    "data": data,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                error_data = response.json() if response.content else {"error": "Unknown error"}
                logger.error(f"❌ API error: {response.status_code} - {error_data}")
                return {
                    "status": "error",
                    "error": f"API request failed: {response.status_code}",
                    "error_type": error_data.get("error-type", "unknown"),
                    "timestamp": datetime.now().isoformat()
                }
                
        except httpx.TimeoutException:
            logger.error(f"⏰ Timeout while fetching rates for {base_currency}")
            return {
                "status": "error",
                "error": "Request timeout - API is not responding",
                "error_type": "timeout",
                "timestamp": datetime.now().isoformat()
            }
        except httpx.RequestError as e:
            logger.error(f"🌐 Network error while fetching rates for {base_currency}: {str(e)}")
            return {
                "status": "error",
                "error": f"Network error: {str(e)}",
                "error_type": "network_error",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Unexpected error while fetching rates for {base_currency}: {str(e)}")
            return {
                "status": "error",
                "error": f"Unexpected error: {str(e)}",
                "error_type": "unexpected_error",
                "timestamp": datetime.now().isoformat()
            }
            
    async def convert_currency(self, from_currency: str, to_currency: str, amount: float) -> Dict[str, Any]:
        """
        Convert amount from one currency to another
        
        Args:
            from_currency: Source currency code
            to_currency: Target currency code
            amount: Amount to convert
            
        Returns:
            Dict with conversion result
        """
        try:
            url = f"{self.base_url}/{self.api_key}/pair/{from_currency.upper()}/{to_currency.upper()}/{amount}"
            
            logger.info(f"💱 Converting {amount} {from_currency} to {to_currency}")
            response = await self.client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Successfully converted {amount} {from_currency} to {to_currency}")
                return {
                    "status": "success",
                    "data": data,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                error_data = response.json() if response.content else {"error": "Unknown error"}
                logger.error(f"❌ API error: {response.status_code} - {error_data}")
                return {
                    "status": "error",
                    "error": f"API request failed: {response.status_code}",
                    "error_type": error_data.get("error-type", "unknown"),
                    "timestamp": datetime.now().isoformat()
                }
                
        except httpx.TimeoutException:
            logger.error(f"⏰ Timeout while converting {amount} {from_currency} to {to_currency}")
            return {
                "status": "error",
                "error": "Request timeout - API is not responding",
                "error_type": "timeout",
                "timestamp": datetime.now().isoformat()
            }
        except httpx.RequestError as e:
            logger.error(f"🌐 Network error while converting {amount} {from_currency} to {to_currency}: {str(e)}")
            return {
                "status": "error",
                "error": f"Network error: {str(e)}",
                "error_type": "network_error",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Unexpected error while converting {amount} {from_currency} to {to_currency}: {str(e)}")
            return {
                "status": "error",
                "error": f"Unexpected error: {str(e)}",
                "error_type": "unexpected_error",
                "timestamp": datetime.now().isoformat()
            }
            
    async def get_quota_info(self) -> Dict[str, Any]:
        """
        Get API quota information
        
        Returns:
            Dict with quota information
        """
        try:
            url = f"{self.base_url}/{self.api_key}/quota"
            
            logger.info("📊 Fetching API quota information")
            response = await self.client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                logger.info("✅ Successfully fetched quota information")
                return {
                    "status": "success",
                    "data": data,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                error_data = response.json() if response.content else {"error": "Unknown error"}
                logger.error(f"❌ API error: {response.status_code} - {error_data}")
                return {
                    "status": "error",
                    "error": f"API request failed: {response.status_code}",
                    "error_type": error_data.get("error-type", "unknown"),
                    "timestamp": datetime.now().isoformat()
                }
                
        except httpx.TimeoutException:
            logger.error("⏰ Timeout while fetching quota information")
            return {
                "status": "error",
                "error": "Request timeout - API is not responding",
                "error_type": "timeout",
                "timestamp": datetime.now().isoformat()
            }
        except httpx.RequestError as e:
            logger.error(f"🌐 Network error while fetching quota information: {str(e)}")
            return {
                "status": "error",
                "error": f"Network error: {str(e)}",
                "error_type": "network_error",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"❌ Unexpected error while fetching quota information: {str(e)}")
            return {
                "status": "error",
                "error": f"Unexpected error: {str(e)}",
                "error_type": "unexpected_error",
                "timestamp": datetime.now().isoformat()
            }
