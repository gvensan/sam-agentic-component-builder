"""
Country Service for Country Information Agent

This module provides service layer functionality for country data operations using REST Countries API.
"""

import asyncio
import aiohttp
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
from solace_ai_connector.common.log import log


class CountryService:
    """Service class for interacting with REST Countries API"""
    
    def __init__(self):
        self.base_url = "https://restcountries.com/v3.1"
        self.session: Optional[aiohttp.ClientSession] = None
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.cache_duration = timedelta(hours=24)  # Cache for 24 hours
        self.last_cache_cleanup = datetime.now()
        
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session"""
        if not self.session:
            self.session = aiohttp.ClientSession(
                headers={'User-Agent': 'SAM-country_information_agent/1.0.0'}
            )
        return self.session
    
    async def _cleanup_cache(self):
        """Clean up expired cache entries"""
        now = datetime.now()
        if now - self.last_cache_cleanup > timedelta(hours=1):
            expired_keys = []
            for key, data in self.cache.items():
                if 'cached_at' in data:
                    cached_time = datetime.fromisoformat(data['cached_at'])
                    if now - cached_time > self.cache_duration:
                        expired_keys.append(key)
            
            for key in expired_keys:
                del self.cache[key]
            
            self.last_cache_cleanup = now
    
    async def _make_request(self, endpoint: str) -> Dict[str, Any]:
        """Make HTTP request to REST Countries API"""
        session = await self._get_session()
        url = f"{self.base_url}/{endpoint}"
        
        try:
            async with session.get(url, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    return {"status": "success", "data": data}
                elif response.status == 404:
                    return {"status": "error", "error": "Country not found"}
                else:
                    return {"status": "error", "error": f"API error: {response.status}"}
        except asyncio.TimeoutError:
            return {"status": "error", "error": "Request timeout"}
        except Exception as e:
            return {"status": "error", "error": f"Request failed: {str(e)}"}
    
    async def get_country_by_name(self, country_name: str) -> Dict[str, Any]:
        """Get country information by name"""
        await self._cleanup_cache()
        
        # Check cache first
        cache_key = f"country_{country_name.lower()}"
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            cached_time = datetime.fromisoformat(cached_data['cached_at'])
            if datetime.now() - cached_time < self.cache_duration:
                return {"status": "success", "data": cached_data['data'], "cached": True}
        
        # Make API request
        result = await self._make_request(f"name/{country_name}")
        
        if result["status"] == "success":
            # Cache the result
            self.cache[cache_key] = {
                "data": result["data"],
                "cached_at": datetime.now().isoformat()
            }
        
        return result
    
    async def search_countries(self, search_term: str) -> Dict[str, Any]:
        """Search countries by name"""
        await self._cleanup_cache()
        
        # Check cache first
        cache_key = f"search_{search_term.lower()}"
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            cached_time = datetime.fromisoformat(cached_data['cached_at'])
            if datetime.now() - cached_time < self.cache_duration:
                return {"status": "success", "data": cached_data['data'], "cached": True}
        
        # Make API request
        result = await self._make_request(f"name/{search_term}")
        
        if result["status"] == "success":
            # Cache the result
            self.cache[cache_key] = {
                "data": result["data"],
                "cached_at": datetime.now().isoformat()
            }
        
        return result
    
    async def get_country_by_code(self, country_code: str) -> Dict[str, Any]:
        """Get country information by ISO code"""
        await self._cleanup_cache()
        
        # Check cache first
        cache_key = f"code_{country_code.lower()}"
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            cached_time = datetime.fromisoformat(cached_data['cached_at'])
            if datetime.now() - cached_time < self.cache_duration:
                return {"status": "success", "data": cached_data['data'], "cached": True}
        
        # Make API request
        result = await self._make_request(f"alpha/{country_code}")
        
        if result["status"] == "success":
            # Cache the result
            self.cache[cache_key] = {
                "data": result["data"],
                "cached_at": datetime.now().isoformat()
            }
        
        return result
    
    async def get_all_countries(self) -> Dict[str, Any]:
        """Get all countries"""
        await self._cleanup_cache()
        
        # Check cache first
        cache_key = "all_countries"
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            cached_time = datetime.fromisoformat(cached_data['cached_at'])
            if datetime.now() - cached_time < self.cache_duration:
                return {"status": "success", "data": cached_data['data'], "cached": True}
        
        # Make API request
        result = await self._make_request("all")
        
        if result["status"] == "success":
            # Cache the result
            self.cache[cache_key] = {
                "data": result["data"],
                "cached_at": datetime.now().isoformat()
            }
        
        return result
    
    async def get_countries_by_region(self, region: str) -> Dict[str, Any]:
        """Get countries by region"""
        await self._cleanup_cache()
        
        # Check cache first
        cache_key = f"region_{region.lower()}"
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            cached_time = datetime.fromisoformat(cached_data['cached_at'])
            if datetime.now() - cached_time < self.cache_duration:
                return {"status": "success", "data": cached_data['data'], "cached": True}
        
        # Make API request
        result = await self._make_request(f"region/{region}")
        
        if result["status"] == "success":
            # Cache the result
            self.cache[cache_key] = {
                "data": result["data"],
                "cached_at": datetime.now().isoformat()
            }
        
        return result
    
    async def close(self):
        """Close the HTTP session"""
        if self.session:
            await self.session.close()
            self.session = None


# Global service instance
_country_service: Optional[CountryService] = None


async def get_country_service() -> CountryService:
    """Get or create the global country service instance"""
    global _country_service
    if _country_service is None:
        _country_service = CountryService()
    return _country_service


async def close_country_service():
    """Close the global country service instance"""
    global _country_service
    if _country_service:
        await _country_service.close()
        _country_service = None
