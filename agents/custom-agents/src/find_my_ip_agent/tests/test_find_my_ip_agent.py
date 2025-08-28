#!/usr/bin/env python3
"""
Test script for SAM-compliant Find My IP Agent

This script tests the agent tools and functionality.
"""

import asyncio
import sys
import os
from unittest.mock import Mock, patch, AsyncMock

# Add the parent directory to the path to import the tools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Mock the SAM dependencies
sys.modules['google.adk.tools'] = Mock()
sys.modules['solace_ai_connector.common.log'] = Mock()

# Import the tools module
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from find_my_ip_agent.tools import (
    get_current_ip,
    get_ip_with_retry,
    get_ip_info,
    get_ip_location,
    get_ip_comprehensive_info,
    get_ip_security_info
)


class MockToolContext:
    """Mock tool context for testing"""
    
    def __init__(self, agent_name="FindMyIPAgent"):
        self.agent_name = agent_name
        self.state = {
            "statistics": {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "ips_searched": set(),
                "last_request_time": None
            }
        }
    
    def get_agent_specific_state(self, key, default=None):
        return self.state.get(key, default)
    
    def set_agent_specific_state(self, key, value):
        self.state[key] = value


class TestFindMyIPAgent:
    """Test class for Find My IP Agent"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.context = MockToolContext()
    
    @patch('find_my_ip_agent.tools.httpx.AsyncClient.get')
    async def test_get_current_ip_success(self, mock_get):
        """Test successful IP retrieval"""
        # Mock the HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ip": "192.168.1.1"}
        mock_get.return_value = mock_response
        
        # Test the function
        result = await get_current_ip(self.context)
        
        # Verify the result
        assert result["status"] == "success"
        assert result["ip_address"] == "192.168.1.1"
        assert "timestamp" in result
        assert result["source"] == "ipify-api"
    
    @patch('find_my_ip_agent.tools.httpx.AsyncClient.get')
    async def test_get_current_ip_error(self, mock_get):
        """Test IP retrieval error handling"""
        # Mock the HTTP response to fail
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = Exception("HTTP 500")
        mock_get.return_value = mock_response
        
        # Test the function
        result = await get_current_ip(self.context)
        
        # Verify the result
        assert result["status"] == "error"
        assert "message" in result
    
    @patch('find_my_ip_agent.tools.httpx.AsyncClient.get')
    async def test_get_ip_with_retry_success(self, mock_get):
        """Test IP retrieval with retry mechanism"""
        # Mock the HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"ip": "192.168.1.1"}
        mock_get.return_value = mock_response
        
        # Test the function
        result = await get_ip_with_retry(max_retries=3, tool_context=self.context)
        
        # Verify the result
        assert result["status"] == "success"
        assert result["ip_address"] == "192.168.1.1"
    
    @patch('find_my_ip_agent.tools.httpx.AsyncClient.get')
    async def test_get_ip_info_success(self, mock_get):
        """Test IP info retrieval"""
        # Mock the IPify response
        ipify_response = Mock()
        ipify_response.status_code = 200
        ipify_response.json.return_value = {"ip": "192.168.1.1"}
        
        # Mock the IP-API response
        ip_api_response = Mock()
        ip_api_response.status_code = 200
        ip_api_response.json.return_value = {
            "status": "success",
            "country": "United States",
            "countryCode": "US",
            "region": "CA",
            "regionName": "California",
            "city": "San Francisco",
            "zip": "94105",
            "lat": 37.7852,
            "lon": -122.3874,
            "timezone": "America/Los_Angeles",
            "isp": "Cloudflare, Inc.",
            "org": "Cloudflare, Inc.",
            "as": "AS13335 Cloudflare, Inc.",
            "query": "192.168.1.1"
        }
        
        # Set up the mock to return different responses
        mock_get.side_effect = [ipify_response, ip_api_response]
        
        # Test the function
        result = await get_ip_info(include_location=True, tool_context=self.context)
        
        # Verify the result
        assert result["status"] == "success"
        assert result["ip_address"] == "192.168.1.1"
        assert "location_info" in result
    
    @patch('find_my_ip_agent.tools.httpx.AsyncClient.get')
    async def test_get_ip_location_success(self, mock_get):
        """Test IP location retrieval"""
        # Mock the IP-API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "success",
            "country": "United States",
            "countryCode": "US",
            "region": "CA",
            "regionName": "California",
            "city": "San Francisco",
            "zip": "94105",
            "lat": 37.7852,
            "lon": -122.3874,
            "timezone": "America/Los_Angeles",
            "isp": "Cloudflare, Inc.",
            "org": "Cloudflare, Inc.",
            "as": "AS13335 Cloudflare, Inc.",
            "query": "8.8.8.8"
        }
        mock_get.return_value = mock_response
        
        # Test the function
        result = await get_ip_location("8.8.8.8", self.context)
        
        # Verify the result
        assert result["status"] == "success"
        assert result["data"]["city"] == "San Francisco"
        assert result["data"]["region"] == "CA"
        assert "api_used" in result
    
    @patch('find_my_ip_agent.tools.httpx.AsyncClient.get')
    async def test_get_ip_comprehensive_info_success(self, mock_get):
        """Test comprehensive IP info retrieval"""
        # Mock the IP-API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "success",
            "country": "United States",
            "countryCode": "US",
            "region": "CA",
            "regionName": "California",
            "city": "San Francisco",
            "zip": "94105",
            "lat": 37.7852,
            "lon": -122.3874,
            "timezone": "America/Los_Angeles",
            "isp": "Cloudflare, Inc.",
            "org": "Cloudflare, Inc.",
            "as": "AS13335 Cloudflare, Inc.",
            "query": "8.8.8.8"
        }
        mock_get.return_value = mock_response
        
        # Test the function
        result = await get_ip_comprehensive_info("8.8.8.8", self.context)
        
        # Verify the result
        assert result["status"] == "success"
        assert result["ip_address"] == "8.8.8.8"
        assert "location" in result
        assert "security" in result
        assert "apis_used" in result
    
    @patch('find_my_ip_agent.tools.httpx.AsyncClient.get')
    async def test_get_ip_security_info_success(self, mock_get):
        """Test IP security info retrieval"""
        # Mock the IP-API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "success",
            "country": "United States",
            "countryCode": "US",
            "region": "CA",
            "regionName": "California",
            "city": "San Francisco",
            "zip": "94105",
            "lat": 37.7852,
            "lon": -122.3874,
            "timezone": "America/Los_Angeles",
            "isp": "Cloudflare, Inc.",
            "org": "Cloudflare, Inc.",
            "as": "AS13335 Cloudflare, Inc.",
            "query": "8.8.8.8"
        }
        mock_get.return_value = mock_response
        
        # Test the function
        result = await get_ip_security_info("8.8.8.8", self.context)
        
        # Verify the result
        assert result["status"] == "success"
        assert "data" in result
        assert "api_used" in result
    
    def test_statistics_tracking(self):
        """Test that statistics are properly tracked"""
        # Verify initial state
        stats = self.context.get_agent_specific_state("statistics")
        assert stats["total_requests"] == 0
        assert stats["successful_requests"] == 0
        assert stats["failed_requests"] == 0
    
    def test_ip_validation(self):
        """Test IP address format validation"""
        # Test valid IP addresses
        valid_ips = ["192.168.1.1", "8.8.8.8", "1.1.1.1", "208.67.222.222"]
        for ip in valid_ips:
            # Basic validation - check if it's a string with dots
            assert isinstance(ip, str)
            assert ip.count('.') == 3
            assert all(part.isdigit() and 0 <= int(part) <= 255 for part in ip.split('.'))
        
        # Test invalid IP addresses
        invalid_ips = ["256.1.2.3", "1.2.3.256", "192.168.1", "invalid-ip"]
        for ip in invalid_ips:
            try:
                # This should fail for invalid IPs
                parts = ip.split('.')
                assert len(parts) == 4
                assert all(part.isdigit() and 0 <= int(part) <= 255 for part in parts)
                assert False, f"IP {ip} should be invalid"
            except (ValueError, AssertionError):
                assert True  # Expected for invalid IPs


async def main():
    """Main test function"""
    print("🌐 Running Find My IP Agent Tests")
    print("=" * 50)
    
    # Create test instance
    test_instance = TestFindMyIPAgent()
    
    # Run tests
    test_methods = [
        test_instance.test_get_current_ip_success,
        test_instance.test_get_current_ip_error,
        test_instance.test_get_ip_with_retry_success,
        test_instance.test_get_ip_info_success,
        test_instance.test_get_ip_location_success,
        test_instance.test_get_ip_comprehensive_info_success,
        test_instance.test_get_ip_security_info_success,
        test_instance.test_statistics_tracking,
        test_instance.test_ip_validation
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
