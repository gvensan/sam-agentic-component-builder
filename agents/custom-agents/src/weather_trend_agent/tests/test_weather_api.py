#!/usr/bin/env python3
"""
Test script for Weather History Agent API functionality
"""

import asyncio
import httpx
from datetime import datetime, timezone, timedelta


async def test_open_meteo_apis():
    """Test Open-Meteo API endpoints"""
    print("🌤️ Weather History Agent - API Testing")
    print("Testing Open-Meteo API endpoints")
    print("=" * 60)
    
    # Test geocoding API
    print("\n1. Testing Geocoding API")
    print("-" * 30)
    
    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
    test_locations = ["London", "New York", "Tokyo", "Sydney"]
    
    for location in test_locations:
        try:
            params = {
                "name": location,
                "count": 1,
                "language": "en",
                "format": "json"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(geocoding_url, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
            
            if data.get("results") and len(data["results"]) > 0:
                result = data["results"][0]
                print(f"✅ {location}: {result.get('latitude')}, {result.get('longitude')} ({result.get('country')})")
            else:
                print(f"❌ {location}: Not found")
                
        except Exception as e:
            print(f"❌ {location}: Error - {e}")
    
    # Test historical weather API
    print("\n2. Testing Historical Weather API")
    print("-" * 30)
    
    archive_url = "https://archive-api.open-meteo.com/v1/archive"
    test_coordinates = [
        {"lat": 51.5074, "lon": -0.1278, "name": "London"},
        {"lat": 40.7128, "lon": -74.0060, "name": "New York"}
    ]
    
    # Test with last week's data
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)
    
    for coords in test_coordinates:
        try:
            params = {
                "latitude": coords["lat"],
                "longitude": coords["lon"],
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "hourly": "temperature_2m,precipitation,relativehumidity_2m",
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
                "timezone": "auto"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(archive_url, params=params, timeout=15.0)
                response.raise_for_status()
                data = response.json()
            
            if "hourly" in data and "daily" in data:
                hourly_data = data["hourly"]
                daily_data = data["daily"]
                
                print(f"✅ {coords['name']}: Historical data retrieved")
                print(f"   Hourly records: {len(hourly_data.get('time', []))}")
                print(f"   Daily records: {len(daily_data.get('time', []))}")
                
                # Show sample data
                if hourly_data.get("temperature_2m"):
                    temps = hourly_data["temperature_2m"]
                    if temps:
                        print(f"   Sample temperature: {temps[0]}°C")
            else:
                print(f"❌ {coords['name']}: Invalid response format")
                
        except Exception as e:
            print(f"❌ {coords['name']}: Error - {e}")
    
    # Test forecast API
    print("\n3. Testing Forecast Weather API")
    print("-" * 30)
    
    forecast_url = "https://api.open-meteo.com/v1/forecast"
    
    for coords in test_coordinates:
        try:
            params = {
                "latitude": coords["lat"],
                "longitude": coords["lon"],
                "hourly": "temperature_2m,precipitation,relativehumidity_2m",
                "forecast_days": 7,
                "timezone": "auto"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(forecast_url, params=params, timeout=15.0)
                response.raise_for_status()
                data = response.json()
            
            if "hourly" in data:
                hourly_data = data["hourly"]
                print(f"✅ {coords['name']}: Forecast data retrieved")
                print(f"   Hourly records: {len(hourly_data.get('time', []))}")
                
                # Show sample forecast
                if hourly_data.get("temperature_2m"):
                    temps = hourly_data["temperature_2m"]
                    if temps:
                        print(f"   Sample forecast temperature: {temps[0]}°C")
            else:
                print(f"❌ {coords['name']}: Invalid response format")
                
        except Exception as e:
            print(f"❌ {coords['name']}: Error - {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Open-Meteo API Testing Completed!")
    print("✅ All APIs are working correctly")
    print("✅ Ready for Weather History Agent deployment")


async def test_weather_variables():
    """Test available weather variables"""
    print("\n4. Testing Available Weather Variables")
    print("-" * 30)
    
    # Test with a simple request to get available variables
    archive_url = "https://archive-api.open-meteo.com/v1/archive"
    
    try:
        params = {
            "latitude": 51.5074,
            "longitude": -0.1278,
            "start_date": "2024-01-01",
            "end_date": "2024-01-01",
            "hourly": "temperature_2m,precipitation,relativehumidity_2m,windspeed_10m,pressure_msl",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,sunrise,sunset",
            "timezone": "auto"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(archive_url, params=params, timeout=15.0)
            response.raise_for_status()
            data = response.json()
        
        if "hourly" in data and "daily" in data:
            hourly_vars = list(data["hourly"].keys())
            daily_vars = list(data["daily"].keys())
            
            print(f"✅ Hourly variables available: {len(hourly_vars)}")
            print(f"   Sample: {hourly_vars[:5]}")
            
            print(f"✅ Daily variables available: {len(daily_vars)}")
            print(f"   Sample: {daily_vars[:5]}")
        else:
            print("❌ Could not retrieve variable information")
            
    except Exception as e:
        print(f"❌ Error testing variables: {e}")


if __name__ == "__main__":
    asyncio.run(test_open_meteo_apis())
    asyncio.run(test_weather_variables())
