# Country Information Agent - API Reference

## Overview

The Country Information Agent provides comprehensive country data using the REST Countries API. This agent can fetch detailed information about any country in the world, including geography, demographics, currencies, languages, borders, flags, and economic information.

## 🌍 Available Tools

### 1. Get Country Information
**Function**: `get_country_info`

Get comprehensive information about a specific country.

**Parameters**:
- `country_name` (string, required): Country name, code, or partial match

**Returns**:
```json
{
  "status": "success",
  "data": {
    "name": "France",
    "official_name": "French Republic",
    "capital": "Paris",
    "population": 67391582,
    "area": 551695,
    "currencies": [{"code": "EUR", "name": "Euro", "symbol": "€"}],
    "languages": [{"code": "fra", "name": "French"}],
    "borders": ["AND", "BEL", "DEU", "ITA", "LUX", "MCO", "ESP", "CHE"],
    "flag": {"png": "https://flagcdn.com/w320/fr.png", "svg": "https://flagcdn.com/fr.svg"},
    "coordinates": {"lat": 46.0, "lng": 2.0},
    "region": "Europe",
    "subregion": "Western Europe",
    "timezones": ["UTC-10:00", "UTC-09:30", "UTC-09:00", "UTC-08:00", "UTC-04:00", "UTC-03:00", "UTC+01:00", "UTC+03:00", "UTC+05:00", "UTC+10:00", "UTC+11:00", "UTC+12:00"],
    "calling_codes": "+33",
    "gdp": 0
  },
  "timestamp": "2024-01-01T12:00:00Z",
  "source": "rest-countries-api"
}
```

**Example Usage**:
- "Tell me about France"
- "Get information for Japan"
- "What's the capital of Brazil?"

### 2. Search Countries
**Function**: `search_countries`

Search for countries by name or partial match.

**Parameters**:
- `search_term` (string, required): Search term for country name

**Returns**:
```json
{
  "status": "success",
  "data": [
    {
      "name": "United States",
      "official_name": "United States of America",
      "capital": "Washington, D.C.",
      "population": 329484123,
      "region": "Americas",
      "flag": "https://flagcdn.com/w320/us.png"
    }
  ],
  "count": 1,
  "timestamp": "2024-01-01T12:00:00Z",
  "source": "rest-countries-api"
}
```

**Example Usage**:
- "Search for countries with 'united' in the name"
- "Find countries containing 'land'"
- "Show me countries with 'stan' in the name"

### 3. Get Country Borders
**Function**: `get_country_borders`

Get border information and neighboring countries.

**Parameters**:
- `country_name` (string, required): Country name or code

**Returns**:
```json
{
  "status": "success",
  "data": {
    "country": "Germany",
    "borders": [
      {
        "name": "Denmark",
        "code": "DNK",
        "capital": "Copenhagen",
        "population": 5831404,
        "flag": "https://flagcdn.com/w320/dk.png"
      }
    ],
    "border_count": 9,
    "coordinates": {"lat": 51.0, "lng": 9.0}
  },
  "timestamp": "2024-01-01T12:00:00Z",
  "source": "rest-countries-api"
}
```

**Example Usage**:
- "What countries border Germany?"
- "Show me the neighbors of France"
- "Get border information for Brazil"

### 4. Compare Countries
**Function**: `get_country_comparison`

Compare multiple countries side by side.

**Parameters**:
- `country_names` (list, required): List of 2-5 country names to compare

**Returns**:
```json
{
  "status": "success",
  "data": {
    "countries": [
      {
        "name": "United States",
        "capital": "Washington, D.C.",
        "population": 329484123,
        "area": 9833517,
        "region": "Americas",
        "currencies": [{"code": "USD", "name": "United States dollar", "symbol": "$"}],
        "languages": [{"code": "eng", "name": "English"}],
        "flag": "https://flagcdn.com/w320/us.png"
      }
    ],
    "count": 3,
    "comparison_fields": ["name", "capital", "population", "area", "region", "currencies", "languages"]
  },
  "timestamp": "2024-01-01T12:00:00Z",
  "source": "rest-countries-api"
}
```

**Example Usage**:
- "Compare USA, China, and India"
- "Show me a comparison of European countries"
- "Compare the population of Japan and Germany"

### 5. Get All Countries
**Function**: `get_all_countries`

Get list of all countries with basic information.

**Parameters**: None

**Returns**:
```json
{
  "status": "success",
  "data": [
    {
      "name": "Afghanistan",
      "official_name": "Islamic Republic of Afghanistan",
      "code": "AF",
      "capital": "Kabul",
      "population": 40218234,
      "region": "Asia",
      "flag": "https://flagcdn.com/w320/af.png"
    }
  ],
  "count": 195,
  "timestamp": "2024-01-01T12:00:00Z",
  "source": "rest-countries-api"
}
```

**Example Usage**:
- "Show me all countries"
- "List all European countries"
- "How many countries are there in the world?"

## 🔧 Error Handling

All functions return consistent error responses:

```json
{
  "status": "error",
  "error": "Country 'InvalidCountry' not found",
  "suggestions": ["France", "Germany", "Italy"],
  "timestamp": "2024-01-01T12:00:00Z"
}
```

**Common Error Scenarios**:
- Country not found (with suggestions)
- Invalid country codes
- API timeout or network errors
- Invalid comparison parameters

## 📊 Data Sources

- **Primary API**: REST Countries API (https://restcountries.com/v3.1/)
- **Authentication**: None required (free public API)
- **Rate Limits**: No rate limits (generous API)
- **Data Format**: JSON
- **Coverage**: All 195+ countries

## 🌟 Natural Language Queries

The agent understands various query formats:

### Country Information
- "Tell me about France"
- "What's the capital of Japan?"
- "How many people live in Brazil?"
- "What currency does Australia use?"
- "Show me the flag of Canada"

### Search Queries
- "Search for countries with 'united' in the name"
- "Find countries containing 'land'"
- "Show me countries with 'stan' in the name"
- "What countries have 'new' in their name?"

### Border Queries
- "What countries border Germany?"
- "Show me the neighbors of France"
- "Get border information for Brazil"
- "Which countries surround Italy?"

### Comparison Queries
- "Compare USA, China, and India"
- "Show me a comparison of European countries"
- "Compare the population of Japan and Germany"
- "Which is bigger: Canada or Australia?"

### List Queries
- "Show me all countries"
- "List all European countries"
- "How many countries are there in the world?"
- "What are the top 10 countries by population?"

## 🔄 Caching

The agent implements intelligent caching:
- **Cache Duration**: 24 hours (country data rarely changes)
- **Cache Keys**: Based on country names, codes, and search terms
- **Cache Cleanup**: Automatic cleanup of expired entries
- **Cache Statistics**: Track cache hits and misses

## 📈 Statistics Tracking

The agent tracks comprehensive usage statistics:
- Total requests processed
- Successful vs failed requests
- Most requested countries
- Cache efficiency metrics
- Response times
- Unique countries searched

## 🚀 Integration Examples

### With Weather Agent
```
User: "What's the weather like in France?"
Weather Agent: "Let me get weather data for France..."
Country Agent: "France is located in Western Europe with coordinates 46.0, 2.0"
```

### With News Agent
```
User: "Show me news from Germany"
News Agent: "Getting news for Germany..."
Country Agent: "Germany is in Central Europe, borders 9 countries, population 83.2 million"
```

### With IP Geolocation Agent
```
User: "Where is my IP located?"
IP Agent: "Your IP is in New York, USA"
Country Agent: "United States is in North America, capital Washington D.C., uses USD currency"
```

## 🛠️ Configuration

### Environment Variables
- `COUNTRY_CACHE_DURATION`: Cache duration in hours (default: 24)
- `MAX_COMPARISON_COUNT`: Maximum countries to compare (default: 5)

### Service Configuration
- **API Timeout**: 30 seconds
- **Max Retries**: 3 attempts
- **Cache Duration**: 24 hours
- **User Agent**: SAM-country_information_agent/1.0.0

## 📝 Usage Examples

### Basic Country Lookup
```
User: "Tell me about France"
Agent: "France is a country in Western Europe with capital Paris, population 67.4 million, uses Euro currency, and borders 8 countries including Germany, Italy, and Spain."
```

### Country Search
```
User: "Search for countries with 'united' in the name"
Agent: "Countries with 'united' in the name: United States, United Kingdom, United Arab Emirates, United Republic of Tanzania"
```

### Border Information
```
User: "What countries border Germany?"
Agent: "Germany borders 9 countries: Denmark, Poland, Czech Republic, Austria, Switzerland, France, Luxembourg, Belgium, and Netherlands"
```

### Country Comparison
```
User: "Compare USA, China, and India"
Agent: "Comparison of USA, China, and India:
- USA: Capital Washington D.C., Population 329.5M, Area 9.8M km²
- China: Capital Beijing, Population 1.4B, Area 9.6M km²  
- India: Capital New Delhi, Population 1.4B, Area 3.3M km²"
```

This Country Information Agent provides comprehensive global geography data and integrates seamlessly with other location-based agents in the SAM ecosystem.
