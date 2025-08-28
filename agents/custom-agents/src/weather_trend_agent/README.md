# 🌤️ Weather Trend Agent

A comprehensive agent for retrieving historical weather data, forecasts, and weather analysis using the Open-Meteo API. Provides detailed weather information for any location worldwide.

## 🚀 Quick Start

### What it does
- Get historical weather data for any location
- Retrieve weather forecasts
- Analyze weather trends and patterns
- Convert location names to coordinates
- Access comprehensive weather variables

### Example Queries
```
"What was the weather in London last week?"
"Get a weather forecast for Tokyo"
"Show me historical weather data for New York in January"
"What's the weather trend in Sydney?"
"Get weather summary for Paris on March 15th"
```

## 📋 Available Tools

| Tool | Description | Example |
|------|-------------|---------|
| `geocode_location` | Convert location to coordinates | "Where is Tokyo located?" |
| `get_historical_weather_by_coordinates` | Get weather data by coordinates | "Weather at 40.7128, -74.0060" |
| `get_historical_weather_by_location` | Get weather data by location name | "Weather in London last month" |
| `get_weather_summary_by_date` | Get weather summary for specific date | "Weather in Paris on March 15" |
| `get_forecast_weather` | Get weather forecast | "Forecast for Tokyo" |
| `get_available_weather_variables` | List available weather data | "What weather data is available?" |

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- SAM framework
- Required dependencies (see `requirements.txt`)

### Installation
```bash
# Install agent-specific dependencies
pip install -r requirements.txt

# Or install individual packages
pip install httpx aiohttp python-dateutil pytest pytest-asyncio
```

### Dependencies
This agent requires the following custom packages:
- **httpx**: Async HTTP client for API calls
- **aiohttp**: Alternative HTTP client for service layer
- **python-dateutil**: Date parsing and manipulation
- **pytest & pytest-asyncio**: Testing framework

### Configuration
The agent is configured via `configs/agents/weather_trend_agent.yaml` and uses:
- **Primary API**: [Open-Meteo API](https://open-meteo.com/)
- **Geocoding API**: [Open-Meteo Geocoding](https://geocoding-api.open-meteo.com/)

## 🧪 Testing

### Run Tests
```bash
# API Tests (external APIs)
python tests/test_weather_api.py

# Tools Tests (agent logic)
python tests/test_weather_agent.py
```

### Test Status
- ✅ **API Tests**: Open-Meteo APIs working
- ⚠️ **Tools Tests**: Import issues (2/10 tests passing)
- ⚠️ **Needs Fix**: Import problems to resolve

## 📊 Data Sources

### Open-Meteo API
- **URL**: https://open-meteo.com/
- **Coverage**: Global weather data
- **Data**: Historical, current, and forecast weather
- **Rate Limit**: No authentication required

### Open-Meteo Geocoding
- **URL**: https://geocoding-api.open-meteo.com/
- **Purpose**: Location name to coordinates conversion
- **Rate Limit**: No authentication required

## 🎯 Use Cases

### Weather Analysis
- Historical weather pattern analysis
- Climate trend research
- Weather forecasting
- Agricultural planning

### Business Applications
- Event planning and scheduling
- Travel and tourism
- Construction and outdoor work
- Energy consumption analysis

### Research & Education
- Climate studies
- Meteorological research
- Environmental analysis
- Data science projects

## 📁 Project Structure

```
weather_trend_agent/
├── __init__.py                 # Module initialization
├── tools.py                    # Core tool functions
├── lifecycle.py                # Agent lifecycle management
├── services/                   # Service layer
│   └── weather_service.py      # Open-Meteo API client
├── tests/                      # Test files
│   ├── test_weather_agent.py           # Tools tests
│   └── test_weather_api.py             # API tests
├── API_REFERENCE.md            # Detailed API documentation
└── README.md                   # This file
```

## 🌡️ Weather Variables

### Available Data
- **Temperature**: Current, min, max, feels like
- **Precipitation**: Rain, snow, probability
- **Humidity**: Relative humidity levels
- **Wind**: Speed, direction, gusts
- **Pressure**: Atmospheric pressure
- **Visibility**: Visibility conditions
- **UV Index**: Ultraviolet radiation levels

### Time Ranges
- **Historical**: Up to 1940 (depending on location)
- **Current**: Real-time weather data
- **Forecast**: Up to 16 days ahead

## 🔒 Security & Privacy

- **No Authentication Required**: Uses public APIs
- **No Personal Data**: Only processes location and weather data
- **Rate Limiting**: Respects API rate limits
- **Data Privacy**: No user data stored

## 🚨 Error Handling

The agent provides comprehensive error handling:
- Network connectivity issues
- Invalid location names
- Date range validation
- API rate limiting
- Data parsing errors

## 📈 Performance

- **Caching**: In-memory caching for repeated requests
- **Async Operations**: Non-blocking API calls
- **Statistics Tracking**: Built-in usage metrics
- **Optimized Queries**: Efficient API usage

## 🛠️ Development

### Adding New Features
1. Add tool function to `tools.py`
2. Update configuration in YAML file
3. Add tests to test suite
4. Update documentation

### Running Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python tests/test_weather_agent.py

# Run API tests
python tests/test_weather_api.py
```

### Known Issues
- **Import Issues**: Tools tests have relative import problems
- **Fix Needed**: Update import paths in test files

## 📞 Support

- **Documentation**: See `API_REFERENCE.md` for detailed API docs
- **Tests**: Check test files for usage examples
- **Issues**: Review error handling in tools.py
- **SAM Framework**: Consult SAM documentation for deployment

## 📄 License

Follows the same license as the parent SAM project.

---

**Stay informed about the weather! 🌤️✨**
