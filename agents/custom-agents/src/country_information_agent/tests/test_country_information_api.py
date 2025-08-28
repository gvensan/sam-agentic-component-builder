"""
Direct API Testing for Country Information Agent

This module contains direct tests for the underlying APIs used by the Country Information Agent.
"""

import asyncio
import httpx
from datetime import datetime


async def test_rest_countries_api():
    """Test REST Countries API endpoints directly"""
    print("🌍 Testing REST Countries API")
    print("=" * 50)
    
    base_url = "https://restcountries.com/v3.1"
    
    # Test 1: Get all countries
    print("\n1. Testing Get All Countries")
    print("-" * 30)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/all", timeout=15.0)
            response.raise_for_status()
            data = response.json()
            
        print(f"✅ Successfully retrieved {len(data)} countries")
        
        # Verify structure of first country
        if data:
            first_country = data[0]
            required_fields = ["name", "cca2", "cca3", "capital", "region", "population"]
            missing_fields = [field for field in required_fields if field not in first_country]
            
            if missing_fields:
                print(f"❌ Missing required fields: {missing_fields}")
            else:
                print(f"✅ Country data structure is valid")
                print(f"   Sample: {first_country['name']['common']} ({first_country['cca2']})")
                
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Get country by name
    print("\n2. Testing Get Country by Name")
    print("-" * 30)
    test_countries = ["United States", "Japan", "Germany", "Brazil"]
    
    for country_name in test_countries:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{base_url}/name/{country_name}", timeout=10.0)
                response.raise_for_status()
                data = response.json()
            
            if data and len(data) > 0:
                country = data[0]
                print(f"✅ {country_name}: {country['name']['common']} ({country['cca2']})")
                print(f"   Capital: {country.get('capital', ['N/A'])[0]}")
                print(f"   Population: {country.get('population', 'N/A'):,}")
            else:
                print(f"❌ {country_name}: Not found")
                
        except Exception as e:
            print(f"❌ {country_name}: Error - {e}")
    
    # Test 3: Get country by code
    print("\n3. Testing Get Country by Code")
    print("-" * 30)
    test_codes = ["US", "JP", "DE", "BR"]
    
    for code in test_codes:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{base_url}/alpha/{code}", timeout=10.0)
                response.raise_for_status()
                data = response.json()
            
            if data:
                country = data[0] if isinstance(data, list) else data
                print(f"✅ {code}: {country['name']['common']}")
            else:
                print(f"❌ {code}: Not found")
                
        except Exception as e:
            print(f"❌ {code}: Error - {e}")
    
    # Test 4: Search countries
    print("\n4. Testing Search Countries")
    print("-" * 30)
    search_terms = ["united", "island", "republic"]
    
    for term in search_terms:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{base_url}/name/{term}", timeout=10.0)
                response.raise_for_status()
                data = response.json()
            
            if data:
                print(f"✅ '{term}': Found {len(data)} countries")
                sample_countries = [country['name']['common'] for country in data[:3]]
                print(f"   Sample: {', '.join(sample_countries)}")
            else:
                print(f"❌ '{term}': No results")
                
        except Exception as e:
            print(f"❌ '{term}': Error - {e}")


async def test_ip_api():
    """Test IP-API.com for geolocation data"""
    print("\n🌐 Testing IP-API.com")
    print("=" * 50)
    
    # Test with a known IP address
    test_ips = ["8.8.8.8", "1.1.1.1", "208.67.222.222"]
    
    for ip in test_ips:
        print(f"\nTesting IP: {ip}")
        print("-" * 20)
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"http://ip-api.com/json/{ip}", timeout=10.0)
                response.raise_for_status()
                data = response.json()
            
            if data.get("status") == "success":
                print(f"✅ {ip}: {data.get('country', 'N/A')}, {data.get('city', 'N/A')}")
                print(f"   ISP: {data.get('isp', 'N/A')}")
                print(f"   Timezone: {data.get('timezone', 'N/A')}")
            else:
                print(f"❌ {ip}: API returned error")
                
        except Exception as e:
            print(f"❌ {ip}: Error - {e}")


async def test_api_rate_limits():
    """Test API rate limiting behavior"""
    print("\n⏱️ Testing API Rate Limits")
    print("=" * 50)
    
    base_url = "https://restcountries.com/v3.1"
    
    # Test multiple rapid requests
    print("Testing rapid requests...")
    start_time = datetime.now()
    
    try:
        async with httpx.AsyncClient() as client:
            responses = []
            for i in range(5):
                response = await client.get(f"{base_url}/name/United", timeout=5.0)
                responses.append(response.status_code)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"✅ Made 5 requests in {duration:.2f} seconds")
        print(f"   Response codes: {responses}")
        
        if all(code == 200 for code in responses):
            print("✅ All requests successful")
        else:
            print("⚠️ Some requests failed")
            
    except Exception as e:
        print(f"❌ Rate limit test failed: {e}")


async def test_api_error_handling():
    """Test API error handling"""
    print("\n🚨 Testing API Error Handling")
    print("=" * 50)
    
    base_url = "https://restcountries.com/v3.1"
    
    # Test invalid country name
    print("Testing invalid country name...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/name/InvalidCountryName123", timeout=10.0)
            
        if response.status_code == 404:
            print("✅ Correctly returned 404 for invalid country")
        else:
            print(f"⚠️ Unexpected status code: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
    
    # Test invalid country code
    print("Testing invalid country code...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{base_url}/alpha/XX", timeout=10.0)
            
        if response.status_code == 404:
            print("✅ Correctly returned 404 for invalid code")
        else:
            print(f"⚠️ Unexpected status code: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")


async def main():
    """Main test function"""
    print("🌍 Country Information Agent - Direct API Testing")
    print("=" * 60)
    
    # Run all API tests
    await test_rest_countries_api()
    await test_ip_api()
    await test_api_rate_limits()
    await test_api_error_handling()
    
    print("\n" + "=" * 60)
    print("🎉 Direct API testing completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
