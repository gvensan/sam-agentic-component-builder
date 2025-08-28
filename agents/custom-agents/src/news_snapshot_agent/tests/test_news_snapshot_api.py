"""
Direct API Testing for News Snapshot Agent

This module contains direct tests for the underlying Google News RSS API.
"""

import asyncio
import httpx
import xml.etree.ElementTree as ET
from datetime import datetime


async def test_google_news_rss_api():
    """Test Google News RSS API directly"""
    print("📰 Testing Google News RSS API")
    print("=" * 50)
    
    base_url = "https://news.google.com/rss/search"
    
    # Test 1: Search for a specific location
    print("\n1. Testing Location Search")
    print("-" * 30)
    test_locations = ["New York", "London", "Tokyo", "Sydney"]
    
    for location in test_locations:
        try:
            url = f"{base_url}?q={location}&hl=en-US&gl=US&ceid=US:en"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers={
                        'User-Agent': 'SAM-news_snapshot_agent/1.0.0',
                        'Accept': 'application/rss+xml, application/xml, text/xml'
                    },
                    timeout=15.0
                )
                response.raise_for_status()
                
            # Parse RSS XML
            root = ET.fromstring(response.text)
            channel = root.find('channel')
            
            if channel is not None:
                title = channel.find('title')
                items = channel.findall('item')
                
                print(f"✅ {location}: {len(items)} articles found")
                if items:
                    first_item = items[0]
                    item_title = first_item.find('title')
                    if item_title is not None and item_title.text:
                        print(f"   Sample: {item_title.text[:60]}...")
            else:
                print(f"❌ {location}: Invalid RSS structure")
                
        except Exception as e:
            print(f"❌ {location}: Error - {e}")
    
    # Test 2: Test different search parameters
    print("\n2. Testing Search Parameters")
    print("-" * 30)
    
    test_searches = [
        ("technology", "Technology news"),
        ("weather", "Weather news"),
        ("sports", "Sports news")
    ]
    
    for search_term, description in test_searches:
        try:
            url = f"{base_url}?q={search_term}&hl=en-US&gl=US&ceid=US:en"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers={
                        'User-Agent': 'SAM-news_snapshot_agent/1.0.0',
                        'Accept': 'application/rss+xml, application/xml, text/xml'
                    },
                    timeout=15.0
                )
                response.raise_for_status()
                
            root = ET.fromstring(response.text)
            channel = root.find('channel')
            items = channel.findall('item') if channel is not None else []
            
            print(f"✅ {description}: {len(items)} articles found")
            
        except Exception as e:
            print(f"❌ {description}: Error - {e}")
    
    # Test 3: Test RSS structure validation
    print("\n3. Testing RSS Structure")
    print("-" * 30)
    
    try:
        url = f"{base_url}?q=test&hl=en-US&gl=US&ceid=US:en"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={
                    'User-Agent': 'SAM-news_snapshot_agent/1.0.0',
                    'Accept': 'application/rss+xml, application/xml, text/xml'
                },
                timeout=15.0
            )
            response.raise_for_status()
            
        root = ET.fromstring(response.text)
        channel = root.find('channel')
        
        if channel is not None:
            # Check required RSS elements
            required_elements = ['title', 'description', 'link']
            missing_elements = []
            
            for element in required_elements:
                if channel.find(element) is None:
                    missing_elements.append(element)
            
            if missing_elements:
                print(f"❌ Missing required elements: {missing_elements}")
            else:
                print("✅ RSS structure is valid")
                
            # Check item structure
            items = channel.findall('item')
            if items:
                first_item = items[0]
                item_elements = ['title', 'link', 'description', 'pubDate']
                missing_item_elements = []
                
                for element in item_elements:
                    if first_item.find(element) is None:
                        missing_item_elements.append(element)
                
                if missing_item_elements:
                    print(f"⚠️ Missing item elements: {missing_item_elements}")
                else:
                    print("✅ Item structure is valid")
            else:
                print("⚠️ No items found in RSS feed")
        else:
            print("❌ Invalid RSS structure - no channel element")
            
    except Exception as e:
        print(f"❌ RSS structure test failed: {e}")
    
    # Test 4: Test response headers and content type
    print("\n4. Testing Response Headers")
    print("-" * 30)
    
    try:
        url = f"{base_url}?q=test&hl=en-US&gl=US&ceid=US:en"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={
                    'User-Agent': 'SAM-news_snapshot_agent/1.0.0',
                    'Accept': 'application/rss+xml, application/xml, text/xml'
                },
                timeout=15.0
            )
            response.raise_for_status()
            
        content_type = response.headers.get('content-type', '')
        print(f"✅ Content-Type: {content_type}")
        
        if 'xml' in content_type.lower() or 'rss' in content_type.lower():
            print("✅ Content type is appropriate for RSS")
        else:
            print("⚠️ Unexpected content type")
            
        content_length = response.headers.get('content-length')
        if content_length:
            print(f"✅ Content-Length: {content_length} bytes")
            
    except Exception as e:
        print(f"❌ Header test failed: {e}")


async def test_news_api_rate_limits():
    """Test API rate limiting behavior"""
    print("\n⏱️ Testing API Rate Limits")
    print("=" * 50)
    
    base_url = "https://news.google.com/rss/search"
    
    # Test multiple rapid requests
    print("Testing rapid requests...")
    start_time = datetime.now()
    
    try:
        async with httpx.AsyncClient() as client:
            responses = []
            for i in range(3):  # Reduced to 3 to be respectful
                response = await client.get(
                    f"{base_url}?q=test&hl=en-US&gl=US&ceid=US:en",
                    headers={
                        'User-Agent': 'SAM-news_snapshot_agent/1.0.0',
                        'Accept': 'application/rss+xml, application/xml, text/xml'
                    },
                    timeout=10.0
                )
                responses.append(response.status_code)
                await asyncio.sleep(1)  # Be respectful with delays
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"✅ Made 3 requests in {duration:.2f} seconds")
        print(f"   Response codes: {responses}")
        
        if all(code == 200 for code in responses):
            print("✅ All requests successful")
        else:
            print("⚠️ Some requests failed")
            
    except Exception as e:
        print(f"❌ Rate limit test failed: {e}")


async def test_news_api_error_handling():
    """Test API error handling"""
    print("\n🚨 Testing API Error Handling")
    print("=" * 50)
    
    base_url = "https://news.google.com/rss/search"
    
    # Test with invalid parameters
    print("Testing invalid search parameters...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{base_url}?q=&hl=en-US&gl=US&ceid=US:en",
                headers={
                    'User-Agent': 'SAM-news_snapshot_agent/1.0.0',
                    'Accept': 'application/rss+xml, application/xml, text/xml'
                },
                timeout=10.0
            )
            
        if response.status_code == 200:
            print("✅ Empty search query handled gracefully")
        else:
            print(f"⚠️ Unexpected status code: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
    
    # Test with very long search query
    print("Testing very long search query...")
    try:
        long_query = "a" * 1000  # Very long query
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{base_url}?q={long_query}&hl=en-US&gl=US&ceid=US:en",
                headers={
                    'User-Agent': 'SAM-news_snapshot_agent/1.0.0',
                    'Accept': 'application/rss+xml, application/xml, text/xml'
                },
                timeout=10.0
            )
            
        if response.status_code == 200:
            print("✅ Long search query handled gracefully")
        else:
            print(f"⚠️ Unexpected status code: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")


async def main():
    """Main test function"""
    print("📰 News Snapshot Agent - Direct API Testing")
    print("=" * 60)
    
    # Run all API tests
    await test_google_news_rss_api()
    await test_news_api_rate_limits()
    await test_news_api_error_handling()
    
    print("\n" + "=" * 60)
    print("🎉 Direct API testing completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
