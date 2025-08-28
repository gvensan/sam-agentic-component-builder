"""
Comprehensive Test Suite for News Snapshot Agent

This module contains comprehensive tests for the News Snapshot Agent tools.
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

from tools import (
    get_news_for_location,
    get_news_with_date_filter,
    get_news_snapshot,
    search_news_by_keywords,
    get_weather_news,
    get_trending_topics,
    parse_date_filter,
    generate_news_summary,
    parse_news_item,
    get_text
)


class MockToolContext:
    """Mock tool context for testing"""
    
    def __init__(self, agent_name="NewsSnapshotAgent"):
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


class TestNewsAgent:
    """Test class for News Snapshot Agent"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.context = MockToolContext()
        self.mock_rss_data = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Google News</title>
    <item>
      <title>Test News Article</title>
      <link>https://example.com/article1</link>
      <description>This is a test news article about technology.</description>
      <pubDate>Mon, 01 Jan 2024 10:00:00 GMT</pubDate>
      <source>Test News</source>
    </item>
    <item>
      <title>Weather Update</title>
      <link>https://example.com/article2</link>
      <description>Weather forecast shows sunny skies ahead.</description>
      <pubDate>Mon, 01 Jan 2024 11:00:00 GMT</pubDate>
      <source>Weather News</source>
    </item>
  </channel>
</rss>'''
    
    def test_parse_date_filter(self):
        """Test date filter parsing"""
        # Test relative dates
        assert parse_date_filter("7d") < datetime.now(timezone.utc)
        assert parse_date_filter("24h") < datetime.now(timezone.utc)
        assert parse_date_filter("1w") < datetime.now(timezone.utc)
        
        # Test "now"
        now = datetime.now(timezone.utc)
        parsed_now = parse_date_filter("now")
        assert abs((now - parsed_now).total_seconds()) < 10
        
        # Test ISO format
        iso_date = "2024-01-01T00:00:00Z"
        parsed_iso = parse_date_filter(iso_date)
        assert parsed_iso.year == 2024
        assert parsed_iso.month == 1
        assert parsed_iso.day == 1
    
    def test_generate_news_summary(self):
        """Test news summary generation"""
        articles = [
            {
                "title": "Tech Company Opens New Office",
                "source": "Tech News",
                "published_date": "2024-01-01T10:00:00Z"
            },
            {
                "title": "Weather Forecast for Weekend",
                "source": "Weather News", 
                "published_date": "2024-01-01T11:00:00Z"
            }
        ]
        
        summary = generate_news_summary(articles, "New York")
        assert summary["location"] == "New York"
        assert summary["total_articles"] == 2
        assert "Tech Company" in summary["top_stories"][0]["title"]
        assert "Weather Forecast" in summary["top_stories"][1]["title"]
    
    def test_parse_news_item(self):
        """Test news item parsing"""
        from xml.etree.ElementTree import fromstring
        
        xml_item = '''<item>
            <title>Test Article</title>
            <link>https://example.com</link>
            <description>Test description</description>
            <pubDate>Mon, 01 Jan 2024 10:00:00 GMT</pubDate>
            <source>Test Source</source>
        </item>'''
        
        item_element = fromstring(xml_item)
        parsed_item = parse_news_item(item_element)
        
        assert parsed_item["title"] == "Test Article"
        assert parsed_item["link"] == "https://example.com"
        assert parsed_item["description"] == "Test description"
        assert parsed_item["source"] == "Test Source"
    
    def test_get_text(self):
        """Test text extraction from XML elements"""
        from xml.etree.ElementTree import fromstring
        
        xml_element = fromstring('<title>Test Title</title>')
        text = get_text(xml_element)
        assert text == "Test Title"
    
    @patch('tools.httpx.AsyncClient.get')
    async def test_get_news_for_location_success(self, mock_get):
        """Test successful news retrieval for location"""
        # Mock the HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = self.mock_rss_data
        mock_get.return_value = mock_response
        
        # Test the function
        result = await get_news_for_location("New York", 20, self.context)
        
        # Verify the result
        assert result["status"] == "success"
        assert result["location"] == "New York"
        assert len(result["articles"]) == 2
        assert result["articles"][0]["title"] == "Test News Article"
    
    @patch('tools.httpx.AsyncClient.get')
    async def test_get_news_for_location_error(self, mock_get):
        """Test error handling for news retrieval"""
        # Mock the HTTP response to fail
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        # Test the function
        result = await get_news_for_location("InvalidLocation", 20, self.context)
        
        # Verify the result
        assert result["status"] == "error"
        assert "Unexpected error" in result["message"]
    
    @patch('tools.httpx.AsyncClient.get')
    async def test_get_news_with_date_filter(self, mock_get):
        """Test news retrieval with date filtering"""
        # Mock the HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = self.mock_rss_data
        mock_get.return_value = mock_response
        
        # Test the function
        result = await get_news_with_date_filter("New York", "7d", "now", 20, self.context)
        
        # Verify the result
        assert result["status"] == "success"
        assert result["location"] == "New York"
        assert "7d" in result["date_filter"]["start_date"]
    
    @patch('tools.httpx.AsyncClient.get')
    async def test_search_news_by_keywords(self, mock_get):
        """Test news search by keywords"""
        # Mock the HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = self.mock_rss_data
        mock_get.return_value = mock_response
        
        # Test the function
        result = await search_news_by_keywords("New York", "technology", 20, self.context)
        
        # Verify the result
        assert result["status"] == "success"
        assert "technology" in result["keywords"]
        assert result["location"] == "New York"
    
    @patch('tools.httpx.AsyncClient.get')
    async def test_get_weather_news(self, mock_get):
        """Test weather news retrieval"""
        # Mock the HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = self.mock_rss_data
        mock_get.return_value = mock_response
        
        # Test the function
        result = await get_weather_news("New York", None, 15, self.context)
        
        # Verify the result
        assert result["status"] == "success"
        assert result["location"] == "New York"
        assert "weather_categories" in result
    
    @patch('tools.httpx.AsyncClient.get')
    async def test_get_trending_topics(self, mock_get):
        """Test trending topics extraction"""
        # Mock the HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = self.mock_rss_data
        mock_get.return_value = mock_response
        
        # Test the function
        result = await get_trending_topics("New York", 10, self.context)
        
        # Verify the result
        assert result["status"] == "success"
        assert result["location"] == "New York"
        assert "trending_topics" in result
    
    @patch('tools.httpx.AsyncClient.get')
    async def test_get_news_snapshot(self, mock_get):
        """Test comprehensive news snapshot"""
        # Mock the HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = self.mock_rss_data
        mock_get.return_value = mock_response
        
        # Test the function
        result = await get_news_snapshot("New York", 7, 15, True, self.context)
        
        # Verify the result
        assert result["status"] == "success"
        assert result["location"] == "New York"
        assert "summary" in result
        assert "articles" in result
        assert "snapshot_info" in result
    
    def test_statistics_tracking(self):
        """Test that statistics are properly tracked"""
        # Verify initial state
        stats = self.context.get_agent_specific_state("statistics")
        assert stats["total_requests"] == 0
        assert stats["successful_requests"] == 0
        assert stats["failed_requests"] == 0


async def main():
    """Main test function"""
    print("📰 Running News Snapshot Agent Tests")
    print("=" * 50)
    
    # Create test instance
    test_instance = TestNewsAgent()
    
    # Run tests
    test_methods = [
        test_instance.test_parse_date_filter,
        test_instance.test_generate_news_summary,
        test_instance.test_parse_news_item,
        test_instance.test_get_text,
        test_instance.test_get_news_for_location_success,
        test_instance.test_get_news_for_location_error,
        test_instance.test_get_news_with_date_filter,
        test_instance.test_search_news_by_keywords,
        test_instance.test_get_weather_news,
        test_instance.test_get_trending_topics,
        test_instance.test_get_news_snapshot,
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
