#!/usr/bin/env python3
"""
API Tests for Exchange Rate Lookup Agent

Tests the actual Exchange Rate API endpoints directly.
Requires a valid API key in the EXCHANGE_RATE_API_KEY environment variable.
"""

import os
import sys
import asyncio
import httpx
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

# Add the parent directory to the path to import the services
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.exchange_rate_service import ExchangeRateService


# Original async functions removed - using the pytest-marked versions below


async def main():
    """Run all API tests"""
    print("🧪 Exchange Rate Lookup Agent - API Tests")
    print("=" * 50)
    
    tests = [
        ("API Key Validation", test_api_key_validation_async),
        ("Latest Rates Endpoint", test_latest_rates_endpoint_async),
        ("Currency Conversion Endpoint", test_currency_conversion_endpoint_async),
        ("Quota Endpoint", test_quota_endpoint_async),
        ("Error Handling", test_error_handling_async),
        ("Rate Limiting", test_rate_limiting_async),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        print("-" * 30)
        
        try:
            result = await test_func()
            if result:
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {str(e)}")
    
    print(f"\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All API tests passed!")
        return True
    else:
        print("⚠️ Some tests failed. Check the output above.")
        return False


# Add pytest markers for async tests
import pytest

@pytest.mark.asyncio
async def test_api_key_validation_async():
    """Async version of API key validation test"""
    print("🔑 Testing API key validation...")
    
    api_key = os.getenv('EXCHANGE_RATE_API_KEY')
    if not api_key:
        print("❌ EXCHANGE_RATE_API_KEY environment variable not set")
        print("   Please set your API key: export EXCHANGE_RATE_API_KEY=your_key_here")
        print("   Or ensure your .env file contains: EXCHANGE_RATE_API_KEY=your_key_here")
        return False
    
    if len(api_key) < 10:
        print("❌ API key appears to be invalid (too short)")
        return False
    
    print(f"✅ API key validation passed (length: {len(api_key)})")
    return True

@pytest.mark.asyncio
async def test_latest_rates_endpoint_async():
    """Async version of latest rates endpoint test"""
    print("🌐 Testing latest rates endpoint...")
    
    api_key = os.getenv('EXCHANGE_RATE_API_KEY')
    if not api_key:
        print("❌ Skipping - no API key")
        return False
    
    try:
        async with ExchangeRateService(api_key) as service:
            # Test with USD
            result = await service.get_latest_rates("USD")
            
            if result["status"] == "success":
                data = result["data"]
                print(f"✅ Successfully fetched USD rates")
                print(f"   Base currency: {data.get('base_code')}")
                print(f"   Last update: {data.get('time_last_update_utc')}")
                print(f"   Number of rates: {len(data.get('conversion_rates', {}))}")
                
                # Check for major currencies
                rates = data.get('conversion_rates', {})
                major_currencies = ['EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'CNY']
                for currency in major_currencies:
                    if currency in rates:
                        print(f"   {currency}: {rates[currency]}")
                
                return True
            else:
                print(f"❌ Failed to get USD rates: {result.get('error')}")
                return False
                
    except Exception as e:
        print(f"❌ Error testing latest rates: {str(e)}")
        return False

@pytest.mark.asyncio
async def test_currency_conversion_endpoint_async():
    """Async version of currency conversion endpoint test"""
    print("💱 Testing currency conversion endpoint...")
    
    api_key = os.getenv('EXCHANGE_RATE_API_KEY')
    if not api_key:
        print("❌ Skipping - no API key")
        return False
    
    try:
        async with ExchangeRateService(api_key) as service:
            # Test USD to EUR conversion
            result = await service.convert_currency("USD", "EUR", 100.0)
            
            if result["status"] == "success":
                data = result["data"]
                print(f"✅ Successfully converted USD to EUR")
                print(f"   From: {data.get('base_code')} 100")
                print(f"   To: {data.get('target_code')} {data.get('conversion_result')}")
                print(f"   Rate: {data.get('conversion_rate')}")
                print(f"   Last update: {data.get('time_last_update_utc')}")
                
                return True
            else:
                print(f"❌ Failed to convert USD to EUR: {result.get('error')}")
                return False
                
    except Exception as e:
        print(f"❌ Error testing currency conversion: {str(e)}")
        return False

@pytest.mark.asyncio
async def test_quota_endpoint_async():
    """Async version of quota endpoint test"""
    print("📊 Testing quota endpoint...")
    
    api_key = os.getenv('EXCHANGE_RATE_API_KEY')
    if not api_key:
        print("❌ Skipping - no API key")
        return False
    
    try:
        async with ExchangeRateService(api_key) as service:
            result = await service.get_quota_info()
            
            if result["status"] == "success":
                data = result["data"]
                print(f"✅ Successfully fetched quota information")
                print(f"   Requests this month: {data.get('requests_this_month')}")
                print(f"   Monthly limit: {data.get('monthly_limit')}")
                print(f"   Remaining requests: {data.get('remaining_requests')}")
                print(f"   Usage percentage: {data.get('usage_percentage')}%")
                
                return True
            else:
                print(f"❌ Failed to get quota info: {result.get('error')}")
                return False
                
    except Exception as e:
        print(f"❌ Error testing quota endpoint: {str(e)}")
        return False

@pytest.mark.asyncio
async def test_error_handling_async():
    """Async version of error handling test"""
    print("🚨 Testing error handling...")
    
    api_key = os.getenv('EXCHANGE_RATE_API_KEY')
    if not api_key:
        print("❌ Skipping - no API key")
        return False
    
    try:
        async with ExchangeRateService(api_key) as service:
            # Test invalid currency code
            result = await service.get_latest_rates("XXX")
            
            if result["status"] == "error":
                print(f"✅ Correctly handled invalid currency code: {result.get('error_type')}")
            else:
                print(f"❌ Expected error for invalid currency code")
                return False
            
            # Test invalid API key (using a fake key)
            fake_service = ExchangeRateService("fake_key_12345")
            result = await fake_service.get_latest_rates("USD")
            
            if result["status"] == "error":
                print(f"✅ Correctly handled invalid API key: {result.get('error_type')}")
            else:
                print(f"❌ Expected error for invalid API key")
                return False
            
            await fake_service.close()
            return True
                
    except Exception as e:
        print(f"❌ Error testing error handling: {str(e)}")
        return False

@pytest.mark.asyncio
async def test_rate_limiting_async():
    """Async version of rate limiting test"""
    print("⏱️ Testing rate limiting...")
    
    api_key = os.getenv('EXCHANGE_RATE_API_KEY')
    if not api_key:
        print("❌ Skipping - no API key")
        return False
    
    try:
        async with ExchangeRateService(api_key) as service:
            # Make multiple requests to test rate limiting
            print("   Making multiple requests to test rate limiting...")
            
            for i in range(3):
                result = await service.get_latest_rates("USD")
                if result["status"] == "success":
                    print(f"   Request {i+1}: Success")
                elif result["status"] == "error" and "quota" in result.get("error", "").lower():
                    print(f"   Request {i+1}: Rate limited (expected)")
                    break
                else:
                    print(f"   Request {i+1}: {result.get('error')}")
            
                    print("✅ Rate limiting test completed")
        return True
                
    except Exception as e:
        print(f"❌ Error testing rate limiting: {str(e)}")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
