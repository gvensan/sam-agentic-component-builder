# SAM Agents Directory

This directory contains all the agents developed for the Solace Agent Mesh (SAM) framework. Each agent is a self-contained module with its own tools, lifecycle management, configuration, and comprehensive testing.

## 📁 Directory Structure

```
src/
├── country_information_agent/     # 🌍 Country Information Agent
├── find_my_ip_agent/             # 🌐 Find My IP Agent  
├── news_snapshot_agent/          # 📰 News Snapshot Agent
├── weather_trend_agent/          # 🌤️ Weather Trend Agent
└── README.md                     # This file
```

## 🤖 Available Agents

### 🌍 Country Information Agent
**Purpose**: Provides comprehensive country data and information using REST Countries API.

**Key Features**:
- Get detailed country information by name or code
- Search countries by various criteria
- Compare multiple countries
- Get country borders and relationships
- IP geolocation using IP-API.com

**Data Sources**:
- Primary: [REST Countries API](https://restcountries.com/v3.1/)
- Secondary: [IP-API.com](http://ip-api.com/) for geolocation

**Tools**:
- `get_country_info` - Get detailed country information
- `search_countries` - Search countries by name/region
- `get_country_borders` - Get bordering countries
- `get_country_comparison` - Compare multiple countries
- `get_all_countries` - List all available countries

**Test Status**: ✅ **FULLY TESTED**
- API Tests: ✅ All external APIs working
- Tools Tests: ✅ 13/13 tests passing

---

### 📰 News Snapshot Agent
**Purpose**: Fetches and analyzes news from Google News RSS feeds with location-based filtering.

**Key Features**:
- Location-based news retrieval
- Date range filtering
- Weather news categorization
- Trending topics extraction
- News summarization

**Data Sources**:
- Primary: [Google News RSS](https://news.google.com/rss/search)

**Tools**:
- `get_news_for_location` - Get news for specific location
- `get_news_with_date_filter` - Filter news by date range
- `get_weather_news` - Get weather-related news
- `get_trending_topics` - Extract trending topics
- `get_news_snapshot` - Comprehensive news overview

**Test Status**: ✅ **FULLY TESTED**
- API Tests: ✅ Google News RSS working
- Tools Tests: ✅ 12/12 tests passing

---

### 🌤️ Weather Trend Agent
**Purpose**: Provides historical weather data and forecasts using Open-Meteo API.

**Key Features**:
- Historical weather data retrieval
- Weather forecasting
- Location geocoding
- Weather variable selection
- Date range analysis

**Data Sources**:
- Primary: [Open-Meteo API](https://open-meteo.com/)
- Geocoding: [Open-Meteo Geocoding](https://geocoding-api.open-meteo.com/)

**Tools**:
- `geocode_location` - Convert location names to coordinates
- `get_historical_weather_by_coordinates` - Get historical weather data
- `get_historical_weather_by_location` - Get weather by location name
- `get_weather_summary_by_date` - Get weather summary for specific date
- `get_forecast_weather` - Get weather forecast
- `get_available_weather_variables` - List available weather variables

**Test Status**: ⚠️ **PARTIALLY TESTED**
- API Tests: ✅ Open-Meteo APIs working
- Tools Tests: ⚠️ Import issues (2/10 tests passing)

---

### 🌐 Find My IP Agent
**Purpose**: Provides IP address information and geolocation data.

**Key Features**:
- Current IP address detection
- IP geolocation and details
- Network information
- Security analysis
- Retry mechanism for reliability

**Data Sources**:
- Primary: [IPify API](https://api.ipify.org/)
- Secondary: [IP-API.com](http://ip-api.com/)

**Tools**:
- `get_current_ip` - Get current IP address
- `get_ip_location` - Get IP geolocation
- `get_ip_info` - Get comprehensive IP information
- `get_ip_comprehensive_info` - Get detailed IP analysis
- `get_ip_with_retry` - Get IP with retry mechanism

**Test Status**: ⚠️ **PARTIALLY TESTED**
- API Tests: ✅ IPify and IP-API.com working
- Tools Tests: ⚠️ Import issues (0/11 tests passing)

---

## 🧪 Testing Strategy

Each agent follows a comprehensive testing strategy with two types of tests:

### 📡 API Tests (`test_<agent>_api.py`)
- **Purpose**: Test external APIs directly
- **Scope**: API availability, rate limits, error handling
- **No Mocking**: Tests actual API endpoints
- **Validation**: Response formats, data structures, error codes

### 🔧 Tools Tests (`test_<agent>.py`)
- **Purpose**: Test agent logic and tools
- **Scope**: Business logic, data processing, error handling
- **Mocking**: External dependencies mocked
- **Validation**: Function behavior, response formatting, edge cases

## 📊 Test Results Summary

| Agent | API Tests | Tools Tests | Overall Status |
|-------|-----------|-------------|----------------|
| 🌍 Country Information | ✅ Working | ✅ 13/13 Pass | ✅ **READY** |
| 📰 News Snapshot | ✅ Working | ✅ 12/12 Pass | ✅ **READY** |
| 🌤️ Weather Trend | ✅ Working | ⚠️ 2/10 Pass | ⚠️ **NEEDS FIX** |
| 🌐 Find My IP | ✅ Working | ⚠️ 0/11 Pass | ⚠️ **NEEDS FIX** |

## 🚀 Deployment Status

### ✅ Ready for Production
- **Country Information Agent**: Fully tested and ready
- **News Snapshot Agent**: Fully tested and ready

### ⚠️ Needs Testing Fixes
- **Weather Trend Agent**: Import issues in tools tests
- **Find My IP Agent**: Import issues in tools tests

## 📋 Agent Structure

Each agent follows a consistent structure:

```
agent_name/
├── __init__.py              # Module initialization
├── tools.py                 # Main tool functions
├── lifecycle.py             # Agent lifecycle management
├── services/                # Service layer (if applicable)
│   └── service_name.py
├── tests/                   # Test files
│   ├── test_agent_api.py    # API tests
│   └── test_agent.py        # Tools tests
├── API_REFERENCE.md         # Detailed API documentation
└── configs/                 # Agent configuration (in parent configs/)
    └── agents/
        └── agent_name.yaml
```

## 🔧 Common Dependencies

All agents use these common dependencies:
- `httpx` - Async HTTP client
- `python-dateutil` - Date parsing utilities
- `google.adk.tools` - SAM framework tools
- `solace_ai_connector.common.log` - SAM logging

## 📝 Development Guidelines

1. **Test Structure**: Always include both API and tools tests
2. **Error Handling**: Comprehensive error handling in all functions
3. **Documentation**: Detailed API reference for each agent
4. **Configuration**: YAML configuration following SAM patterns
5. **Logging**: Proper logging with agent-specific identifiers

## 🎯 Next Steps

1. **Fix Weather Trend Agent**: Resolve import issues in tools tests
2. **Fix Find My IP Agent**: Resolve import issues in tools tests
3. **Deploy Ready Agents**: Deploy Country Information and News Snapshot agents
4. **Add New Agents**: Continue building agents following this pattern

## 📞 Support

For issues with specific agents or the overall testing framework, refer to the individual agent documentation in their respective directories.

## 🔗 Quick Navigation

- [🌍 Country Information Agent](./country_information_agent/README.md)
- [📰 News Snapshot Agent](./news_snapshot_agent/README.md)
- [🌤️ Weather Trend Agent](./weather_trend_agent/README.md)
- [🌐 Find My IP Agent](./find_my_ip_agent/README.md)
