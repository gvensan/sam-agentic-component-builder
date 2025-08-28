"""
Weather Service for Weather Trend Agent

This module provides service layer functionality for weather data operations using Open-Meteo API.
"""

import aiohttp
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone, timedelta
from solace_ai_connector.common.log import log


class WeatherService:
    """Service for fetching weather data from Open-Meteo API."""
    
    def __init__(self, 
                 forecast_url: str = "https://api.open-meteo.com/v1/forecast",
                 archive_url: str = "https://archive-api.open-meteo.com/v1/archive",
                 geocoding_url: str = "https://geocoding-api.open-meteo.com/v1/search"):
        self.forecast_url = forecast_url
        self.archive_url = archive_url
        self.geocoding_url = geocoding_url
        self.session: Optional[aiohttp.ClientSession] = None
        self.request_count = 0
    
    async def get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session."""
        if not self.session:
            self.session = aiohttp.ClientSession(
                headers={'User-Agent': 'SAM-weather_trend_agent/1.0.0'}
            )
        return self.session
    
    async def geocode_location(self, location_name: str) -> Dict[str, Any]:
        """
        Geocode a location name to get coordinates.
        
        Args:
            location_name: Name of the location (city, country, etc.)
        
        Returns:
            Dict containing geocoding information
        """
        log.info(f"[WeatherService] Geocoding location: {location_name}")
        self.request_count += 1
        
        session = await self.get_session()
        
        try:
            params = {
                "name": location_name,
                "count": 1,
                "language": "en",
                "format": "json"
            }
            
            async with session.get(self.geocoding_url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as response:
                response.raise_for_status()
                data = await response.json()
            
            if data.get("results") and len(data["results"]) > 0:
                result = data["results"][0]
                geocoding_info = {
                    "name": result.get("name"),
                    "latitude": result.get("latitude"),
                    "longitude": result.get("longitude"),
                    "country": result.get("country"),
                    "admin1": result.get("admin1"),
                    "timezone": result.get("timezone")
                }
                
                log.info(f"[WeatherService] Geocoded {location_name} to {geocoding_info['latitude']}, {geocoding_info['longitude']}")
                return {
                    "status": "success",
                    "data": geocoding_info,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            else:
                return {
                    "status": "error",
                    "message": f"Location '{location_name}' not found",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                
        except Exception as e:
            log.error(f"[WeatherService] Geocoding error: {e}")
            return {
                "status": "error",
                "message": f"Geocoding failed: {str(e)}",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    
    async def get_historical_weather(
        self, 
        latitude: float, 
        longitude: float, 
        start_date: str, 
        end_date: str,
        hourly_variables: Optional[List[str]] = None,
        daily_variables: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get historical weather data for a location.
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            hourly_variables: List of hourly variables to fetch
            daily_variables: List of daily variables to fetch
        
        Returns:
            Dict containing historical weather data
        """
        log.info(f"[WeatherService] Getting historical weather for {latitude}, {longitude} from {start_date} to {end_date}")
        self.request_count += 1
        
        session = await self.get_session()
        
        # Default variables if none specified
        if not hourly_variables and not daily_variables:
            hourly_variables = ["temperature_2m", "precipitation", "relativehumidity_2m", "windspeed_10m"]
            daily_variables = ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"]
        
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "start_date": start_date,
                "end_date": end_date,
                "timezone": "auto"
            }
            
            if hourly_variables:
                params["hourly"] = ",".join(hourly_variables)
            if daily_variables:
                params["daily"] = ",".join(daily_variables)
            
            async with session.get(self.archive_url, params=params, timeout=aiohttp.ClientTimeout(total=15)) as response:
                response.raise_for_status()
                data = await response.json()
            
            # Add metadata
            result = {
                "location": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "period": {
                    "start_date": start_date,
                    "end_date": end_date
                },
                "data": data,
                "request_count": self.request_count
            }
            
            log.info(f"[WeatherService] Successfully retrieved historical weather data")
            return {
                "status": "success",
                "data": result,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            log.error(f"[WeatherService] Historical weather error: {e}")
            return {
                "status": "error",
                "message": f"Historical weather request failed: {str(e)}",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    
    async def get_forecast_weather(
        self, 
        latitude: float, 
        longitude: float, 
        days: int = 7,
        hourly_variables: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get weather forecast for a location.
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            days: Number of forecast days (1-16)
            hourly_variables: List of hourly variables to fetch
        
        Returns:
            Dict containing forecast weather data
        """
        log.info(f"[WeatherService] Getting forecast weather for {latitude}, {longitude} for {days} days")
        self.request_count += 1
        
        session = await self.get_session()
        
        # Default variables if none specified
        if not hourly_variables:
            hourly_variables = ["temperature_2m", "precipitation", "relativehumidity_2m", "windspeed_10m"]
        
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "hourly": ",".join(hourly_variables),
                "forecast_days": min(days, 16),
                "timezone": "auto"
            }
            
            async with session.get(self.forecast_url, params=params, timeout=aiohttp.ClientTimeout(total=15)) as response:
                response.raise_for_status()
                data = await response.json()
            
            # Add metadata
            result = {
                "location": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "forecast_days": days,
                "data": data,
                "request_count": self.request_count
            }
            
            log.info(f"[WeatherService] Successfully retrieved forecast weather data")
            return {
                "status": "success",
                "data": result,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            log.error(f"[WeatherService] Forecast weather error: {e}")
            return {
                "status": "error",
                "message": f"Forecast weather request failed: {str(e)}",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    
    async def get_weather_summary(
        self, 
        latitude: float, 
        longitude: float, 
        date: str
    ) -> Dict[str, Any]:
        """
        Get weather summary for a specific date.
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            date: Date (YYYY-MM-DD)
        
        Returns:
            Dict containing weather summary
        """
        log.info(f"[WeatherService] Getting weather summary for {latitude}, {longitude} on {date}")
        
        result = await self.get_historical_weather(
            latitude=latitude,
            longitude=longitude,
            start_date=date,
            end_date=date,
            daily_variables=["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "windspeed_10m_max"]
        )
        
        if result["status"] == "success":
            # Extract summary data
            daily_data = result["data"]["data"].get("daily", {})
            if daily_data:
                summary = {
                    "date": date,
                    "max_temperature": daily_data.get("temperature_2m_max", [None])[0],
                    "min_temperature": daily_data.get("temperature_2m_min", [None])[0],
                    "total_precipitation": daily_data.get("precipitation_sum", [None])[0],
                    "max_wind_speed": daily_data.get("windspeed_10m_max", [None])[0]
                }
                result["data"]["summary"] = summary
        
        return result
