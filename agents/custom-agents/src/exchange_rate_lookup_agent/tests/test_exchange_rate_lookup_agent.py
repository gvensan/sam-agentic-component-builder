#!/usr/bin/env python3
"""
Tools Tests for Exchange Rate Lookup Agent

Tests agent functions with mocked dependencies.
Does not require a real API key.
"""

import sys
import os
import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
# Try multiple locations for .env file
env_locations = [
    os.path.join(os.getcwd(), '.env'),  # Current working directory
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), '.env'),  # Project root
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))), '.env'),  # SAM installation
    '.env'  # Current directory (fallback)
]

env_loaded = False
for env_path in env_locations:
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print(f"📁 Loaded environment variables from: {env_path}")
        env_loaded = True
        break

if not env_loaded:
    load_dotenv()  # Final fallback
    print("📁 Loaded environment variables from current directory (fallback)")

# Add the parent directory to the path to import the tools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Mock the SAM dependencies
sys.modules['google.adk.tools'] = Mock()
sys.modules['solace_ai_connector.common.log'] = Mock()

# Import the tools module
from tools import (
    get_exchange_rates,
    convert_currency,
    get_supported_currencies,
    get_currency_info,
    get_agent_stats
)


class TestExchangeRateLookupAgent:
    """Test class for Exchange Rate Lookup Agent functions"""
    
    def setup_method(self):
        """Set up test context"""
        self.context = Mock()
        
        # Get API key from environment variables
        api_key = os.getenv('EXCHANGE_RATE_API_KEY', 'test_api_key_12345')
        
        # Mock agent state using the correct SAM method
        agent_state = {
            'api_key': api_key,
            'base_url': 'https://v6.exchangerate-api.com/v6',
            'timeout': 30,
            'cache_duration': 3600,
            'request_count': 0,
            'initialized_at': '2024-01-15T10:00:00.000Z'
        }
        
        # Mock the get_agent_specific_state method
        self.context.get_agent_specific_state = Mock(return_value=agent_state)
        self.context.set_agent_specific_state = Mock()
        
        # Clear any existing cache and rate limiter
        if hasattr(self.context, '_cache_manager'):
            delattr(self.context, '_cache_manager')
        if hasattr(self.context, '_rate_limiter'):
            delattr(self.context, '_rate_limiter')
    
    def test_environment_variables_loaded(self):
        """Test that environment variables are properly loaded"""
        api_key = os.getenv('EXCHANGE_RATE_API_KEY')
        assert api_key is not None, "EXCHANGE_RATE_API_KEY should be loaded from environment"
        assert len(api_key) > 0, "EXCHANGE_RATE_API_KEY should not be empty"
        print(f"✅ Environment variables loaded successfully. API key length: {len(api_key)}")
    
    @pytest.mark.asyncio
    async def test_get_exchange_rates_success(self):
        """Test successful exchange rates retrieval"""
        # Mock successful API response
        mock_response = {
            "status": "success",
            "data": {
                "result": "success",
                "base_code": "USD",
                "conversion_rates": {
                    "USD": 1.0,
                    "EUR": 0.9013,
                    "GBP": 0.7679,
                    "JPY": 110.25
                },
                "time_last_update_utc": "Fri, 27 Mar 2020 00:00:00 +0000"
            }
        }
        
        # Clear any existing cache and rate limiter
        if hasattr(self.context, '_cache_manager'):
            delattr(self.context, '_cache_manager')
        if hasattr(self.context, '_rate_limiter'):
            delattr(self.context, '_rate_limiter')
        
        with patch('tools.ExchangeRateService') as mock_service_class, \
             patch('tools.RateLimiter') as mock_rate_limiter_class, \
             patch('tools.CacheManager') as mock_cache_class:
            
            # Mock rate limiter
            mock_rate_limiter = Mock()
            mock_rate_limiter.can_make_request.return_value = True
            mock_rate_limiter.record_request = Mock()
            mock_rate_limiter.get_quota_warning.return_value = None
            mock_rate_limiter_class.return_value = mock_rate_limiter
            
            # Mock cache
            mock_cache = Mock()
            mock_cache.get.return_value = None  # No cached data
            mock_cache.generate_cache_key.return_value = "USD_rates"
            mock_cache.set = Mock()
            mock_cache_class.return_value = mock_cache
            
            # Mock service
            mock_service = AsyncMock()
            mock_service.get_latest_rates.return_value = mock_response
            mock_service_class.return_value.__aenter__.return_value = mock_service
            
            result = await get_exchange_rates("USD", self.context, None)
            
            assert result["status"] == "success"
            assert result["data"]["base_code"] == "USD"
            assert "EUR" in result["data"]["conversion_rates"]
            assert result["data"]["conversion_rates"]["EUR"] == 0.9013
    
    @pytest.mark.asyncio
    async def test_get_exchange_rates_invalid_currency(self):
        """Test exchange rates with invalid currency code"""
        result = await get_exchange_rates("XXX", self.context, None)
        
        assert result["status"] == "error"
        assert "Unsupported currency code" in result["error"]
    
    @pytest.mark.asyncio
    async def test_get_exchange_rates_no_context(self):
        """Test exchange rates without proper context"""
        # Mock the API service to avoid actual API calls
        with patch('tools.ExchangeRateService') as mock_service_class, \
             patch('tools.RateLimiter') as mock_rate_limiter_class, \
             patch('tools.CacheManager') as mock_cache_class:
            
            # Mock rate limiter
            mock_rate_limiter = Mock()
            mock_rate_limiter.can_make_request.return_value = True
            mock_rate_limiter.record_request = Mock()
            mock_rate_limiter.get_quota_warning.return_value = None
            mock_rate_limiter_class.return_value = mock_rate_limiter
            
            # Mock cache
            mock_cache = Mock()
            mock_cache.get.return_value = None  # No cached data
            mock_cache.generate_cache_key.return_value = "USD_rates"
            mock_cache.set = Mock()
            mock_cache_class.return_value = mock_cache
            
            # Mock service
            mock_service = AsyncMock()
            mock_service.get_latest_rates.return_value = {
                "status": "success",
                "data": {"result": "success"}
            }
            mock_service_class.return_value.__aenter__.return_value = mock_service
            
            result = await get_exchange_rates("USD", None, None)
            
            # Now the function should work with environment variables as fallback
            assert result["status"] == "success"
    
    @pytest.mark.asyncio
    async def test_convert_currency_success(self):
        """Test successful currency conversion"""
        # Mock successful API response
        mock_response = {
            "status": "success",
            "data": {
                "result": "success",
                "base_code": "USD",
                "target_code": "EUR",
                "conversion_rate": 0.9013,
                "conversion_result": 90.13
            }
        }
        
        # Clear any existing cache and rate limiter
        if hasattr(self.context, '_cache_manager'):
            delattr(self.context, '_cache_manager')
        if hasattr(self.context, '_rate_limiter'):
            delattr(self.context, '_rate_limiter')
        
        with patch('tools.ExchangeRateService') as mock_service_class, \
             patch('tools.RateLimiter') as mock_rate_limiter_class, \
             patch('tools.CacheManager') as mock_cache_class:
            
            # Mock rate limiter
            mock_rate_limiter = Mock()
            mock_rate_limiter.can_make_request.return_value = True
            mock_rate_limiter.record_request = Mock()
            mock_rate_limiter.get_quota_warning.return_value = None
            mock_rate_limiter_class.return_value = mock_rate_limiter
            
            # Mock cache
            mock_cache = Mock()
            mock_cache.get.return_value = None  # No cached data
            mock_cache.generate_cache_key.return_value = "USD_EUR_100"
            mock_cache.set = Mock()
            mock_cache_class.return_value = mock_cache
            
            # Mock service
            mock_service = AsyncMock()
            mock_service.convert_currency.return_value = mock_response
            mock_service_class.return_value.__aenter__.return_value = mock_service
            
            result = await convert_currency("USD", "EUR", 100.0, self.context, None)
            
            assert result["status"] == "success"
            assert result["data"]["base_code"] == "USD"
            assert result["data"]["target_code"] == "EUR"
            assert result["data"]["conversion_result"] == 90.13
    
    @pytest.mark.asyncio
    async def test_convert_currency_invalid_from_currency(self):
        """Test conversion with invalid from currency"""
        result = await convert_currency("XXX", "EUR", 100.0, self.context, None)
        
        assert result["status"] == "error"
        assert "Invalid from_currency" in result["error"]
    
    @pytest.mark.asyncio
    async def test_convert_currency_invalid_to_currency(self):
        """Test conversion with invalid to currency"""
        result = await convert_currency("USD", "XXX", 100.0, self.context, None)
        
        assert result["status"] == "error"
        assert "Invalid to_currency" in result["error"]
    
    @pytest.mark.asyncio
    async def test_convert_currency_invalid_amount(self):
        """Test conversion with invalid amount"""
        result = await convert_currency("USD", "EUR", -100.0, self.context, None)
        
        assert result["status"] == "error"
        assert "Invalid amount" in result["error"]
    
    @pytest.mark.asyncio
    async def test_convert_currency_zero_amount(self):
        """Test conversion with zero amount"""
        result = await convert_currency("USD", "EUR", 0.0, self.context, None)
        
        assert result["status"] == "error"
        assert "Invalid amount" in result["error"]
    
    @pytest.mark.asyncio
    async def test_get_supported_currencies(self):
        """Test getting supported currencies"""
        result = await get_supported_currencies(self.context, None)
        
        assert result["status"] == "success"
        assert "currencies" in result["data"]
        assert "total_count" in result["data"]
        assert len(result["data"]["currencies"]) > 0
        
        # Check for major currencies
        currency_codes = [c["code"] for c in result["data"]["currencies"]]
        assert "USD" in currency_codes
        assert "EUR" in currency_codes
        assert "GBP" in currency_codes
    
    @pytest.mark.asyncio
    async def test_get_currency_info_success(self):
        """Test getting currency information"""
        # Mock exchange rates for USD rate lookup
        mock_rates_response = {
            "status": "success",
            "data": {
                "conversion_rates": {
                    "EUR": 0.9013
                }
            }
        }
        
        with patch('tools.get_exchange_rates', return_value=mock_rates_response):
            result = await get_currency_info("EUR", self.context, None)
            
            assert result["status"] == "success"
            assert result["data"]["code"] == "EUR"
            assert result["data"]["name"] == "Euro"
            assert result["data"]["supported"] == True
            assert result["data"]["usd_rate"] == 0.9013
    
    @pytest.mark.asyncio
    async def test_get_currency_info_invalid_currency(self):
        """Test getting info for invalid currency"""
        result = await get_currency_info("XXX", self.context, None)
        
        assert result["status"] == "error"
        assert "Unsupported currency code" in result["error"]
    
    @pytest.mark.asyncio
    async def test_get_currency_info_usd(self):
        """Test getting USD currency information"""
        result = await get_currency_info("USD", self.context, None)
        
        assert result["status"] == "success"
        assert result["data"]["code"] == "USD"
        assert result["data"]["name"] == "US Dollar"
        assert result["data"]["usd_rate"] == 1.0
        assert result["data"]["symbol"] == "$"
    
    @pytest.mark.asyncio
    async def test_get_agent_stats(self):
        """Test getting agent statistics"""
        result = await get_agent_stats(self.context, None)
        
        assert result["status"] == "success"
        assert "agent_info" in result["data"]
        assert "api_info" in result["data"]
        
        agent_info = result["data"]["agent_info"]
        assert agent_info["name"] == "Exchange Rate Lookup Agent"
        assert agent_info["version"] == "1.0.0"
        assert agent_info["total_requests"] == 0
    
    @pytest.mark.asyncio
    async def test_get_agent_stats_no_context(self):
        """Test getting agent stats without context"""
        result = await get_agent_stats(None, None)
        
        assert result["status"] == "success"
        assert "agent_info" in result["data"]
    
    @pytest.mark.asyncio
    async def test_rate_limiting_integration(self):
        """Test rate limiting integration"""
        # Clear any existing cache and rate limiter
        if hasattr(self.context, '_cache_manager'):
            delattr(self.context, '_cache_manager')
        if hasattr(self.context, '_rate_limiter'):
            delattr(self.context, '_rate_limiter')
        
        # Mock rate limiter that prevents requests
        with patch('tools.RateLimiter') as mock_rate_limiter_class:
            mock_rate_limiter = Mock()
            mock_rate_limiter.can_make_request.return_value = False
            mock_rate_limiter_class.return_value = mock_rate_limiter
            
            result = await get_exchange_rates("USD", self.context, None)
            
            assert result["status"] == "error"
            assert "quota exceeded" in result["error"].lower()
    
    @pytest.mark.asyncio
    async def test_caching_integration(self):
        """Test caching integration"""
        # Mock cache that returns cached data
        with patch('tools.CacheManager') as mock_cache_class:
            mock_cache = Mock()
            mock_cache.get.return_value = {"cached": "data"}
            mock_cache.generate_cache_key.return_value = "USD_rates"
            mock_cache_class.return_value = mock_cache
            
            result = await get_exchange_rates("USD", self.context, None)
            
            # Should return cached data
            assert result["status"] == "success"
            assert result["cached"] == True
    
    @pytest.mark.asyncio
    async def test_error_handling_api_failure(self):
        """Test error handling when API fails"""
        # Mock API failure
        mock_response = {
            "status": "error",
            "error": "API request failed: 401",
            "error_type": "invalid_key"
        }
        
        # Clear any existing cache and rate limiter
        if hasattr(self.context, '_cache_manager'):
            delattr(self.context, '_cache_manager')
        if hasattr(self.context, '_rate_limiter'):
            delattr(self.context, '_rate_limiter')
        
        with patch('tools.ExchangeRateService') as mock_service_class, \
             patch('tools.RateLimiter') as mock_rate_limiter_class, \
             patch('tools.CacheManager') as mock_cache_class:
            
            # Mock rate limiter
            mock_rate_limiter = Mock()
            mock_rate_limiter.can_make_request.return_value = True
            mock_rate_limiter.record_request = Mock()
            mock_rate_limiter.get_quota_warning.return_value = None
            mock_rate_limiter_class.return_value = mock_rate_limiter
            
            # Mock cache
            mock_cache = Mock()
            mock_cache.get.return_value = None  # No cached data
            mock_cache.generate_cache_key.return_value = "USD_rates"
            mock_cache.set = Mock()
            mock_cache_class.return_value = mock_cache
            
            # Mock service
            mock_service = AsyncMock()
            mock_service.get_latest_rates.return_value = mock_response
            mock_service_class.return_value.__aenter__.return_value = mock_service
            
            result = await get_exchange_rates("USD", self.context, None)
            
            assert result["status"] == "error"
            assert "API request failed" in result["error"]
    
    @pytest.mark.asyncio
    async def test_currency_validation_edge_cases(self):
        """Test currency validation edge cases"""
        # Clear any existing cache and rate limiter
        if hasattr(self.context, '_cache_manager'):
            delattr(self.context, '_cache_manager')
        if hasattr(self.context, '_rate_limiter'):
            delattr(self.context, '_rate_limiter')
        
        # Test empty currency code
        result = await get_exchange_rates("", self.context, None)
        assert result["status"] == "error"
        assert "empty" in result["error"].lower() or "invalid" in result["error"].lower()
        
        # Test None currency code
        result = await get_exchange_rates(None, self.context, None)
        assert result["status"] == "error"
        assert "empty" in result["error"].lower() or "invalid" in result["error"].lower()
        
        # Test currency code with spaces (should be stripped and validated)
        # " USD " should be stripped to "USD" which is valid, so this should succeed
        # Let's test with an invalid currency instead
        result = await get_exchange_rates("XXX", self.context, None)
        assert result["status"] == "error"
        assert "unsupported" in result["error"].lower() or "invalid" in result["error"].lower()
    
    @pytest.mark.asyncio
    async def test_amount_validation_edge_cases(self):
        """Test amount validation edge cases"""
        # Test negative amount
        result = await convert_currency("USD", "EUR", -100.0, self.context, None)
        assert result["status"] == "error"
        
        # Test zero amount
        result = await convert_currency("USD", "EUR", 0.0, self.context, None)
        assert result["status"] == "error"
        
        # Test very large amount
        result = await convert_currency("USD", "EUR", 1e15, self.context, None)
        assert result["status"] == "error"
        
        # Test very small amount
        result = await convert_currency("USD", "EUR", 1e-10, self.context, None)
        assert result["status"] == "error"
    
    @pytest.mark.asyncio
    async def test_context_state_management(self):
        """Test context state management"""
        # Test that request count is incremented
        mock_response = {"status": "success", "data": {"result": "success"}}
        
        # Clear any existing cache and rate limiter
        if hasattr(self.context, '_cache_manager'):
            delattr(self.context, '_cache_manager')
        if hasattr(self.context, '_rate_limiter'):
            delattr(self.context, '_rate_limiter')
        
        with patch('tools.ExchangeRateService') as mock_service_class, \
             patch('tools.RateLimiter') as mock_rate_limiter_class, \
             patch('tools.CacheManager') as mock_cache_class:
            
            # Mock rate limiter
            mock_rate_limiter = Mock()
            mock_rate_limiter.can_make_request.return_value = True
            mock_rate_limiter.record_request = Mock()
            mock_rate_limiter.get_quota_warning.return_value = None
            mock_rate_limiter_class.return_value = mock_rate_limiter
            
            # Mock cache
            mock_cache = Mock()
            mock_cache.get.return_value = None  # No cached data
            mock_cache.generate_cache_key.return_value = "USD_rates"
            mock_cache.set = Mock()
            mock_cache_class.return_value = mock_cache
            
            # Mock service
            mock_service = AsyncMock()
            mock_service.get_latest_rates.return_value = mock_response
            mock_service_class.return_value.__aenter__.return_value = mock_service
            
            initial_count = self.context.get_agent_specific_state("agent_state", {})['request_count']
            await get_exchange_rates("USD", self.context, None)
            final_count = self.context.get_agent_specific_state("agent_state", {})['request_count']
            
            assert final_count == initial_count + 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
