"""
Test Suite for Country Information Agent

This module contains comprehensive tests for the Country Information Agent tools.
"""

import sys
import os
import asyncio
import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

# Add the parent directory to the path to import the tools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Mock the SAM dependencies
sys.modules['google.adk.tools'] = Mock()
sys.modules['solace_ai_connector.common.log'] = Mock()

# Import the tools module
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Mock the services module
sys.modules['services.country_service'] = Mock()

from country_information_agent.tools import (
    get_country_info, 
    search_countries, 
    get_country_borders, 
    get_country_comparison, 
    get_all_countries,
    _format_country_data,
    _format_currencies,
    _format_languages
)


class MockToolContext:
    """Mock tool context for testing"""
    
    def __init__(self, agent_name="CountryInformationAgent"):
        self.agent_name = agent_name
        self.state = {
            "statistics": {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "countries_searched": set(),
                "most_requested_countries": {},
                "cache_hits": 0,
                "cache_misses": 0
            }
        }
    
    def get_agent_specific_state(self, key, default=None):
        return self.state.get(key, default)
    
    def set_agent_specific_state(self, key, value):
        self.state[key] = value


class TestCountryAgent:
    """Test class for Country Information Agent"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.context = MockToolContext()
        self.mock_country_data = {
            "name": {"common": "France", "official": "French Republic"},
            "capital": ["Paris"],
            "population": 67391582,
            "area": 551695,
            "currencies": {"EUR": {"name": "Euro", "symbol": "€"}},
            "languages": {"fra": "French"},
            "borders": ["AND", "BEL", "DEU", "ITA", "LUX", "MCO", "ESP", "CHE"],
            "flags": {"png": "https://flagcdn.com/w320/fr.png", "svg": "https://flagcdn.com/fr.svg"},
            "latlng": [46.0, 2.0],
            "region": "Europe",
            "subregion": "Western Europe",
            "timezones": ["UTC-10:00", "UTC+01:00"],
            "idd": {"root": "+3", "suffixes": ["3"]},
            "gini": {"2020": 32.4}
        }
    
    def test_format_country_data(self):
        """Test country data formatting"""
        formatted = _format_country_data(self.mock_country_data)
        
        assert formatted["name"] == "France"
        assert formatted["official_name"] == "French Republic"
        assert formatted["capital"] == "Paris"
        assert formatted["population"] == 67391582
        assert formatted["area"] == 551695
        assert formatted["region"] == "Europe"
        assert formatted["subregion"] == "Western Europe"
        assert formatted["coordinates"]["lat"] == 46.0
        assert formatted["coordinates"]["lng"] == 2.0
        assert formatted["calling_codes"] == "+33"
        assert formatted["gdp"] == 32.4
    
    def test_format_currencies(self):
        """Test currency formatting"""
        currencies_data = {"EUR": {"name": "Euro", "symbol": "€"}}
        formatted = _format_currencies(currencies_data)
        
        assert len(formatted) == 1
        assert formatted[0]["code"] == "EUR"
        assert formatted[0]["name"] == "Euro"
        assert formatted[0]["symbol"] == "€"
    
    def test_format_languages(self):
        """Test language formatting"""
        languages_data = {"fra": "French", "eng": "English"}
        formatted = _format_languages(languages_data)
        
        assert len(formatted) == 2
        assert formatted[0]["code"] == "fra"
        assert formatted[0]["name"] == "French"
        assert formatted[1]["code"] == "eng"
        assert formatted[1]["name"] == "English"
    
    @patch('country_information_agent.tools.get_country_service')
    @pytest.mark.asyncio
    async def test_get_country_info_success(self, mock_get_service):
        """Test successful country info retrieval"""
        # Mock the service
        mock_service = AsyncMock()
        mock_service.get_country_by_name.return_value = {
            "status": "success",
            "data": [self.mock_country_data]
        }
        mock_get_service.return_value = mock_service
        
        # Test the function
        result = await get_country_info("France", self.context)
        
        # Verify the result
        assert result["status"] == "success"
        assert result["data"]["name"] == "France"
        assert result["data"]["capital"] == "Paris"
        assert result["data"]["population"] == 67391582
        assert result["source"] == "rest-countries-api"
        assert "timestamp" in result
    
    @patch('country_information_agent.tools.get_country_service')
    @pytest.mark.asyncio
    async def test_get_country_info_not_found(self, mock_get_service):
        """Test country info when country not found"""
        # Mock the service
        mock_service = AsyncMock()
        mock_service.get_country_by_name.return_value = {
            "status": "error",
            "error": "Country not found"
        }
        mock_service.get_country_by_code.return_value = {
            "status": "error",
            "error": "Country not found"
        }
        mock_service.get_all_countries.return_value = {
            "status": "success",
            "data": [self.mock_country_data]
        }
        mock_get_service.return_value = mock_service
        
        # Test the function
        result = await get_country_info("InvalidCountry", self.context)
        
        # Verify the result
        assert result["status"] == "error"
        assert "InvalidCountry" in result["error"]
        assert "suggestions" in result
    
    @patch('country_information_agent.tools.get_country_service')
    @pytest.mark.asyncio
    async def test_search_countries_success(self, mock_get_service):
        """Test successful country search"""
        # Mock the service
        mock_service = AsyncMock()
        mock_service.search_countries.return_value = {
            "status": "success",
            "data": [self.mock_country_data]
        }
        mock_get_service.return_value = mock_service
        
        # Test the function
        result = await search_countries("France", self.context)
        
        # Verify the result
        assert result["status"] == "success"
        assert len(result["data"]) == 1
        assert result["data"][0]["name"] == "France"
        assert result["count"] == 1
        assert result["source"] == "rest-countries-api"
    
    @patch('country_information_agent.tools.get_country_service')
    @pytest.mark.asyncio
    async def test_get_country_borders_success(self, mock_get_service):
        """Test successful border retrieval"""
        # Mock the service
        mock_service = AsyncMock()
        mock_service.get_country_by_name.return_value = {
            "status": "success",
            "data": [self.mock_country_data]
        }
        mock_service.get_country_by_code.return_value = {
            "status": "success",
            "data": {
                "name": {"common": "Germany"},
                "capital": ["Berlin"],
                "population": 83190556,
                "flags": {"png": "https://flagcdn.com/w320/de.png"}
            }
        }
        mock_get_service.return_value = mock_service
        
        # Test the function
        result = await get_country_borders("France", self.context)
        
        # Verify the result
        assert result["status"] == "success"
        assert result["data"]["country"] == "France"
        assert result["data"]["border_count"] == 8
        assert len(result["data"]["borders"]) == 8
    
    @pytest.mark.asyncio
    async def test_get_country_comparison_success(self):
        """Test successful country comparison"""
        # Mock get_country_info for each country
        with patch('country_information_agent.tools.get_country_info') as mock_get_info:
            mock_get_info.return_value = {
                "status": "success",
                "data": {
                    "name": "France",
                    "capital": "Paris",
                    "population": 67391582,
                    "area": 551695,
                    "region": "Europe",
                    "currencies": [{"code": "EUR", "name": "Euro"}],
                    "languages": [{"code": "fra", "name": "French"}],
                    "flag": {"png": "https://flagcdn.com/w320/fr.png"}
                }
            }
            
            # Test the function
            result = await get_country_comparison(["France", "Germany"], self.context)
            
            # Verify the result
            assert result["status"] == "success"
            assert result["data"]["count"] == 2
            assert len(result["data"]["countries"]) == 2
            assert "comparison_fields" in result["data"]
    
    @pytest.mark.asyncio
    async def test_get_country_comparison_too_few(self):
        """Test country comparison with too few countries"""
        result = await get_country_comparison(["France"], self.context)
        
        assert result["status"] == "error"
        assert "At least 2 countries" in result["error"]
    
    @pytest.mark.asyncio
    async def test_get_country_comparison_too_many(self):
        """Test country comparison with too many countries"""
        result = await get_country_comparison(["A", "B", "C", "D", "E", "F"], self.context)
        
        assert result["status"] == "error"
        assert "Maximum 5 countries" in result["error"]
    
    @patch('country_information_agent.tools.get_country_service')
    @pytest.mark.asyncio
    async def test_get_all_countries_success(self, mock_get_service):
        """Test successful retrieval of all countries"""
        # Mock the service
        mock_service = AsyncMock()
        mock_service.get_all_countries.return_value = {
            "status": "success",
            "data": [self.mock_country_data]
        }
        mock_get_service.return_value = mock_service
        
        # Test the function
        result = await get_all_countries(self.context)
        
        # Verify the result
        assert result["status"] == "success"
        assert len(result["data"]) == 1
        assert result["data"][0]["name"] == "France"
        assert result["count"] == 1
        assert result["source"] == "rest-countries-api"
    
    @patch('country_information_agent.tools.get_country_service')
    @pytest.mark.asyncio
    async def test_service_error_handling(self, mock_get_service):
        """Test error handling when service fails"""
        # Mock the service to raise an exception
        mock_service = AsyncMock()
        mock_service.get_country_by_name.side_effect = Exception("Network error")
        mock_get_service.return_value = mock_service
        
        # Test the function
        result = await get_country_info("France", self.context)
        
        # Verify the result
        assert result["status"] == "error"
        assert "Failed to get country information" in result["error"]
    
    def test_statistics_tracking(self):
        """Test that statistics are properly tracked"""
        # Verify initial state
        stats = self.context.get_agent_specific_state("statistics")
        assert stats["total_requests"] == 0
        assert stats["successful_requests"] == 0
        assert stats["failed_requests"] == 0


async def main():
    """Main test function"""
    print("🧪 Running Country Information Agent Tests")
    print("=" * 50)
    
    # Create test instance
    test_instance = TestCountryAgent()
    
    # Run tests
    test_methods = [
        test_instance.test_format_country_data,
        test_instance.test_format_currencies,
        test_instance.test_format_languages,
        test_instance.test_get_country_info_success,
        test_instance.test_get_country_info_not_found,
        test_instance.test_search_countries_success,
        test_instance.test_get_country_borders_success,
        test_instance.test_get_country_comparison_success,
        test_instance.test_get_country_comparison_too_few,
        test_instance.test_get_country_comparison_too_many,
        test_instance.test_get_all_countries_success,
        test_instance.test_service_error_handling,
        test_instance.test_statistics_tracking
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
