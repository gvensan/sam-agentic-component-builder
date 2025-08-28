"""
IP Service for Find My IP Agent

This module provides service layer functionality for IP address operations.
"""

import aiohttp
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from solace_ai_connector.common.log import log


class IPService:
    """Service for fetching IP address data from external APIs."""
    
    def __init__(self, ipify_url: str = "https://api.ipify.org?format=json", 
                 location_url: str = "https://ipapi.co"):
        self.ipify_url = ipify_url
        self.location_url = location_url
        self.session: Optional[aiohttp.ClientSession] = None
        self.request_count = 0
    
    async def get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session."""
        if not self.session:
            self.session = aiohttp.ClientSession(
                headers={'User-Agent': 'SAM-find_my_ip_agent/1.0.0'}
            )
        return self.session
    
    async def get_current_ip(self) -> Dict[str, Any]:
        """
        Get current IP address from IPify API.
        
        Returns:
            Dict containing IP address information
        """
        log.info("[IPService] Getting current IP address")
        self.request_count += 1
        
        session = await self.get_session()
        
        try:
            async with session.get(self.ipify_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                response.raise_for_status()
                data = await response.json()
            
            ip_address = data.get("ip")
            if not ip_address:
                raise ValueError("No IP address found in API response")
            
            result = {
                "status": "success",
                "ip_address": ip_address,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "source": "ipify-api",
                "request_count": self.request_count
            }
            
            log.info(f"[IPService] Successfully retrieved IP: {ip_address}")
            return result
            
        except aiohttp.ClientError as e:
            log.error(f"[IPService] Network error: {e}")
            return {
                "status": "error",
                "message": f"Network error: {str(e)}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "error_type": "network_error"
            }
        except Exception as e:
            log.error(f"[IPService] Error getting IP: {e}")
            return {
                "status": "error",
                "message": f"Service error: {str(e)}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "error_type": "service_error"
            }
    
    async def get_ip_location(self, ip_address: str) -> Dict[str, Any]:
        """
        Get location information for an IP address.
        
        Args:
            ip_address: The IP address to look up
        
        Returns:
            Dict containing location information
        """
        log.info(f"[IPService] Getting location for IP: {ip_address}")
        
        session = await self.get_session()
        url = f"{self.location_url}/{ip_address}/json/"
        
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                response.raise_for_status()
                data = await response.json()
            
            location_info = {
                "country": data.get("country_name"),
                "region": data.get("region"),
                "city": data.get("city"),
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude"),
                "timezone": data.get("timezone"),
                "isp": data.get("org"),
                "postal_code": data.get("postal")
            }
            
            return {
                "status": "success",
                "data": location_info,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            log.error(f"[IPService] Error getting location for {ip_address}: {e}")
            return {
                "status": "error",
                "message": f"Location lookup failed: {str(e)}",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    
    async def get_comprehensive_ip_info(self) -> Dict[str, Any]:
        """
        Get comprehensive IP information including location.
        
        Returns:
            Dict containing IP address and location information
        """
        log.info("[IPService] Getting comprehensive IP information")
        
        # Get basic IP information
        ip_result = await self.get_current_ip()
        
        if ip_result["status"] != "success":
            return ip_result
        
        # Get location information
        location_result = await self.get_ip_location(ip_result["ip_address"])
        
        result = {
            "status": "success",
            "ip_address": ip_result["ip_address"],
            "timestamp": ip_result["timestamp"],
            "source": ip_result["source"],
            "request_count": ip_result["request_count"],
            "location_info": location_result.get("data") if location_result["status"] == "success" else None,
            "location_error": location_result.get("message") if location_result["status"] != "success" else None
        }
        
        return result
    
    async def close(self):
        """Close the service session."""
        if self.session:
            await self.session.close()
            log.info("[IPService] Session closed")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get service statistics."""
        return {
            "request_count": self.request_count,
            "session_active": self.session is not None,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
