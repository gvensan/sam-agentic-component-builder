"""
Weather Trend Agent Tools

This module contains the tools for the Weather Trend Agent following SAM patterns.
"""

import httpx
from typing import Any, Dict, Optional, List
from datetime import datetime, timezone, timedelta
from google.adk.tools import ToolContext
from solace_ai_connector.common.log import log
from .services.weather_service import WeatherService


# Global weather service instance
weather_service = WeatherService()


async def geocode_location(
    location_name: str,
    tool_context: Optional[ToolContext] = None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Geocode a location name to get coordinates.
    
    Args:
        location_name: Name of the location (e.g., "London", "New York", "Tokyo")
    
    Returns:
        Dict containing geocoding information with coordinates
    """
    log.info(f"[GeocodeLocation] Geocoding location: {location_name}")
    
    try:
        result = await weather_service.geocode_location(location_name)
        
        if result["status"] == "success":
            data = result["data"]
            return {
                "status": "success",
                "location_name": location_name,
                "coordinates": {
                    "latitude": data["latitude"],
                    "longitude": data["longitude"]
                },
                "details": {
                    "name": data["name"],
                    "country": data["country"],
                    "admin1": data["admin1"],
                    "timezone": data["timezone"]
                },
                "timestamp": result["timestamp"],
                "source": "open-meteo-geocoding"
            }
        else:
            return {
                "status": "error",
                "message": result["message"],
                "location_name": location_name,
                "timestamp": result["timestamp"]
            }
            
    except Exception as e:
        log.error(f"[GeocodeLocation] Error: {e}")
        return {
            "status": "error",
            "message": f"Geocoding failed: {str(e)}",
            "location_name": location_name,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


async def get_historical_weather_by_coordinates(
    latitude: float,
    longitude: float,
    start_date: str,
    end_date: str,
    hourly_variables: Optional[List[str]] = None,
    daily_variables: Optional[List[str]] = None,
    tool_context: Optional[ToolContext] = None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Get historical weather data for a location using coordinates.
    
    Args:
        latitude: Location latitude (-90 to 90)
        longitude: Location longitude (-180 to 180)
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        hourly_variables: List of hourly variables (optional)
        daily_variables: List of daily variables (optional)
    
    Returns:
        Dict containing historical weather data
    """
    log.info(f"[GetHistoricalWeather] Getting historical weather for {latitude}, {longitude} from {start_date} to {end_date}")
    
    try:
        result = await weather_service.get_historical_weather(
            latitude=latitude,
            longitude=longitude,
            start_date=start_date,
            end_date=end_date,
            hourly_variables=hourly_variables,
            daily_variables=daily_variables
        )
        
        if result["status"] == "success":
            data = result["data"]
            return {
                "status": "success",
                "location": data["location"],
                "period": data["period"],
                "weather_data": data["data"],
                "variables": {
                    "hourly": hourly_variables or ["temperature_2m", "precipitation", "relativehumidity_2m", "windspeed_10m"],
                    "daily": daily_variables or ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"]
                },
                "timestamp": result["timestamp"],
                "source": "open-meteo-archive"
            }
        else:
            return {
                "status": "error",
                "message": result["message"],
                "coordinates": {"latitude": latitude, "longitude": longitude},
                "period": {"start_date": start_date, "end_date": end_date},
                "timestamp": result["timestamp"]
            }
            
    except Exception as e:
        log.error(f"[GetHistoricalWeather] Error: {e}")
        return {
            "status": "error",
            "message": f"Historical weather request failed: {str(e)}",
            "coordinates": {"latitude": latitude, "longitude": longitude},
            "period": {"start_date": start_date, "end_date": end_date},
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


async def get_historical_weather_by_location(
    location_name: str,
    start_date: str,
    end_date: str,
    hourly_variables: Optional[List[str]] = None,
    daily_variables: Optional[List[str]] = None,
    tool_context: Optional[ToolContext] = None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Get historical weather data for a location by name.
    
    Args:
        location_name: Name of the location (e.g., "London", "New York")
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        hourly_variables: List of hourly variables (optional)
        daily_variables: List of daily variables (optional)
    
    Returns:
        Dict containing historical weather data
    """
    log.info(f"[GetHistoricalWeatherByLocation] Getting historical weather for {location_name} from {start_date} to {end_date}")
    
    try:
        # First geocode the location
        geocode_result = await weather_service.geocode_location(location_name)
        
        if geocode_result["status"] != "success":
            return {
                "status": "error",
                "message": f"Location '{location_name}' not found: {geocode_result['message']}",
                "location_name": location_name,
                "timestamp": geocode_result["timestamp"]
            }
        
        # Get coordinates from geocoding result
        coords = geocode_result["data"]
        
        # Get historical weather data
        weather_result = await weather_service.get_historical_weather(
            latitude=coords["latitude"],
            longitude=coords["longitude"],
            start_date=start_date,
            end_date=end_date,
            hourly_variables=hourly_variables,
            daily_variables=daily_variables
        )
        
        if weather_result["status"] == "success":
            data = weather_result["data"]
            return {
                "status": "success",
                "location": {
                    "name": location_name,
                    "coordinates": data["location"],
                    "country": coords["country"],
                    "timezone": coords["timezone"]
                },
                "period": data["period"],
                "weather_data": data["data"],
                "variables": {
                    "hourly": hourly_variables or ["temperature_2m", "precipitation", "relativehumidity_2m", "windspeed_10m"],
                    "daily": daily_variables or ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"]
                },
                "timestamp": weather_result["timestamp"],
                "source": "open-meteo-archive"
            }
        else:
            return {
                "status": "error",
                "message": weather_result["message"],
                "location_name": location_name,
                "coordinates": {"latitude": coords["latitude"], "longitude": coords["longitude"]},
                "period": {"start_date": start_date, "end_date": end_date},
                "timestamp": weather_result["timestamp"]
            }
            
    except Exception as e:
        log.error(f"[GetHistoricalWeatherByLocation] Error: {e}")
        return {
            "status": "error",
            "message": f"Weather request failed: {str(e)}",
            "location_name": location_name,
            "period": {"start_date": start_date, "end_date": end_date},
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


async def get_weather_summary_by_date(
    latitude: float,
    longitude: float,
    date: str,
    tool_context: Optional[ToolContext] = None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Get weather summary for a specific date.
    
    Args:
        latitude: Location latitude (-90 to 90)
        longitude: Location longitude (-180 to 180)
        date: Date in YYYY-MM-DD format
    
    Returns:
        Dict containing weather summary for the date
    """
    log.info(f"[GetWeatherSummary] Getting weather summary for {latitude}, {longitude} on {date}")
    
    try:
        result = await weather_service.get_weather_summary(
            latitude=latitude,
            longitude=longitude,
            date=date
        )
        
        if result["status"] == "success":
            data = result["data"]
            summary = data.get("summary", {})
            
            return {
                "status": "success",
                "location": data["location"],
                "date": date,
                "summary": {
                    "max_temperature": summary.get("max_temperature"),
                    "min_temperature": summary.get("min_temperature"),
                    "total_precipitation": summary.get("total_precipitation"),
                    "max_wind_speed": summary.get("max_wind_speed")
                },
                "full_data": data["data"],
                "timestamp": result["timestamp"],
                "source": "open-meteo-archive"
            }
        else:
            return {
                "status": "error",
                "message": result["message"],
                "coordinates": {"latitude": latitude, "longitude": longitude},
                "date": date,
                "timestamp": result["timestamp"]
            }
            
    except Exception as e:
        log.error(f"[GetWeatherSummary] Error: {e}")
        return {
            "status": "error",
            "message": f"Weather summary request failed: {str(e)}",
            "coordinates": {"latitude": latitude, "longitude": longitude},
            "date": date,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


async def get_forecast_weather(
    latitude: float,
    longitude: float,
    days: int = 7,
    hourly_variables: Optional[List[str]] = None,
    tool_context: Optional[ToolContext] = None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Get weather forecast for a location.
    
    Args:
        latitude: Location latitude (-90 to 90)
        longitude: Location longitude (-180 to 180)
        days: Number of forecast days (1-16, default: 7)
        hourly_variables: List of hourly variables (optional)
    
    Returns:
        Dict containing forecast weather data
    """
    log.info(f"[GetForecastWeather] Getting forecast weather for {latitude}, {longitude} for {days} days")
    
    try:
        result = await weather_service.get_forecast_weather(
            latitude=latitude,
            longitude=longitude,
            days=days,
            hourly_variables=hourly_variables
        )
        
        if result["status"] == "success":
            data = result["data"]
            return {
                "status": "success",
                "location": data["location"],
                "forecast_days": data["forecast_days"],
                "weather_data": data["data"],
                "variables": {
                    "hourly": hourly_variables or ["temperature_2m", "precipitation", "relativehumidity_2m", "windspeed_10m"]
                },
                "timestamp": result["timestamp"],
                "source": "open-meteo-forecast"
            }
        else:
            return {
                "status": "error",
                "message": result["message"],
                "coordinates": {"latitude": latitude, "longitude": longitude},
                "forecast_days": days,
                "timestamp": result["timestamp"]
            }
            
    except Exception as e:
        log.error(f"[GetForecastWeather] Error: {e}")
        return {
            "status": "error",
            "message": f"Forecast weather request failed: {str(e)}",
            "coordinates": {"latitude": latitude, "longitude": longitude},
            "forecast_days": days,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


async def get_available_weather_variables(
    tool_context: Optional[ToolContext] = None,
    tool_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Get list of available weather variables for Open-Meteo API.
    
    Returns:
        Dict containing available weather variables
    """
    log.info(f"[GetAvailableWeatherVariables] Getting available weather variables")
    
    variables = {
        "hourly_variables": [
            "temperature_2m",
            "temperature_80m", 
            "temperature_120m",
            "relativehumidity_2m",
            "dewpoint_2m",
            "apparent_temperature",
            "precipitation",
            "rain",
            "snowfall",
            "weathercode",
            "pressure_msl",
            "surface_pressure",
            "cloudcover",
            "cloudcover_low",
            "cloudcover_mid",
            "cloudcover_high",
            "evapotranspiration",
            "et0_fao_evapotranspiration",
            "vapor_pressure_deficit",
            "windspeed_10m",
            "windspeed_80m",
            "windspeed_120m",
            "winddirection_10m",
            "winddirection_80m",
            "winddirection_120m",
            "windgusts_10m",
            "shortwave_radiation",
            "direct_radiation",
            "diffuse_radiation",
            "direct_normal_irradiance",
            "terrestrial_radiation",
            "shortwave_radiation_instant",
            "direct_radiation_instant",
            "diffuse_radiation_instant",
            "terrestrial_radiation_instant"
        ],
        "daily_variables": [
            "temperature_2m_max",
            "temperature_2m_min",
            "apparent_temperature_max",
            "apparent_temperature_min",
            "precipitation_sum",
            "rain_sum",
            "snowfall_sum",
            "precipitation_hours",
            "weathercode",
            "sunrise",
            "sunset",
            "windspeed_10m_max",
            "windgusts_10m_max",
            "winddirection_10m_dominant",
            "shortwave_radiation_sum",
            "et0_fao_evapotranspiration"
        ]
    }
    
    return {
        "status": "success",
        "variables": variables,
        "description": "Available weather variables for Open-Meteo API",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": "open-meteo-documentation"
    }
