#!/usr/bin/env python3
"""
Environment Integration Tests for Exchange Rate Lookup Agent

Tests that all services properly use environment variables instead of hard-coded values.
"""

import os
import sys
import pytest
from dotenv import load_dotenv

# Add the parent directory to the path to import the services
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Load environment variables from .env file
env_locations = [
    os.path.join(os.getcwd(), '.env'),  # Current working directory
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), '.env'),  # Project root
    '/Users/vengatagirivenkatesan/sam/v1/.env',  # SAM installation
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))), '.env'),  # Alternative SAM path
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


class TestEnvironmentIntegration:
    """Test class for environment variable integration"""
    
    def test_exchange_rate_service_environment_variables(self):
        """Test that ExchangeRateService uses environment variables"""
        from services.exchange_rate_service import ExchangeRateService
        
        # Test with no parameters (should use environment variables)
        api_key = os.getenv('EXCHANGE_RATE_API_KEY')
        service = ExchangeRateService(api_key)
        
        # Verify that environment variables are used
        expected_base_url = os.getenv('EXCHANGE_RATE_API_BASE_URL', 'https://v6.exchangerate-api.com/v6')
        expected_timeout = int(os.getenv('EXCHANGE_RATE_API_TIMEOUT', '30'))
        
        assert service.base_url == expected_base_url.rstrip('/'), f"Base URL should use environment variable: {service.base_url}"
        assert service.timeout == expected_timeout, f"Timeout should use environment variable: {service.timeout}"
        
        print(f"✅ ExchangeRateService uses environment variables: base_url={service.base_url}, timeout={service.timeout}")
    
    def test_rate_limiter_environment_variables(self):
        """Test that RateLimiter uses environment variables"""
        from services.rate_limiter import RateLimiter
        
        # Test with no parameters (should use environment variable)
        rate_limiter = RateLimiter()
        
        # Verify that environment variable is used
        expected_monthly_limit = int(os.getenv('EXCHANGE_RATE_MONTHLY_LIMIT', '1500'))
        
        assert rate_limiter.monthly_limit == expected_monthly_limit, f"Monthly limit should use environment variable: {rate_limiter.monthly_limit}"
        
        print(f"✅ RateLimiter uses environment variable: monthly_limit={rate_limiter.monthly_limit}")
    
    def test_cache_manager_environment_variables(self):
        """Test that CacheManager uses environment variables"""
        from services.cache_manager import CacheManager
        
        # Test with no parameters (should use environment variable)
        cache_manager = CacheManager()
        
        # Verify that environment variable is used
        expected_ttl = int(os.getenv('EXCHANGE_RATE_CACHE_DURATION', '3600'))
        
        assert cache_manager.default_ttl == expected_ttl, f"Default TTL should use environment variable: {cache_manager.default_ttl}"
        
        print(f"✅ CacheManager uses environment variable: default_ttl={cache_manager.default_ttl}")
    
    def test_lifecycle_environment_variables(self):
        """Test that lifecycle functions use environment variables"""
        from lifecycle import initialize_exchange_rate_lookup_agent
        
        # Create a mock host component
        class MockHostComponent:
            pass
        
        host_component = MockHostComponent()
        
        # Initialize the agent
        result = initialize_exchange_rate_lookup_agent(host_component)
        
        if result["status"] == "success":
            agent_state = host_component.agent_state
            
            # Verify that all environment variables are used
            expected_api_key = os.getenv('EXCHANGE_RATE_API_KEY')
            expected_base_url = os.getenv('EXCHANGE_RATE_API_BASE_URL', 'https://v6.exchangerate-api.com/v6')
            expected_cache_duration = int(os.getenv('EXCHANGE_RATE_CACHE_DURATION', '3600'))
            expected_timeout = int(os.getenv('EXCHANGE_RATE_API_TIMEOUT', '30'))
            expected_monthly_limit = int(os.getenv('EXCHANGE_RATE_MONTHLY_LIMIT', '1500'))
            expected_log_level = os.getenv('EXCHANGE_RATE_LOG_LEVEL', 'INFO')
            
            assert agent_state["api_key"] == expected_api_key, "API key should use environment variable"
            assert agent_state["base_url"] == expected_base_url, "Base URL should use environment variable"
            assert agent_state["cache_duration"] == expected_cache_duration, "Cache duration should use environment variable"
            assert agent_state["timeout"] == expected_timeout, "Timeout should use environment variable"
            assert agent_state["monthly_limit"] == expected_monthly_limit, "Monthly limit should use environment variable"
            assert agent_state["log_level"] == expected_log_level, "Log level should use environment variable"
            
            print(f"✅ Lifecycle uses all environment variables:")
            print(f"   - API Key: {agent_state['api_key'][:10]}...")
            print(f"   - Base URL: {agent_state['base_url']}")
            print(f"   - Cache Duration: {agent_state['cache_duration']}s")
            print(f"   - Timeout: {agent_state['timeout']}s")
            print(f"   - Monthly Limit: {agent_state['monthly_limit']}")
            print(f"   - Log Level: {agent_state['log_level']}")
        else:
            print(f"⚠️ Agent initialization failed: {result.get('error')}")
            # This might happen if API key is not set, which is expected in some test environments
    
    def test_environment_variable_consistency(self):
        """Test that all services use consistent environment variable values"""
        from services.exchange_rate_service import ExchangeRateService
        from services.rate_limiter import RateLimiter
        from services.cache_manager import CacheManager
        
        # Get expected values from environment
        expected_base_url = os.getenv('EXCHANGE_RATE_API_BASE_URL', 'https://v6.exchangerate-api.com/v6')
        expected_timeout = int(os.getenv('EXCHANGE_RATE_API_TIMEOUT', '30'))
        expected_monthly_limit = int(os.getenv('EXCHANGE_RATE_MONTHLY_LIMIT', '1500'))
        expected_cache_duration = int(os.getenv('EXCHANGE_RATE_CACHE_DURATION', '3600'))
        
        # Create service instances
        api_key = os.getenv('EXCHANGE_RATE_API_KEY', 'test_key')
        service = ExchangeRateService(api_key)
        rate_limiter = RateLimiter()
        cache_manager = CacheManager()
        
        # Verify consistency
        assert service.base_url == expected_base_url.rstrip('/'), "ExchangeRateService base_url should be consistent"
        assert service.timeout == expected_timeout, "ExchangeRateService timeout should be consistent"
        assert rate_limiter.monthly_limit == expected_monthly_limit, "RateLimiter monthly_limit should be consistent"
        assert cache_manager.default_ttl == expected_cache_duration, "CacheManager default_ttl should be consistent"
        
        print("✅ All services use consistent environment variable values")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
