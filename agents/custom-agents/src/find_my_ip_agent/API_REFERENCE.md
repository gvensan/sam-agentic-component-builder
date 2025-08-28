# API Reference - IP Address Agent

This document outlines the APIs used by the IP Address Agent and their capabilities.

## 🌐 Implemented APIs

### 1. IPify API (Primary IP Source)
- **URL**: `https://api.ipify.org?format=json`
- **Purpose**: Get current public IP address
- **Rate Limit**: Free tier available
- **Documentation**: https://www.ipify.org/

**Example Response:**
```json
{
  "ip": "203.0.113.1"
}
```

### 2. ipapi.co (Primary Location API)
- **URL**: `https://ipapi.co/{ip}/json/`
- **Purpose**: Get location information for any IP
- **Rate Limit**: 1,000 requests/day (free tier)
- **Documentation**: https://ipapi.co/

**Example Response:**
```json
{
  "ip": "203.0.113.1",
  "city": "New York",
  "region": "New York",
  "country": "United States",
  "country_name": "United States",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "timezone": "America/New_York",
  "org": "ISP Name",
  "postal": "10001"
}
```

### 3. ip-api.com (Secondary Location & Security API)
- **URL**: `http://ip-api.com/json/{ip}`
- **Purpose**: Location and security data source
- **Rate Limit**: 45 requests/minute (free tier)
- **Documentation**: http://ip-api.com/

**Example Response:**
```json
{
  "status": "success",
  "country": "United States",
  "countryCode": "US",
  "region": "NY",
  "regionName": "New York",
  "city": "New York",
  "zip": "10001",
  "lat": 40.7128,
  "lon": -74.0060,
  "timezone": "America/New_York",
  "isp": "ISP Name",
  "org": "Organization",
  "as": "AS12345 ISP Name"
}
```

### 4. ipinfo.io (Tertiary Location API)
- **URL**: `https://ipinfo.io/{ip}/json`
- **Purpose**: Additional location data source
- **Rate Limit**: 50,000 requests/month (free tier)
- **Documentation**: https://ipinfo.io/

**Example Response:**
```json
{
  "ip": "203.0.113.1",
  "city": "New York",
  "region": "New York",
  "country": "US",
  "loc": "40.7128,-74.0060",
  "org": "ISP Name",
  "postal": "10001",
  "timezone": "America/New_York"
}
```

### 5. ipwhois.io (Primary Security API)
- **URL**: `https://ipwhois.app/json/{ip}`
- **Purpose**: Location and security data with threat detection
- **Rate Limit**: 10,000 requests/month (free tier)
- **Documentation**: https://ipwhois.io/

**Example Response:**
```json
{
  "ip": "203.0.113.1",
  "success": true,
  "type": "IPv4",
  "continent": "North America",
  "continent_code": "NA",
  "country": "United States",
  "country_code": "US",
  "region": "New York",
  "region_code": "NY",
  "city": "New York",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "timezone": {
    "id": "America/New_York",
    "abbr": "EST",
    "is_dst": false,
    "offset": -18000
  },
  "connection": {
    "asn": 7922,
    "org": "Comcast Cable",
    "isp": "Comcast Cable"
  },
  "security": {
    "proxy": false,
    "vpn": false,
    "tor": false
  }
}
```

## 🛠️ Agent Tools and API Usage

### 1. `get_current_ip`
- **API**: IPify API (`https://api.ipify.org?format=json`)
- **Purpose**: Get current public IP address
- **Data**: IP address only

### 2. `get_ip_with_retry`
- **API**: IPify API (`https://api.ipify.org?format=json`)
- **Purpose**: Get IP with retry logic
- **Data**: IP address with retry information

### 3. `get_ip_info`
- **APIs**: IPify API + ipapi.co
- **Purpose**: Get IP with optional location
- **Data**: IP address + location data

### 4. `get_ip_location`
- **APIs**: ipapi.co → ip-api.com → ipinfo.io → ipwhois.io (fallback chain)
- **Purpose**: Get location for any IP
- **Data**: Country, city, coordinates, timezone, ISP

### 5. `get_ip_comprehensive_info`
- **APIs**: Location APIs + Security APIs combined
- **Purpose**: Get comprehensive IP information
- **Data**: Location + security + connection data

### 6. `get_ip_security_info`
- **APIs**: ipwhois.io → ip-api.com (fallback)
- **Purpose**: Get security and connection info
- **Data**: ISP, ASN, organization, security flags

## 🔄 API Redundancy Strategy

### Location Data (4 APIs with fallback)
1. **Primary**: ipapi.co
2. **Secondary**: ip-api.com
3. **Tertiary**: ipinfo.io
4. **Quaternary**: ipwhois.io

### Security Data (2 APIs with fallback)
1. **Primary**: ipwhois.io
2. **Secondary**: ip-api.com

### Benefits:
- **High Availability**: If one API fails, others continue working
- **Data Accuracy**: Cross-reference data from multiple sources
- **Rate Limit Management**: Distribute requests across APIs
- **Geographic Coverage**: Different APIs may have better coverage in different regions

## 📊 API Comparison

| Feature | ipapi.co | ip-api.com | ipinfo.io | ipwhois.io |
|---------|----------|------------|-----------|------------|
| **Location Data** | ✅ | ✅ | ✅ | ✅ |
| **ISP Information** | ✅ | ✅ | ✅ | ✅ |
| **ASN Data** | ❌ | ✅ | ❌ | ✅ |
| **Security Data** | ❌ | ❌ | ❌ | ✅ |
| **Free Tier** | 1K/day | 45/min | 50K/month | 10K/month |
| **HTTPS** | ✅ | ❌ | ✅ | ✅ |
| **JSON Response** | ✅ | ✅ | ✅ | ✅ |
| **No API Key** | ✅ | ✅ | ✅ | ✅ |

## 📝 Usage Examples

### Basic IP Lookup
```python
# Get current IP
result = await get_current_ip()
# Returns: {"ip": "203.0.113.1", "source": "ipify-api"}
```

### Location Lookup
```python
# Get location for any IP
result = await get_ip_location("8.8.8.8")
# Returns: {"country": "United States", "city": "Mountain View", ...}
```

### Comprehensive Analysis
```python
# Get full IP analysis
result = await get_ip_comprehensive_info("8.8.8.8")
# Returns: Location + Security + Connection data
```

## 📚 Additional Resources

- [IPify Documentation](https://www.ipify.org/)
- [ipapi.co Documentation](https://ipapi.co/)
- [ip-api.com Documentation](http://ip-api.com/)
- [ipinfo.io Documentation](https://ipinfo.io/)
- [ipwhois.io Documentation](https://ipwhois.io/)
