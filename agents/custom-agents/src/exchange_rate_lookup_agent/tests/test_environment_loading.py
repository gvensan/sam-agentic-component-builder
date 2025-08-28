#!/usr/bin/env python3
"""
Environment Variable Loading Tests for Exchange Rate Lookup Agent

Tests that environment variables are properly loaded from .env files.
"""

import os
import sys
import pytest
from dotenv import load_dotenv

# Add the parent directory to the path to import the tools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Load environment variables from .env file
# Try multiple locations for .env file
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


class TestEnvironmentVariableLoading:
    """Test class for environment variable loading functionality"""
    
    def test_api_key_loaded_from_env(self):
        """Test that the API key is loaded from environment variables"""
        api_key = os.getenv('EXCHANGE_RATE_API_KEY')
        assert api_key is not None, "EXCHANGE_RATE_API_KEY should be loaded from environment"
        assert len(api_key) > 0, "EXCHANGE_RATE_API_KEY should not be empty"
        assert api_key.strip() != "", "EXCHANGE_RATE_API_KEY should not be just whitespace"
        print(f"✅ API key loaded successfully. Length: {len(api_key)}")
    
    def test_api_key_format(self):
        """Test that the API key has a reasonable format"""
        api_key = os.getenv('EXCHANGE_RATE_API_KEY')
        assert api_key is not None, "EXCHANGE_RATE_API_KEY should be loaded"
        
        # Check that it's not a placeholder value
        invalid_values = ['none', 'null', 'undefined', '', 'your_api_key_here', 'test_api_key_12345']
        assert api_key.lower() not in invalid_values, f"API key appears to be a placeholder: {api_key}"
        
        # Check minimum length (most API keys are at least 20 characters)
        assert len(api_key) >= 10, f"API key seems too short: {len(api_key)} characters"
        
        print(f"✅ API key format validation passed. Key: {api_key[:10]}...")
    
    def test_optional_environment_variables(self):
        """Test that optional environment variables have reasonable defaults"""
        # Test API base URL
        base_url = os.getenv('EXCHANGE_RATE_API_BASE_URL', 'https://v6.exchangerate-api.com/v6')
        assert base_url.startswith('http'), f"Base URL should be a valid URL: {base_url}"
        print(f"✅ API base URL: {base_url}")
        
        # Test timeout
        timeout = int(os.getenv('EXCHANGE_RATE_API_TIMEOUT', '30'))
        assert 5 <= timeout <= 300, f"Timeout should be between 5 and 300 seconds: {timeout}"
        print(f"✅ API timeout: {timeout}s")
        
        # Test cache duration
        cache_duration = int(os.getenv('EXCHANGE_RATE_CACHE_DURATION', '3600'))
        assert 60 <= cache_duration <= 86400, f"Cache duration should be between 60 and 86400 seconds: {cache_duration}"
        print(f"✅ Cache duration: {cache_duration}s")
        
        # Test monthly limit
        monthly_limit = int(os.getenv('EXCHANGE_RATE_MONTHLY_LIMIT', '1500'))
        assert 100 <= monthly_limit <= 100000, f"Monthly limit should be between 100 and 100000: {monthly_limit}"
        print(f"✅ Monthly limit: {monthly_limit}")
        
        # Test log level
        log_level = os.getenv('EXCHANGE_RATE_LOG_LEVEL', 'INFO')
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        assert log_level.upper() in valid_levels, f"Log level should be one of {valid_levels}: {log_level}"
        print(f"✅ Log level: {log_level}")
    
    def test_other_environment_variables(self):
        """Test that other relevant environment variables can be loaded"""
        # Test that we can access other environment variables
        sam_env_vars = [
            'SAM_NAMESPACE',
            'SAM_GATEWAY_ID',
            'SAM_BROKER_HOST',
            'SAM_BROKER_PORT'
        ]
        
        loaded_vars = []
        for var in sam_env_vars:
            value = os.getenv(var)
            if value:
                loaded_vars.append(var)
                print(f"✅ Found environment variable: {var}")
        
        print(f"📊 Loaded {len(loaded_vars)} SAM environment variables")
        # Don't fail if SAM vars aren't present, they might not be needed for all tests
    
    def test_env_file_locations(self):
        """Test that .env files can be found in expected locations"""
        found_env_files = []
        
        for env_path in env_locations:
            if os.path.exists(env_path):
                found_env_files.append(env_path)
                print(f"✅ Found .env file at: {env_path}")
        
        assert len(found_env_files) > 0, "No .env files found in any expected location"
        print(f"📁 Found {len(found_env_files)} .env file(s)")
    
    def test_environment_variable_persistence(self):
        """Test that environment variables persist across multiple accesses"""
        api_key_1 = os.getenv('EXCHANGE_RATE_API_KEY')
        api_key_2 = os.getenv('EXCHANGE_RATE_API_KEY')
        
        assert api_key_1 == api_key_2, "Environment variable should be consistent"
        assert api_key_1 is not None, "Environment variable should be loaded"
        
        print("✅ Environment variable persistence test passed")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
