# 🌍 Country Information Agent

A comprehensive agent for retrieving detailed country information, including demographics, geography, economics, and cultural data using the REST Countries API.

## 🚀 Quick Start

### What it does
- Get detailed information about any country
- Search countries by name, region, or other criteria
- Compare multiple countries side-by-side
- Find bordering countries and relationships
- Get IP geolocation data

### Example Queries
```
"Tell me about Japan"
"Compare the United States and Canada"
"What countries border Germany?"
"Search for countries in Europe"
"Where is IP address 8.8.8.8 located?"
```

## 📋 Available Tools

| Tool | Description | Example |
|------|-------------|---------|
| `get_country_info` | Get detailed country information | "Tell me about France" |
| `search_countries` | Search countries by criteria | "Find countries in Asia" |
| `get_country_borders` | Get bordering countries | "What countries border Brazil?" |
| `get_country_comparison` | Compare multiple countries | "Compare USA and UK" |
| `get_all_countries` | List all available countries | "Show me all countries" |

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
pip install aiohttp python-dateutil pytest pytest-asyncio
```

### Dependencies
This agent requires the following custom packages:
- **aiohttp**: Async HTTP client for API calls
- **python-dateutil**: Date parsing and manipulation
- **pytest & pytest-asyncio**: Testing framework

### Configuration
The agent is configured via `configs/agents/country_information_agent.yaml` and uses:
- **Primary API**: [REST Countries API](https://restcountries.com/v3.1/)
- **Secondary API**: [IP-API.com](http://ip-api.com/) for geolocation

## 🧪 Testing

### Run Tests
```bash
# API Tests (external APIs)
python tests/test_country_information_api.py

# Tools Tests (agent logic)
python tests/test_country_agent.py
```

### Test Status
- ✅ **API Tests**: All external APIs working
- ✅ **Tools Tests**: 13/13 tests passing
- ✅ **Ready for Production**

## 📊 Data Sources

### REST Countries API
- **URL**: https://restcountries.com/v3.1/
- **Coverage**: 250+ countries and territories
- **Data**: Demographics, geography, economics, culture
- **Rate Limit**: No authentication required

### IP-API.com
- **URL**: http://ip-api.com/
- **Purpose**: IP geolocation
- **Rate Limit**: 45 requests per minute (free tier)

## 🎯 Use Cases

### Business Intelligence
- Market research and analysis
- International expansion planning
- Demographic analysis
- Economic comparisons

### Educational
- Geography and culture learning
- Research projects
- Comparative studies
- Data analysis

### Development
- Location-based applications
- Internationalization support
- Geographic data validation
- IP geolocation services

## 📁 Project Structure

```
country_information_agent/
├── __init__.py                 # Module initialization
├── tools.py                    # Core tool functions
├── lifecycle.py                # Agent lifecycle management
├── services/                   # Service layer
│   └── country_service.py      # REST Countries API client
├── tests/                      # Test files
│   ├── test_country_agent.py           # Tools tests
│   └── test_country_information_api.py # API tests
├── API_REFERENCE.md            # Detailed API documentation
└── README.md                   # This file
```

## 🔒 Security & Privacy

- **No Authentication Required**: Uses public APIs
- **No Personal Data**: Only processes country information
- **Rate Limiting**: Respects API rate limits
- **Data Privacy**: No user data stored

## 🚨 Error Handling

The agent provides comprehensive error handling:
- Network connectivity issues
- API rate limiting
- Invalid country names/codes
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
python tests/test_country_agent.py

# Run API tests
python tests/test_country_information_api.py
```

## 📞 Support

- **Documentation**: See `API_REFERENCE.md` for detailed API docs
- **Tests**: Check test files for usage examples
- **Issues**: Review error handling in tools.py
- **SAM Framework**: Consult SAM documentation for deployment

## 📄 License

Follows the same license as the parent SAM project.

---

**Ready to explore the world's countries! 🌍✨**
