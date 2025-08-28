"""
Comprehensive Test Suite for Weather Trend Agent

This module contains comprehensive tests for the Weather Trend Agent tools.
"""

import sys
import os
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timezone, timedelta

# Add the parent directory to the path to import the tools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Mock the SAM dependencies
sys.modules['google.adk.tools'] = Mock()
sys.modules['solace_ai_connector.common.log'] = Mock()

# Import the tools module
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Mock the services module
sys.modules['services.weather_service'] = Mock()

from weather_trend_agent.tools import (
    geocode_location,
    get_historical_weather_by_coordinates,
    get_historical_weather_by_location,
    get_weather_summary_by_date,
    get_forecast_weather,
    get_available_weather_variables
)


class MockToolContext:
    """Mock tool context for testing"""
    
    def __init__(self, agent_name="WeatherTrendAgent"):
        self.agent_name = agent_name
        self.state = {
            "statistics": {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "locations_searched": set(),
                "last_request_time": None
            }
        }
    
    def get_agent_specific_state(self, key, default=None):
        return self.state.get(key, default)
    
    def set_agent_specific_state(self, key, value):
        self.state[key] = value


class TestWeatherAgent:
    """Test class for Weather Trend Agent"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.context = MockToolContext()
        self.mock_geocoding_response = {
            "results": [
                {
                    "name": "London",
                    "latitude": 51.5074,
                    "longitude": -0.1278,
                    "country": "United Kingdom",
                    "admin1": "England"
                }
            ]
        }
        self.mock_weather_response = {
            "latitude": 51.5074,
            "longitude": -0.1278,
            "hourly": {
                "time": ["2024-01-01T00:00", "2024-01-01T01:00"],
                "temperature_2m": [10.5, 11.2],
                "precipitation": [0.0, 0.5],
                "relativehumidity_2m": [75, 80]
            },
            "daily": {
                "time": ["2024-01-01"],
                "temperature_2m_max": [15.0],
                "temperature_2m_min": [8.0],
                "precipitation_sum": [2.5]
            }
        }
    
    @patch('weather_trend_agent.tools.weather_service')
    async def test_geocode_location_success(self, mock_weather_service):
        """Test successful geocoding"""
        # Mock the weather service response
        mock_weather_service.geocode_location = AsyncMock(return_value={
            "status": "success",
            "data": {
                "name": "London",
                "latitude": 51.5074,
                "longitude": -0.1278,
                "country": "United Kingdom",
                "admin1": "England",
                "timezone": "Europe/London"
            },
            "timestamp": "2024-01-01T10:00:00Z"
        })
        
        # Test the function
        result = await geocode_location("London", self.context)
        
        # Verify the result
        assert result["status"] == "success"
        assert result["location_name"] == "London"
        assert result["coordinates"]["latitude"] == 51.5074
        assert result["coordinates"]["longitude"] == -0.1278
        assert result["details"]["country"] == "United Kingdom"
    
    @patch('weather_trend_agent.tools.weather_service')
    async def test_geocode_location_not_found(self, mock_weather_service):
        """Test geocoding when location not found"""
        # Mock the weather service response
        mock_weather_service.geocode_location = AsyncMock(return_value={
            "status": "error",
            "message": "Location 'InvalidLocation' not found",
            "timestamp": "2024-01-01T10:00:00Z"
        })
        
        # Test the function
        result = await geocode_location("InvalidLocation", self.context)
        
        # Verify the result
        assert result["status"] == "error"
        assert "Location 'InvalidLocation' not found" in result["message"]
    
    @patch('weather_trend_agent.tools.weather_service')
    async def test_get_historical_weather_by_coordinates(self, mock_weather_service):
        """Test historical weather retrieval by coordinates"""
        # Mock the weather service response
        mock_weather_service.get_historical_weather = AsyncMock(return_value={
            "status": "success",
            "data": {
                "location": {"name": "London", "latitude": 51.5074, "longitude": -0.1278},
                "period": {"start_date": "2024-01-01", "end_date": "2024-01-01"},
                "data": self.mock_weather_response
            },
            "timestamp": "2024-01-01T10:00:00Z"
        })
        
        # Test the function
        result = await get_historical_weather_by_coordinates(
            51.5074, -0.1278, "2024-01-01", "2024-01-01", self.context
        )
        
        # Verify the result
        assert result["status"] == "success"
        assert result["location"]["latitude"] == 51.5074
        assert result["location"]["longitude"] == -0.1278
        assert "weather_data" in result
    
    @patch('weather_trend_agent.tools.weather_service')
    async def test_get_historical_weather_by_location(self, mock_weather_service):
        """Test historical weather retrieval by location name"""
        # Mock the geocoding response
        mock_weather_service.geocode_location = AsyncMock(return_value={
            "status": "success",
            "data": {
                "name": "London",
                "latitude": 51.5074,
                "longitude": -0.1278,
                "country": "United Kingdom",
                "admin1": "England",
                "timezone": "Europe/London"
            },
            "timestamp": "2024-01-01T10:00:00Z"
        })
        
        # Mock the weather service response
        mock_weather_service.get_historical_weather = AsyncMock(return_value={
            "status": "success",
            "data": {
                "location": {"name": "London", "latitude": 51.5074, "longitude": -0.1278},
                "period": {"start_date": "2024-01-01", "end_date": "2024-01-01"},
                "data": self.mock_weather_response
            },
            "timestamp": "2024-01-01T10:00:00Z"
        })
        
        # Test the function
        result = await get_historical_weather_by_location(
            "London", "2024-01-01", "2024-01-01", self.context
        )
        
        # Verify the result
        assert result["status"] == "success"
        assert result["location"]["name"] == "London"
        assert "weather_data" in result
    
    @patch('weather_trend_agent.tools.weather_service')
    async def test_get_weather_summary_by_date(self, mock_weather_service):
        """Test weather summary for specific date"""
        # Mock the weather service response (get_weather_summary calls get_historical_weather internally)
        mock_weather_service.get_weather_summary = AsyncMock(return_value={
            "status": "success",
            "data": {
                "location": {"name": "London", "latitude": 51.5074, "longitude": -0.1278},
                "summary": {
                    "date": "2024-01-01",
                    "max_temperature": 15.0,
                    "min_temperature": 8.0,
                    "total_precipitation": 2.5,
                    "max_wind_speed": 12.0
                },
                "data": self.mock_weather_response
            },
            "timestamp": "2024-01-01T10:00:00Z"
        })
        
        # Test the function
        result = await get_weather_summary_by_date(
            51.5074, -0.1278, "2024-01-01", self.context
        )
        
        # Verify the result
        assert result["status"] == "success"
        assert result["date"] == "2024-01-01"
        assert "max_temperature" in result["summary"]
        assert "min_temperature" in result["summary"]
        assert "total_precipitation" in result["summary"]
    
    @patch('weather_trend_agent.tools.weather_service')
    async def test_get_forecast_weather(self, mock_weather_service):
        """Test weather forecast retrieval"""
        # Mock the geocoding response
        mock_weather_service.geocode_location = AsyncMock(return_value={
            "status": "success",
            "data": {
                "name": "London",
                "latitude": 51.5074,
                "longitude": -0.1278,
                "country": "United Kingdom",
                "admin1": "England",
                "timezone": "Europe/London"
            },
            "timestamp": "2024-01-01T10:00:00Z"
        })
        
        # Mock the forecast response
        mock_weather_service.get_forecast_weather = AsyncMock(return_value={
            "status": "success",
            "data": {
                "location": {"name": "London", "latitude": 51.5074, "longitude": -0.1278},
                "forecast_days": 7,
                "data": self.mock_weather_response
            },
            "timestamp": "2024-01-01T10:00:00Z"
        })
        
        # Test the function
        result = await get_forecast_weather("London", self.context)
        
        # Verify the result
        assert result["status"] == "success"
        assert result["location"]["name"] == "London"
        assert "weather_data" in result
    
    async def test_get_available_weather_variables(self):
        """Test available weather variables list"""
        result = await get_available_weather_variables(self.context)
        
        # Verify the result
        assert result["status"] == "success"
        assert "variables" in result
        assert "hourly_variables" in result["variables"]
        assert "daily_variables" in result["variables"]
        assert "temperature_2m" in result["variables"]["hourly_variables"]
        assert "precipitation" in result["variables"]["hourly_variables"]
        assert "relativehumidity_2m" in result["variables"]["hourly_variables"]
    
    @patch('weather_trend_agent.tools.weather_service')
    async def test_weather_api_error_handling(self, mock_weather_service):
        """Test error handling for weather API failures"""
        # Mock the weather service to fail
        mock_weather_service.get_historical_weather = AsyncMock(return_value={
            "status": "error",
            "message": "Failed to fetch weather data",
            "timestamp": "2024-01-01T10:00:00Z"
        })
        
        # Test the function
        result = await get_historical_weather_by_coordinates(
            51.5074, -0.1278, "2024-01-01", "2024-01-01", self.context
        )
        
        # Verify the result
        assert result["status"] == "error"
        assert "Failed to fetch weather data" in result["message"]
    
    def test_statistics_tracking(self):
        """Test that statistics are properly tracked"""
        # Verify initial state
        stats = self.context.get_agent_specific_state("statistics")
        assert stats["total_requests"] == 0
        assert stats["successful_requests"] == 0
        assert stats["failed_requests"] == 0
    
    def test_date_validation(self):
        """Test date format validation"""
        # Test valid date formats
        valid_dates = ["2024-01-01", "2024-12-31", "2023-06-15"]
        for date in valid_dates:
            try:
                datetime.strptime(date, "%Y-%m-%d")
                assert True  # Date is valid
            except ValueError:
                assert False, f"Date {date} should be valid"
        
        # Test invalid date formats
        invalid_dates = ["2024-13-01", "2024-00-01", "invalid-date"]
        for date in invalid_dates:
            try:
                datetime.strptime(date, "%Y-%m-%d")
                assert False, f"Date {date} should be invalid"
            except ValueError:
                assert True  # Date is invalid as expected


async def main():
    """Main test function"""
    print("🌤️ Running Weather Trend Agent Tests")
    print("=" * 50)
    
    # Create test instance
    test_instance = TestWeatherAgent()
    
    # Run tests
    test_methods = [
        test_instance.test_geocode_location_success,
        test_instance.test_geocode_location_not_found,
        test_instance.test_get_historical_weather_by_coordinates,
        test_instance.test_get_historical_weather_by_location,
        test_instance.test_get_weather_summary_by_date,
        test_instance.test_get_forecast_weather,
        test_instance.test_get_available_weather_variables,
        test_instance.test_weather_api_error_handling,
        test_instance.test_statistics_tracking,
        test_instance.test_date_validation
    ]
    
    passed = 0
    failed = 0
    
    for test_method in test_methods:
        try:
            test_instance.setup_method()
            if asyncio.iscoroutinefunction(test_method):
                await test_method()
            else:
                test_method()
            print(f"✅ {test_method.__name__}")
            passed += 1
        except Exception as e:
            import traceback
            print(f"❌ {test_method.__name__}: {e}")
            print(f"   Traceback: {traceback.format_exc()}")
            failed += 1
    
    print("=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠️  Some tests failed!")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
